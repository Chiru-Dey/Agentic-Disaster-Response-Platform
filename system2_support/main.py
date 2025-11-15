# system2_support/main.py
import asyncio
from uuid import uuid4
from google.adk.services import InMemorySessionService, InMemoryMemoryService
from google.adk.tools import preload_memory
from google.adk.runtime import Runner
from agents.support_orchestrator import support_orchestrator_agent

async def main():
    """A sample async main function to run the agent's REPL with memory."""
    print("--- Support & Intake System 2 (with Long-Term Memory) ---")
    
    # 1. Initialize both session and memory services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    # 2. Define a callback to automatically save session to memory
    async def after_agent_callback(session):
        await memory_service.add_session_to_memory(session=session)
        print("\n[System: Session context saved to long-term memory.]")

    # 3. Create a Runner to combine services and callbacks
    runner = Runner(
        session_service=session_service,
        memory_service=memory_service,
        after_agent_callback=after_agent_callback
    )
    
    # 4. Add the preload_memory tool to the agent
    support_orchestrator_agent.tools.append(preload_memory)

    # Create a new session for this conversation
    session_id = str(uuid4())
    print(f"Created new session: {session_id}")

    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ("exit", "quit"):
                break
            
            # 5. Use the runner to interact with the agent
            async for chunk in runner.run_agent(
                agent=support_orchestrator_agent,
                session_id=session_id,
                message=user_input
            ):
                print(f"Agent > {chunk['content']}", end="", flush=True)
            print() # for a new line after the agent's response
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        pass