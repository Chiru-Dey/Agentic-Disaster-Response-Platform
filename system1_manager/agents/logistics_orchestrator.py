# system1_manager/agents/logistics_orchestrator.py

from google.adk.agents import LlmAgent
from .inventory_agent import inventory_agent
from .routing_agent import routing_agent
from .resource_allocation_agent import resource_allocation_agent

logistics_orchestrator_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="LogisticsOrchestrator",
    description="Root agent. Coordinates all logistics sub-agents to process relief requests.",
    instruction=(
        "You are the central coordinator for disaster relief logistics. "
        "When you receive a new request, you must follow these steps:\n"
        "1. Use the InventoryAgent to check for resource availability.\n"
        "2. Use the RoutingAgent to determine a viable delivery route.\n"
        "3. Pass the inventory and route information to the ResourceAllocationAgent to create a final plan.\n"
        "4. Present the final, structured plan as your output."
    ),
    sub_agents=[
        inventory_agent,
        routing_agent,
        resource_allocation_agent
    ]
)