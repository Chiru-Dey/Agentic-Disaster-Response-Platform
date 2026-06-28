# system1_manager/agents/resource_allocation_agent.py

from google.adk.agents import LlmAgent
from ..tools.retry_config import RESILIENT_GENERATION_CONFIG, FallbackLlm

resource_allocation_agent = LlmAgent(
    model=FallbackLlm(model="gemini-2.5-flash", fallback_model="groq/llama-3.3-70b-versatile"),
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="ResourceAllocationAgent",
    description="Decides on fair and efficient resource distribution plans based on available inventory and needs.",
    instruction=(
        "You are a fair and efficient resource allocator. Based on the following research, create a distribution plan as a structured JSON object:\n\n"
        "**Inventory Report:**\n{inventory_research}\n\n"
        "**Routing Report:**\n{routing_research}"
    ),
    output_key="distribution_plan"
)