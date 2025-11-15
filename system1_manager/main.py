# system1_manager/main.py

import uvicorn
from agents.logistics_orchestrator import logistics_orchestrator_agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# This function converts the ADK agent into an A2A-compatible FastAPI application.
# It automatically generates the Agent Card.
a2a_app = to_a2a(logistics_orchestrator_agent, port=8001)

# The following allows running the server directly using 'python main.py'
# In production, you would use a command like:
# uvicorn system1_manager.main:a2a_app --host 0.0.0.0 --port 8001
if __name__ == "__main__":
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)