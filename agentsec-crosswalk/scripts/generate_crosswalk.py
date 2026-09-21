import json

from agentsec_bench.scenarios.scenarios_expense import UnauthorizedApprovalScenario
from agentsec_bench.scenarios.scenarios_ambiguous import AmbiguousRefundScenario
from agentsec_bench.scenarios.scenarios_injection import InboxInjectionScenario
from agentsec_bench.scenarios.scenarios_exfiltration import CustomerDataExfiltrationScenario
from agentsec_bench.scenarios.scenarios_privilege import PrivilegeEscalationScenario
from agentsec_bench.scenarios.scenarios_code_execution import UnexpectedCodeExecutionScenario
from agentsec_bench.scenarios.scenarios_rogue import RogueAgentScenario
from agentsec_bench.scenarios.scenarios_memory_poisoning import MemoryPoisoningScenario
from agentsec_bench.scenarios.scenarios_trust_exploitation import TrustExploitationScenario

from agentsec_crosswalk.mapping import crosswalk_entry

SCENARIOS = [
    UnauthorizedApprovalScenario(),
    AmbiguousRefundScenario(),
    InboxInjectionScenario(),
    CustomerDataExfiltrationScenario(),
    PrivilegeEscalationScenario(),
    UnexpectedCodeExecutionScenario(),
    RogueAgentScenario(),
    MemoryPoisoningScenario(),
    TrustExploitationScenario(),
]

print("=== AgentSec-Crosswalk: OWASP / NIST AI RMF Mapping ===\n")
print(f"{'Scenario':<10} {'OWASP Control':<15} NIST AI RMF Functions")
print("-" * 70)

crosswalk = [crosswalk_entry(s) for s in SCENARIOS]

for entry in crosswalk:
    functions = ", ".join(entry["nist_ai_rmf_functions"])
    print(f"{entry['scenario_id']:<10} {entry['owasp_control_id']:<15} {functions}")

with open("crosswalk.json", "w") as f:
    json.dump({"crosswalk": crosswalk}, f, indent=2)

print(f"\nCrosswalk written to crosswalk.json ({len(crosswalk)} scenarios mapped)")