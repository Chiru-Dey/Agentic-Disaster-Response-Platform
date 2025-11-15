# system1_manager/agents/logistics_orchestrator.py
from google.adk.agents import SequentialAgent, ParallelAgent
from .inventory_agent import inventory_agent
from .routing_agent import routing_agent
from .resource_allocation_agent import resource_allocation_agent
from .distribution_workflow import distribution_workflow_agent

# 1. Define the parallel data gathering step
data_gathering_team = ParallelAgent(
    name="DataGatheringTeam",
    sub_agents=[
        inventory_agent,
        routing_agent,
    ],
)

# 2. Update the distribution workflow to accept the plan from the previous step
distribution_workflow_agent.instruction = (
    "Execute the following distribution plan:\n{distribution_plan}"
)


# 3. Define the root agent as a sequential pipeline
logistics_orchestrator_agent = SequentialAgent(
    name="LogisticsOrchestrator",
    description="Root agent for logistics. Runs a pipeline: Gather Data (Parallel) -> Allocate Resources -> Execute Plan.",
    sub_agents=[
        data_gathering_team,
        resource_allocation_agent,
        distribution_workflow_agent
    ]
)