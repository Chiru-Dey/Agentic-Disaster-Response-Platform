from google.adk.agents import LlmAgent
from ..tools.retry_config import RESILIENT_GENERATION_CONFIG
from .specialist_agents import chat_intake_agent, voice_intake_agent
from ..tools.a2a_tool import delegate_logistics_task
from ..tools.firebase_logger import firebase_log_toolset

support_orchestrator_agent = LlmAgent(
    model="gemini-2.5-flash",
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="SupportOrchestrator",
    description="Root agent for the support system. Routes user requests to the correct specialist agent or tool.",
    instruction=(
        "You are the central coordinator for the public support system. Your primary job is to understand the user's request and delegate it to the correct specialist agent or tool.\n\n"
        "**Decision-Making Criteria:**\n"
        "- If the user's request is a clear, actionable logistics task (e.g., 'send water', 'we need supplies'), you MUST use the `delegate_logistics_task` tool to send the request to the logistics system.\n"
        "- If the user wants to have a text-based conversation, delegate to the 'ChatIntakeAgent'.\n"
        "- If the user wants to have a voice-based conversation, delegate to the 'VoiceIntakeAgent'.\n"
        "- For any other type of request, handle it with your own general knowledge.\n\n"
        "After every interaction, you MUST use the `log_relief_request` tool to record the event."
    ),
    sub_agents=[chat_intake_agent, voice_intake_agent],
    tools=[firebase_log_toolset.log_relief_request, delegate_logistics_task]
)