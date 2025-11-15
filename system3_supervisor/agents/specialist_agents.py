# system3_supervisor/agents/supervisor_agents.py

from google.adk.agents import LlmAgent
from tools.supervisor_tools import dashboard_toolset
# We will conceptually re-use the A2A tool logic here
# In a real project, you might share this tool definition
from system2_support.tools.a2a_tool import manager_a2a_toolset

dashboard_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="DashboardAgent",
    # ... (rest of dashboard_agent is unchanged)
    description="Provides natural language summaries of operations by querying logistics data.",
    instruction=(
        "You are a logistics analyst. Use your tools to answer supervisor questions "
        "about the current state of the relief operation by providing clear, concise summaries."
    ),
    tools=[dashboard_toolset]
)

override_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="OverrideAgent",
    description="Translates human commands into A2A calls to the Logistics Manager.",
    instruction=(
        "You are a command interface. Your job is to understand a human supervisor's "
        "command and translate it into a call to the 'LogisticsManagerTool'. "
        "You must call the 'execute_manual_override' task, passing the 'command' and 'target'."
    ),
    # Replace the old tool with the A2A tool
    tools=[manager_a2a_toolset]
)