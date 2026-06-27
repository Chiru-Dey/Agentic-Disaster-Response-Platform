# import httpx
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools import AgentTool

SYSTEM1_AGENT_CARD_URL = "http://127.0.0.1:8000/.well-known/agent-card.json"

logistics_manager_agent = RemoteA2aAgent(
    name="LogisticsManagerAgent",
    description="The remote Core Logistics System (System 1). Send it a relief request and it returns a logistics decision.",
    agent_card=SYSTEM1_AGENT_CARD_URL,
)

# Wrapped as an AgentTool so existing code that imports `delegate_logistics_task`
# as a tool keeps working unchanged.
delegate_logistics_task = AgentTool(agent=logistics_manager_agent)
# SYSTEM1_URL = "http://127.0.0.1:8000/run_logistics"

# async def delegate_logistics_task(query: str) -> str:
#     """Delegates a detailed logistics request to the Core Logistics System (System 1) for execution.

#     Args:
#         query: The logistics request to send, in natural language.
#     """
#     async with httpx.AsyncClient(timeout=30.0) as client:
#         response = await client.post(SYSTEM1_URL, json={"query": query})
#         response.raise_for_status()
#         data = response.json()
#     return f"The logistics task was successfully delegated. System 1 responded with: {data.get('response', '')}"