# system3_supervisor/main.py
from agents.supervisor_orchestrator import supervisor_orchestrator_agent
from google.adk.runtime import adk
import asyncio

async def main():
    """Main function to run the Supervisor Orchestrator agent."""
    print("Supervisor Orchestrator is running. Type your query or command.")
    while True:
        user_input = input("Supervisor> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response_generator = adk.run(
            agent=supervisor_orchestrator_agent,
            prompt=user_input
        )
        
        async for chunk in response_generator:
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())