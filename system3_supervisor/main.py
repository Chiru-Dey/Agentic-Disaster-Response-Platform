from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from .agents.supervisor_orchestrator import supervisor_orchestrator_agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

APP_NAME = "system3_supervisor"
USER_ID = "local-user"

async def main():
    print("Supervisor Orchestrator is running. Type your query or command.")
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)

    runner = Runner(
        app_name=APP_NAME,
        agent=supervisor_orchestrator_agent,
        session_service=session_service,
    )

    while True:
        user_input = input("Supervisor> ")
        if user_input.lower() in ["exit", "quit"]:
            break

        new_message = types.Content(role="user", parts=[types.Part(text=user_input)])

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=new_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())