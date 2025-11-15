# evaluation/run_evaluation.py
import json
import asyncio
import sys
import os

# Add the parent directory to the path to allow importing from system1_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from system1_manager.agents.logistics_orchestrator import logistics_orchestrator_agent
from google.adk.runtime import adk

async def run_single_test(agent, prompt):
    """Runs the agent for a single prompt and collects the full response."""
    response_generator = adk.run(agent=agent, prompt=prompt)
    full_response = ""
    async for chunk in response_generator:
        full_response += chunk.content
    return full_response

async def main():
    """Main evaluation function."""
    print("Starting evaluation...")
    
    with open("evaluation/scenarios.json", "r") as f:
        scenarios = json.load(f)
        
    with open("evaluation/expected_outcomes.json", "r") as f:
        expected_outcomes = json.load(f)
        
    pass_count = 0
    fail_count = 0
    
    for scenario in scenarios:
        scenario_id = scenario["scenario_id"]
        prompt = scenario["prompt"]
        
        print(f"\n--- Running {scenario_id} ---")
        print(f"Prompt: {prompt}")
        
        actual_response = await run_single_test(logistics_orchestrator_agent, prompt)
        print(f"Actual Response: {actual_response}")
        
        expected = expected_outcomes.get(scenario_id, {})
        expected_contains = expected.get("contains", [])
        
        test_passed = all(keyword in actual_response for keyword in expected_contains)
        
        if test_passed:
            print("Result: PASS")
            pass_count += 1
        else:
            print(f"Result: FAIL (Expected to contain: {expected_contains})")
            fail_count += 1
            
    print("\n--- Evaluation Summary ---")
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"Passed: {pass_count}")
    print(f"Failed: {fail_count}")
    print("--------------------------")

if __name__ == "__main__":
    asyncio.run(main())