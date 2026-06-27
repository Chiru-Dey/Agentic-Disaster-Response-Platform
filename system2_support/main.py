# system2_support/main.py
import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.agents.context import Context
from google.adk.tools import preload_memory
from google.genai import types
from google.adk import Runner
from .agents.support_orchestrator import support_orchestrator_agent

APP_NAME = "system2_support"
USER_ID = "local-user"


async def main():
    print("--- Support & Intake System 2 (with Long-Term Memory) ---")
    
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    async def after_agent_callback(ctx: Context):
        await ctx.add_session_to_memory()
        print("\n[System: Session context saved to long-term memory.]")

    runner = Runner(
        app_name=APP_NAME,
        agent=support_orchestrator_agent,
        session_service=session_service,
        memory_service=memory_service,
    )

    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    print(f"Created new session: {session.id}")    

    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ("exit", "quit"):
                break
            
            new_message = types.Content(role="user", parts=[types.Part(text=user_input)])
            async for event in runner.run_async(user_id=USER_ID, session_id=session.id, new_message=new_message):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text, end="", flush=True)
            print() # for a new line after the agent's response
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        pass