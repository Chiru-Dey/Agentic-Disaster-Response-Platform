# system1_manager/agents/resource_allocation_agent.py

from google.adk.agents import LlmAgent

resource_allocation_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="ResourceAllocationAgent",
    description="Decides on fair and efficient resource distribution plans based on available inventory and needs.",
    instruction="You are a fair and efficient resource allocator guided by humanitarian principles. Your goal is to meet the most urgent needs first, prioritizing medical supplies and water. You must create a distribution plan as a structured JSON object based on the information provided to you."
    # This agent has no tools of its own; it operates on data passed to it.
)