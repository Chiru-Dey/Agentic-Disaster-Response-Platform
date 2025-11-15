# system2_support/main.py
from agents.support_orchestrator import support_orchestrator_agent
from google.adk.runtime import adk
import asyncio

async def main():
    """Main function to run the Support Orchestrator agent."""
    print("Support Orchestrator is running. Type your request (e.g., 'A user is calling on the phone').")
    while True:
        user_input = input("Request> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response_generator = adk.run(
            agent=support_orchestrator_agent,
            prompt=user_input
        )
        
        async for chunk in response_generator:
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())