# system2_support/tools/a2a_tool.py
from google.adk.tools import A2aClientTool

# This tool is a client that communicates with the System 1 A2A server.
delegate_logistics_task = A2aClientTool(
    name="delegate_logistics_task",
    description="Delegates a detailed logistics request to the Core Logistics System for execution.",
    url="http://127.0.0.1:8000/run_logistics", # URL of the System 1 server
    request_body_format={"query": "{query}"}, # Maps tool input to the server's request body
    response_format="The logistics task was successfully delegated. System 1 responded with: {response}"
)