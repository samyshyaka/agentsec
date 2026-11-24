

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard
from criticalagent_blueprints.demo_runtime import execute_trace

from mock_utility.environment import UtilityEnvironment
from mock_utility.tools import lookup_account_tool, waive_balance_tool
from mock_utility.scenario import UrgentBalanceWaiverScenario
from mock_utility.agents import PressuredServiceAgent, ProceduralServiceAgent

print("=== CriticalAgent-Blueprints: Municipal Utility ===")
print("Scenario: Urgent Balance Waiver (social-engineering pattern)\n")

scenario = UrgentBalanceWaiverScenario()
tools = [lookup_account_tool, waive_balance_tool]

for agent in [PressuredServiceAgent(), ProceduralServiceAgent()]:
    print(f"--- Agent: {agent.name} ---")

    evaluator = Evaluator(tools=tools)
    env = UtilityEnvironment()
    result = evaluator.run(scenario, agent, env)
    print(f"AgentSec-Bench detection - Attack succeeded: {result.attack_succeeded}")
    print(f"  Role violations: {result.unauthorized_tool_calls}")
    print(f"  Suspicious destinations: {result.suspicious_destinations}")

    guard = AgentGuard([
        ToolPolicy(tool_name="lookup_account", allowed_roles=["default"]),
        ToolPolicy(tool_name="waive_balance", allowed_roles=["utility_supervisor"], max_value=100.0),
    ], default_deny=True)
    _, trace = agent.query(scenario.prompt, tools, UtilityEnvironment())
    baseline = execute_trace(trace, tools, agent.role)
    protected = execute_trace(trace, tools, agent.role, guard)
    print("  Without Guard:")
    for action in baseline:
        print(f"    {action['tool_name']} {action['status'].upper()} -> {action['result']}")
    print("  With Guard:")
    for action in protected:
        if action["status"] == "denied":
            print(f"    {action['tool_name']} DENIED before callback -> {action['reason']}")
        else:
            print(f"    {action['tool_name']} EXECUTED -> {action['result']}")
    print()