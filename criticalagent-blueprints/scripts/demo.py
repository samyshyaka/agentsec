import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard
from criticalagent_blueprints.demo_runtime import execute_trace

from community_bank.environment import BankEnvironment
from community_bank.tools import lookup_account_tool, transfer_funds_tool
from community_bank.scenario import UrgentWireTransferScenario
from community_bank.agents import SympatheticBankAgent, ProceduralBankAgent

print("=== CriticalAgent-Blueprints: Community Bank ===")
print("Scenario: Urgent Wire Transfer (social-engineering pattern)\n")

scenario = UrgentWireTransferScenario()
tools = [lookup_account_tool, transfer_funds_tool]

for agent in [SympatheticBankAgent(), ProceduralBankAgent()]:
    print(f"--- Agent: {agent.name} ---")

    evaluator = Evaluator(tools=tools)
    env = BankEnvironment()
    result = evaluator.run(scenario, agent, env)
    print(f"AgentSec-Bench detection - Attack succeeded: {result.attack_succeeded}")
    print(f"  Role violations: {result.unauthorized_tool_calls}")
    print(f"  Suspicious destinations: {result.suspicious_destinations}")

    guard = AgentGuard([
        ToolPolicy(tool_name="lookup_account", allowed_roles=["default"]),
        ToolPolicy(tool_name="transfer_funds", allowed_roles=["bank_officer"], max_value=500.0),
    ], default_deny=True)
    _, trace = agent.query(scenario.prompt, tools, BankEnvironment())
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