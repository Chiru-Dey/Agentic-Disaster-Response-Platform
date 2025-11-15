# system2_support/agents/support_orchestrator.py
from google.adk.agents import LlmAgent
from .specialist_agents import voice_intake_agent, chat_intake_agent, transcription_agent

support_orchestrator_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="SupportOrchestrator",
    description="Root agent for customer support. Routes tasks to specialist agents for voice, chat, or transcription.",
    instruction=(
        "You are the central coordinator for public support. Your job is to understand the user's request and delegate it to the correct specialist agent.\n"
        "- If the request is a live voice call, delegate to the 'VoiceIntakeAgent'.\n"
        "- If the request is a text message, delegate to the 'ChatIntakeAgent'.\n"
        "- If the request is to transcribe a completed call, delegate to the 'TranscriptionAgent'."
    ),
    sub_agents=[
        voice_intake_agent,
        chat_intake_agent,
        transcription_agent
    ]
)