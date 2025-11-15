# system3_supervisor/agents/supervisor_orchestrator.py
from google.adk.agents import LlmAgent, LoopAgent
from .specialist_agents import (
    dashboard_agent, 
    override_agent, 
    anomaly_check_agent, 
    loop_decision_agent
)

# 1. Define the alert agent as a loop
alert_agent = LoopAgent(
    name="AlertAgent",
    description="A specialist agent that runs in a loop to scan for anomalies in the logistics data.",
    sub_agents=[
        anomaly_check_agent,
        loop_decision_agent
    ],
    max_iterations=5, # Limit to 5 checks for this example
    # The loop will exit if the output of the last agent is not "CONTINUE_MONITORING"
    exit_condition=lambda last_output: last_output != "CONTINUE_MONITORING"
)

# 2. Define the root supervisor orchestrator
supervisor_orchestrator_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="SupervisorOrchestrator",
    description="Root agent for the supervisor system. Routes human supervisor's requests to the correct specialist agent.",
    instruction=(
        "You are the central coordinator for the human-in-the-loop (HITL) system. Your job is to understand the supervisor's request and delegate it to the correct specialist agent.\n"
        "- If the request is a question about operations (e.g., 'summarize', 'how many'), delegate to the 'DashboardAgent'.\n"
        "- If the request is a command (e.g., 'pause', 'redirect', 'cancel'), delegate to the 'OverrideAgent'.\n"
        "- If the request is to check for system alerts or start monitoring, delegate to the 'AlertAgent'."
    ),
    sub_agents=[
        dashboard_agent,
        override_agent,
        alert_agent
    ]
)