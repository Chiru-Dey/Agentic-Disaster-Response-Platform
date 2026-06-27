# system1_manager/agents/request_parser_agent.py
from google.adk.agents import LlmAgent

request_parser_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="RequestParserAgent",
    description="Parses a natural language logistics request into a structured format.",
    instruction=(
        "You are a request parsing specialist. Your task is to analyze a user's request and extract the key logistical parameters.\n"
        "The user's request will be a plain text sentence. You MUST convert it into a JSON object with the following keys:\n"
        "- 'resource': The item being requested (e.g., 'water', 'food').\n"
        "- 'quantity': The number of units requested.\n"
        "- 'origin': The starting location for the delivery.\n"
        "- 'destination': The final destination for the delivery.\n"
        "Example Input: 'We need to send 500 units of water from the main_warehouse to shelter_b.'\n"
        "Example Output: {\"resource\": \"water\", \"quantity\": 500, \"origin\": \"main_warehouse\", \"destination\": \"shelter_b\"}"
    ),
    output_key="parsed_request"
)