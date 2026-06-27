# system1_manager/main.py
import os
import logging
import uvicorn
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.logistics_orchestrator import logistics_orchestrator_agent

# Enable verbose logging for the ADK
os.environ["ADK_LOG_LEVEL"] = "DEBUG"
logging.basicConfig(level=logging.DEBUG)

# --- FastAPI App Setup ---

app = FastAPI(
    title="System 1: Core Logistics MAS",
    description="This system provides an A2A endpoint to run the logistics workflow.",
    version="1.0.0"
)

APP_NAME = "system1_manager"
USER_ID = "a2a-caller"

session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=logistics_orchestrator_agent,
    session_service=session_service,
)
class LogisticsRequest(BaseModel):
    """Request model for the logistics endpoint."""
    query: str

@app.post("/run_logistics")
async def run_logistics_workflow(request: LogisticsRequest):
    """
    Run the logistics orchestrator agent with the provided query.
    This is the primary entry point for A2A communication from other systems.
    """
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    new_message = types.Content(role="user", parts=[types.Part(text=request.query)])

    final_response = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=new_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_response += part.text
    return {"response": final_response}

# --- Main execution (for local testing) ---

async def main():
    """A sample async main function to run the agent's REPL for local testing."""
    print("--- Core Logistics System 1 (A2A Server Mode) ---")
    print("To test the server, run 'uvicorn system1_manager.main:app --reload'")
    print("To interact directly, use the local REPL below.")
    repl_session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    
    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ("exit", "quit"):
                break
            
            new_message = types.Content(role="user", parts=[types.Part(text=user_input)])
            async for event in runner.run_async(user_id=USER_ID, session_id=repl_session.id, new_message=new_message):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)
            print()
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    # This allows running the REPL directly for testing.
    # For the A2A server, use the uvicorn command.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        pass