# system1_manager/agents/inventory_agent.py
from google.adk.agents import LlmAgent
from system1_manager.tools.logistics_tools import get_inventory_levels

inventory_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="InventoryAgent",
    description="A specialist agent that checks inventory levels for requested resources.",
    instruction=(
        "You are an inventory specialist. Your task is to provide a detailed report on the availability of a specific resource.\n"
        "You will receive a structured JSON object with the request details: {parsed_request}\n"
        "Extract the 'resource' value from this object and use it to call the `get_inventory_levels` tool.\n"
        "Based on the tool's output, formulate a clear, human-readable summary of the inventory status."
    ),
    tools=[get_inventory_levels],
    output_key="inventory_research"
)