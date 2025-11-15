# system1_manager/agents/logistics_orchestrator.py
from google.adk.agents import SequentialAgent, ParallelAgent
from .request_parser_agent import request_parser_agent
from .inventory_agent import inventory_agent
from .routing_agent import routing_agent
from .resource_allocation_agent import resource_allocation_agent
from .distribution_workflow import distribution_workflow_agent

# 1. Define the parallel data gathering step
data_gathering_team = ParallelAgent(
    name="DataGatheringTeam",
    sub_agents=[
        inventory_agent,
        routing_agent
    ],
)

# 2. Define the root agent as a sequential pipeline
logistics_orchestrator_agent = SequentialAgent(
    name="LogisticsOrchestrator",
    description="Orchestrates the entire logistics workflow from request to delivery.",
    sub_agents=[
        request_parser_agent,  # <-- New first step
        data_gathering_team,
        resource_allocation_agent,
        distribution_workflow_agent
    ]
)