# system1_manager/main.py

from agents.logistics_orchestrator import logistics_orchestrator_agent
from google.adk.runtime import adk
import asyncio

async def main():
    """Main function to run the Logistics Orchestrator agent."""
    print("Logistics Orchestrator is running. Type your request.")
    while True:
        user_input = input("Request> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response_generator = adk.run(
            agent=logistics_orchestrator_agent,
            prompt=user_input
        )
        
        async for chunk in response_generator:
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())