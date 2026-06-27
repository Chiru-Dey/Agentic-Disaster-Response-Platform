from google.adk.tools import exit_loop
from google.adk.agents import LlmAgent
from ..tools.retry_config import RESILIENT_GENERATION_CONFIG
from ..tools.supervisor_tools import dashboard_toolset, override_toolset

dashboard_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="DashboardAgent",
    description="Provides natural language summaries of operations by querying logistics data.",
    instruction=(
        "You are a logistics analyst. Use your tools to answer supervisor questions "
        "about the current state of the relief operation by providing clear, concise summaries."
    ),
    tools=[dashboard_toolset.summarize_needs]
)

override_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="OverrideAgent",
    description="Translates human commands into override actions on the Logistics Manager.",
    instruction=(
        "You are a command interface. Your job is to understand a human supervisor's "
        "command and translate it into a call to `send_override_command`, "
        "passing the 'command' and 'target'."
    ),
    tools=[override_toolset.send_override_command]
)

anomaly_check_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="AnomalyCheckAgent",
    instruction="Use a (simulated) tool to query the logistics databases for anomalies like stale requests or low inventory. Report 'No anomalies found.' or describe the specific problem.",
    output_key="anomaly_report"
)

loop_decision_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    generate_content_config=RESILIENT_GENERATION_CONFIG,
    name="LoopDecisionAgent",
    instruction=(
        "You are a monitoring supervisor. Review the following anomaly report:\n{anomaly_report}\n\n"
        "- If the report contains a problem, output the report to the human supervisor and call `exit_loop`.\n"
        "- If the report is 'No anomalies found.', call `exit_loop` is NOT needed yet — just respond with 'CONTINUE_MONITORING' and let the loop run again."
    ),
    tools=[exit_loop]
)