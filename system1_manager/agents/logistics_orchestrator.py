# system1_manager/agents/logistics_orchestrator.py

from google.adk.agents import LlmAgent
from .inventory_agent import inventory_agent
from .routing_agent import routing_agent
from .resource_allocation_agent import resource_allocation_agent
# Import the new workflow agent
from .distribution_workflow import distribution_workflow_agent

logistics_orchestrator_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="LogisticsOrchestrator",
    description="Root agent. Coordinates logistics sub-agents to create and then execute relief request plans.",
    instruction=(
        "You are the central coordinator for disaster relief logistics. "
        "When you receive a new request, you must first create a plan:\n"
        "1. Use the InventoryAgent to check for resource availability.\n"
        "2. Use the RoutingAgent to determine a viable delivery route.\n"
        "3. Pass the inventory and route information to the ResourceAllocationAgent to create a final, structured plan.\n"
        "Once the plan is created, you MUST delegate the execution of this plan to the 'DistributionWorkflow' agent."
    ),
    sub_agents=[
        inventory_agent,
        routing_agent,
        resource_allocation_agent,
        # Add the new workflow as a tool/sub-agent
        distribution_workflow_agent
    ]
)