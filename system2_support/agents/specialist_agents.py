from google.adk.agents import LlmAgent
from ..tools.firebase_logger import firebase_log_toolset
from ..tools.a2a_tool import delegate_logistics_task

voice_intake_agent = LlmAgent(
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    name="VoiceIntakeAgent",
    description="A specialist agent for handling real-time voice calls to collect relief requests.",
    instruction=(
        "You are a calm, helpful, and empathetic disaster relief voice operator. "
        "Speak naturally and collect four pieces of information: location, type of aid, number of people, and a contact number. "
        "Confirm the details, then use the 'log_relief_request' tool, and finally use the 'delegate_logistics_task' tool to notify the manager."
    ),
    tools=[firebase_log_toolset.log_relief_request, delegate_logistics_task]
)

chat_intake_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="ChatIntakeAgent",
    description="A specialist agent for handling text-based chat to collect relief requests.",
    instruction=(
        "You are a helpful and efficient disaster relief chat operator. "
        "Collect four pieces of information: location, type of aid, number of people, and a contact number. "
        "Confirm the details, then use the 'log_relief_request' tool, and finally use the 'delegate_logistics_task' tool to notify the manager."
    ),
    tools=[firebase_log_toolset.log_relief_request, delegate_logistics_task]
)

transcription_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="TranscriptionAgent",
    description="A specialist agent to create a text transcript from a call recording.",
    instruction="You receive an audio file reference. Transcribe it accurately."
)