# system2_support/main.py

from agents.intake_agent import intake_agent
from google.adk.runtime import adk
import asyncio

async def main():
    """Main function to run the Intake agent."""
    print("Intake Agent is running. How can I help you?")
    while True:
        user_input = input("User> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response_generator = adk.run(
            agent=intake_agent,
            prompt=user_input
        )
        
        async for chunk in response_generator:
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())