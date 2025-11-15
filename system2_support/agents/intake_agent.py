# system2_support/agents/intake_agent.py

from google.adk.agents import LlmAgent
from tools.firebase_logger import firebase_log_toolset

intake_agent = LlmAgent(
    # In a real scenario, the model might be "gemini-1.5-flash" for voice
    model="gemini-1.5-flash",
    name="IntakeAgent",
    description="Handles public chat/voice intake for disaster relief.",
    instruction=(
        "You are a calm, helpful, and empathetic disaster relief intake operator. "
        "Your goal is to collect four critical pieces of information from the user: "
        "1. Their exact location (address or landmark). "
        "2. The type of aid needed (e.g., food, water, medical, shelter). "
        "3. The number of people requiring aid. "
        "4. A safe contact number.\n"
        "Once you have all four pieces of information, confirm them with the user. "
        "Then, you MUST use your 'log_relief_request' tool to log the request. "
        "Finally, inform the user that their request has been logged and help is being coordinated."
    ),
    tools=[firebase_log_toolset]
)