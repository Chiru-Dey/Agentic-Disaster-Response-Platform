# system1_manager/main.py
import os
import logging
import uvicorn
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.runtime import Runner
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

runner = Runner()

class LogisticsRequest(BaseModel):
    """Request model for the logistics endpoint."""
    query: str

@app.post("/run_logistics")
async def run_logistics_workflow(request: LogisticsRequest):
    """
    Run the logistics orchestrator agent with the provided query.
    This is the primary entry point for A2A communication from other systems.
    """
    final_response = ""
    async for chunk in runner.run_agent(
        agent=logistics_orchestrator_agent,
        message=request.query
    ):
        final_response += chunk['content']
    
    return {"response": final_response}

# --- Main execution (for local testing) ---

async def main():
    """A sample async main function to run the agent's REPL for local testing."""
    print("--- Core Logistics System 1 (A2A Server Mode) ---")
    print("To test the server, run 'uvicorn system1_manager.main:app --reload'")
    print("To interact directly, use the local REPL below.")
    
    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ("exit", "quit"):
                break
            
            async for chunk in runner.run_agent(
                agent=logistics_orchestrator_agent,
                message=user_input
            ):
                print(f"Agent > {chunk['content']}", end="", flush=True)
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