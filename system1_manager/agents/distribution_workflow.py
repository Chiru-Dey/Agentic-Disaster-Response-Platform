# system1_manager/agents/distribution_workflow.py
from google.adk.agents import LlmAgent, SequentialAgent

# A simple agent to validate the plan structure
plan_validation_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="PlanValidationAgent",
    instruction="Review the attached plan. Confirm all required fields (e.g., location, items, route) are present. Output 'pass' or 'fail'."
)

# A placeholder agent to update inventory status
inventory_update_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="InventoryUpdateAgent",
    instruction="Use a (simulated) BigQuery tool to reserve the items in the plan, moving them from 'available' to 'dispatched' status. Confirm completion."
    # In a real scenario, this would have a BigQuery tool with write access.
)

# A placeholder agent to send the final dispatch
dispatch_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="DispatchAgent",
    instruction="Send the final, validated plan to the external dispatch API (simulated). Confirm dispatch."
)

# The SequentialAgent that orchestrates the workflow in a fixed order
distribution_workflow_agent = SequentialAgent(
    name="DistributionWorkflow",
    description="Executes a validated dispatch plan in a fixed, deterministic order: Validate -> Update Inventory -> Dispatch.",
    sub_agents=[
        plan_validation_agent,
        inventory_update_agent,
        dispatch_agent
    ]
)