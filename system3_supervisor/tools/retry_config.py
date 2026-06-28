import asyncio
import logging
import uuid
from typing import AsyncGenerator, List
from pydantic import PrivateAttr
from google.adk.models.base_llm import BaseLlm
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

# NOTE: attempts=1 here on purpose - retry/fallback is now handled by
# FallbackLlm below, at a higher level. Keeping a slow retry loop here too
# would compound with FallbackLlm's own attempts and defeat the goal of
# failing over to Groq quickly instead of waiting out a long Gemini outage.
RESILIENT_GENERATION_CONFIG = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)


class FallbackLlm(BaseLlm):
    """
    Tries the primary Gemini model first. On failure, switches to a Groq
    model via LiteLlm. Each side gets its own short retry budget, and if
    BOTH sides are exhausted, the whole Gemini -> Groq cycle repeats up to
    `max_rounds` times before finally giving up.
    """
    fallback_model: str
    primary_attempts: int = 2
    fallback_attempts: int = 2
    max_rounds: int = 2
    retry_delay_seconds: float = 1.5

    _primary: Gemini = PrivateAttr()
    _fallback: LiteLlm = PrivateAttr()

    def model_post_init(self, __context) -> None:
        self._primary = Gemini(model=self.model)
        self._fallback = LiteLlm(model=self.fallback_model)

    def _ensure_tool_call_ids(self, llm_request: LlmRequest) -> None:
        """Groq (via LiteLLM) requires every function_call/function_response
        pair to carry a matching, non-empty id. Gemini doesn't need this for
        its own matching, so history built while talking to Gemini may have
        it missing. Backfill it before handing history to a different
        provider."""
        pending_ids_by_name: dict = {}
        for content in llm_request.contents:
            if not content.parts:
                continue
            for part in content.parts:
                if part.function_call:
                    if not part.function_call.id:
                        part.function_call.id = f"call_{uuid.uuid4().hex[:24]}"
                    pending_ids_by_name.setdefault(
                        part.function_call.name, []
                    ).append(part.function_call.id)
                elif part.function_response:
                    if not part.function_response.id:
                        ids_for_name = pending_ids_by_name.get(part.function_response.name)
                        part.function_response.id = (
                            ids_for_name.pop(0) if ids_for_name
                            else f"call_{uuid.uuid4().hex[:24]}"
                        )

    async def _try_backend(
        self, backend: BaseLlm, label: str, model_name: str, attempts: int,
        llm_request: LlmRequest, stream: bool,
    ) -> List[LlmResponse]:
        last_error = None
        for attempt in range(1, attempts + 1):
            llm_request.model = model_name
            try:
                responses = []
                async for response in backend.generate_content_async(llm_request, stream):
                    responses.append(response)
                return responses
            except Exception as e:
                last_error = e
                logging.warning(f"{label} attempt {attempt}/{attempts} failed: {e}")
                if attempt < attempts:
                    await asyncio.sleep(self.retry_delay_seconds)
        raise last_error

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        self._ensure_tool_call_ids(llm_request)
        last_error = None
        for round_num in range(1, self.max_rounds + 1):
            try:
                responses = await self._try_backend(
                    self._primary, f"Gemini ({self.model})", self.model,
                    self.primary_attempts, llm_request, stream,
                )
                for r in responses:
                    yield r
                return
            except Exception as e:
                last_error = e
                logging.warning(f"Round {round_num}: Gemini exhausted, trying Groq.")

            try:
                responses = await self._try_backend(
                    self._fallback, f"Groq ({self.fallback_model})", self.fallback_model,
                    self.fallback_attempts, llm_request, stream,
                )
                for r in responses:
                    yield r
                return
            except Exception as e:
                last_error = e
                logging.warning(f"Round {round_num}: Groq also exhausted.")

        raise last_error