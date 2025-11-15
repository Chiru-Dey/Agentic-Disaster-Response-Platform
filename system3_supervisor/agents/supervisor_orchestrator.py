# system3_supervisor/agents/supervisor_orchestrator.py
from google.adk.agents import LlmAgent
from .specialist_agents import dashboard_agent, override_agent

# Placeholder for the anomaly detection agent mentioned in the blueprint
alert_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="AlertAgent",
    description="A specialist agent that runs in a loop to scan for anomalies in the logistics data.",
    instruction="You are a monitoring agent. You will be triggered periodically to check for issues like stale requests or low inventory. Report any anomalies you find."
    # This would likely be a CustomAgent wrapping a LoopAgent in a real implementation.
)

supervisor_orchestrator_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="SupervisorOrchestrator",
    description="Root agent for the supervisor system. Routes human supervisor's requests to the correct specialist agent.",
    instruction=(
        "You are the central coordinator for the human-in-the-loop (HITL) system. Your job is to understand the supervisor's request and delegate it to the correct specialist agent.\n"
        "- If the request is a question about operations (e.g., 'summarize', 'how many'), delegate to the 'DashboardAgent'.\n"
        "- If the request is a command (e.g., 'pause', 'redirect', 'cancel'), delegate to the 'OverrideAgent'.\n"
        "- If the request is to check for system alerts, delegate to the 'AlertAgent'."
    ),
    sub_agents=[
        dashboard_agent,
        override_agent,
        alert_agent
    ]
)