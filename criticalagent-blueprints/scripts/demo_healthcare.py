


import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard
from criticalagent_blueprints.demo_runtime import execute_trace

from mock_hospital.environment import HospitalEnvironment
from mock_hospital.tools import lookup_patient_tool, prescribe_medication_tool
from mock_hospital.scenario import UrgentPrescriptionChangeScenario
from mock_hospital.agents import RushedIntakeAgent, CompliantIntakeAgent

print("=== CriticalAgent-Blueprints: Mock Hospital ===")
print("Scenario: Urgent Prescription Change (social-engineering pattern)\n")

scenario = UrgentPrescriptionChangeScenario()
tools = [lookup_patient_tool, prescribe_medication_tool]

for agent in [RushedIntakeAgent(), CompliantIntakeAgent()]:
    print(f"--- Agent: {agent.name} ---")

    evaluator = Evaluator(tools=tools)
    env = HospitalEnvironment()
    result = evaluator.run(scenario, agent, env)
    print(f"AgentSec-Bench detection - Attack succeeded: {result.attack_succeeded}")
    print(f"  Role violations: {result.unauthorized_tool_calls}")
    print(f"  Suspicious destinations: {result.suspicious_destinations}")

    guard = AgentGuard([
        ToolPolicy(tool_name="lookup_patient", allowed_roles=["default"]),
        ToolPolicy(tool_name="prescribe_medication", allowed_roles=["physician"]),
    ], default_deny=True)
    _, trace = agent.query(scenario.prompt, tools, HospitalEnvironment())
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