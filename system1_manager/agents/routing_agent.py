# system1_manager/agents/routing_agent.py
from google.adk.agents import LlmAgent
from ..tools.retry_config import RESILIENT_GENERATION_CONFIG, FallbackLlm
from ..tools.logistics_tools import find_optimal_route

routing_agent = LlmAgent(
    model=FallbackLlm(model="gemini-2.5-flash-lite", fallback_model="groq/llama-3.3-70b-versatile"),
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="RoutingAgent",
    description="A specialist agent that finds the optimal route for resource delivery.",
    instruction=(
        "You are a logistics routing specialist. Your task is to find the best route for delivering resources.\n"
        "You will receive a structured JSON object with the request details: {parsed_request}\n"
        "Extract the 'origin' and 'destination' values from this object.\n"
        "You MUST use the `find_optimal_route` tool with these values and assume the vehicle is a 'truck'.\n"
        "Based on the tool's output, provide a clear, human-readable summary of the optimal route."
    ),
    tools=[find_optimal_route],
    output_key="routing_research"
)