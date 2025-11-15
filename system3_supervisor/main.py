# system3_supervisor/main.py

from agents.supervisor_agents import dashboard_agent, override_agent
from google.adk.runtime import adk
import asyncio

async def main():
    """Main function to run the Supervisor agents."""
    print("Supervisor System is running. Choose an agent to interact with:")
    print("1. DashboardAgent (for summaries)")
    print("2. OverrideAgent (for manual commands)")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == '1':
        agent = dashboard_agent
        print("\nInteracting with DashboardAgent. Type your query.")
    elif choice == '2':
        agent = override_agent
        print("\nInteracting with OverrideAgent. Type your command.")
    else:
        print("Invalid choice.")
        return

    while True:
        user_input = input("Supervisor> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response_generator = adk.run(
            agent=agent,
            prompt=user_input
        )
        
        async for chunk in response_generator:
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())