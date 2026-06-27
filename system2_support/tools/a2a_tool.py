import httpx

SYSTEM1_URL = "http://127.0.0.1:8000/run_logistics"

async def delegate_logistics_task(query: str) -> str:
    """Delegates a detailed logistics request to the Core Logistics System (System 1) for execution.

    Args:
        query: The logistics request to send, in natural language.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(SYSTEM1_URL, json={"query": query})
        response.raise_for_status()
        data = response.json()
    return f"The logistics task was successfully delegated. System 1 responded with: {data.get('response', '')}"