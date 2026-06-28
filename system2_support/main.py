# system2_support/main.py
from dotenv import load_dotenv
load_dotenv()

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
from fastapi.responses import FileResponse

STATIC_DIR = Path(__file__).resolve().parent / "static"

from pydantic import BaseModel
from typing import Optional
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.agents.context import Context
from google.adk.tools import preload_memory
from google.genai import types
from google.genai.errors import APIError
from .agents.support_orchestrator import support_orchestrator_agent

os.environ["ADK_LOG_LEVEL"] = "INFO"
logging.basicConfig(level=logging.INFO)

APP_NAME = "system2_support"

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

async def after_agent_callback(callback_context: Context):
    await callback_context.add_session_to_memory()

support_orchestrator_agent.after_agent_callback = after_agent_callback
support_orchestrator_agent.tools.append(preload_memory)

runner = Runner(
    app_name=APP_NAME,
    agent=support_orchestrator_agent,
    session_service=session_service,
    memory_service=memory_service,
)

app = FastAPI(
    title="System 2: Public Support & Intake",
    description="Human-facing REST endpoint for relief request intake.",
    version="1.0.0",
)

@app.get("/")
async def chat_ui():
    return FileResponse(STATIC_DIR / "chat.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session = None
    if request.session_id:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=request.user_id, session_id=request.session_id
        )
    if session is None:
        session = await session_service.create_session(app_name=APP_NAME, user_id=request.user_id)

    new_message = types.Content(role="user", parts=[types.Part(text=request.message)])

    final_response = ""
    try:
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session.id,
            new_message=new_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text
    except APIError as e:
        logging.error(f"API error occurred: {e}")
        return ChatResponse(session_id=session.id, response="Model API error occurred. Please try again later.")

    return ChatResponse(session_id=session.id, response=final_response)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Run with: uvicorn system2_support.main:app --host 127.0.0.1 --port 8001