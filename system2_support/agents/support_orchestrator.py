# system2_support/agents/support_orchestrator.py
from google.adk.agents import LlmAgent
from .specialist_agents import chat_agent, voice_agent
from system2_support.tools.a2a_tool import delegate_logistics_task
from system2_support.tools.firebase_logger import log_to_firebase

support_orchestrator_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="SupportOrchestrator",
    description="Root agent for the support system. Routes user requests to the correct specialist agent or tool.",
    instruction=(
        "You are the central coordinator for the public support system. Your primary job is to understand the user's request and delegate it to the correct specialist agent or tool.\n\n"
        "**Decision-Making Criteria:**\n"
        "- If the user's request is a clear, actionable logistics task (e.g., 'send water', 'we need supplies'), you MUST use the `delegate_logistics_task` tool to send the request to the logistics system.\n"
        "- If the user wants to have a text-based conversation, delegate to the 'ChatAgent'.\n"
        "- If the user wants to have a voice-based conversation, delegate to the 'VoiceAgent'.\n"
        "- For any other type of request, handle it with your own general knowledge.\n\n"
        "After every interaction, you MUST use the `log_to_firebase` tool to record the event."
    ),
    sub_agents=[
        chat_agent,
        voice_agent
    ],
    tools=[
        log_to_firebase,
        delegate_logistics_task  # <-- New tool added here
    ]
)