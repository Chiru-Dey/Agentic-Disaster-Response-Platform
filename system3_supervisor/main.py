# system3_supervisor/main.py
from dotenv import load_dotenv
load_dotenv()

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.errors import APIError
from .agents.supervisor_orchestrator import supervisor_orchestrator_agent

os.environ["ADK_LOG_LEVEL"] = "INFO"
logging.basicConfig(level=logging.INFO)

APP_NAME = "system3_supervisor"

session_service = InMemorySessionService()
runner = Runner(
    app_name=APP_NAME,
    agent=supervisor_orchestrator_agent,
    session_service=session_service,
)

app = FastAPI(
    title="System 3: Supervisor (HITL)",
    description="Human supervisor REST endpoint for dashboard queries and overrides.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SuperviseRequest(BaseModel):
    message: str
    user_id: str = "supervisor"
    session_id: Optional[str] = None

class SuperviseResponse(BaseModel):
    session_id: str
    response: str

@app.post("/supervise", response_model=SuperviseResponse)
async def supervise(request: SuperviseRequest):
    session = None
    if request.session_id:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=request.user_id, session_id=request.session_id
        )
    if session is None:
        session = await session_service.create_session(app_name=APP_NAME, user_id=request.user_id)

    new_message = types.Content(role="user", parts=[types.Part(text=request.message)])

    final_response = ""
    try:
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session.id,
            new_message=new_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text
    except APIError as e:
        logging.error(f"API error occurred: {e}")
        return SuperviseResponse(session_id=session.id, response="Model API error occurred. Please try again later.")


    return SuperviseResponse(session_id=session.id, response=final_response)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Run with: uvicorn system3_supervisor.main:app --host 127.0.0.1 --port 8002