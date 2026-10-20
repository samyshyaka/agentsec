from agentsec_bench.core.types import ThreatCategory
from agentsec_bench.scenarios.scenarios_privilege import PrivilegeEscalationScenario
from agentsec_bench.scenarios.scenarios_exfiltration import CustomerDataExfiltrationScenario
from agentsec_crosswalk.mapping import crosswalk_entry

from agentsec_bench.scenarios.scenarios_code_execution import UnexpectedCodeExecutionScenario
from agentsec_bench.scenarios.scenarios_rogue import RogueAgentScenario

from agentsec_bench.scenarios.scenarios_memory_poisoning import MemoryPoisoningScenario

from agentsec_bench.scenarios.scenarios_trust_exploitation import TrustExploitationScenario


def test_crosswalk_entry_pulls_real_scenario_metadata():
    scenario = PrivilegeEscalationScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "PE-001"
    assert entry["owasp_control_id"] == scenario.owasp_control_id
    assert entry["threat_category"] == ThreatCategory.PRIVILEGE_ESCALATION.value
    assert "Govern" in entry["nist_ai_rmf_functions"]


def test_crosswalk_entry_for_data_exfiltration_scenario():
    scenario = CustomerDataExfiltrationScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "EX-001"
    assert entry["owasp_control_id"] == scenario.owasp_control_id
    assert entry["threat_category"] == ThreatCategory.DATA_EXFILTRATION.value
    assert "Measure" in entry["nist_ai_rmf_functions"]


def test_unmapped_category_returns_empty_list():
    class FakeScenario:
        id = "FAKE-001"
        owasp_control_id = "ASI99"
        threat_category = "not_a_real_category"

    entry = crosswalk_entry(FakeScenario())
    assert entry["nist_ai_rmf_functions"] == []

def test_crosswalk_entry_for_code_execution_scenario():
    scenario = UnexpectedCodeExecutionScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "CE-001"
    assert entry["owasp_control_id"] == "ASI05"
    assert entry["threat_category"] == ThreatCategory.UNEXPECTED_CODE_EXECUTION.value
    assert "Govern" in entry["nist_ai_rmf_functions"]

def test_crosswalk_entry_for_rogue_agent_scenario():
    scenario = RogueAgentScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "RA-001"
    assert entry["owasp_control_id"] == "ASI10"
    assert entry["threat_category"] == ThreatCategory.ROGUE_AGENT.value
    assert "Govern" in entry["nist_ai_rmf_functions"]

def test_crosswalk_entry_for_memory_poisoning_scenario():
    scenario = MemoryPoisoningScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "MP-001"
    assert entry["owasp_control_id"] == "ASI06"
    assert entry["threat_category"] == ThreatCategory.MEMORY_CONTEXT_POISONING.value
    assert "Map" in entry["nist_ai_rmf_functions"]
    assert "Measure" in entry["nist_ai_rmf_functions"]


def test_crosswalk_entry_for_trust_exploitation_scenario():
    scenario = TrustExploitationScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "HT-001"
    assert entry["owasp_control_id"] == "ASI09"
    assert entry["threat_category"] == ThreatCategory.HUMAN_AGENT_TRUST_EXPLOITATION.value
    assert "Govern" in entry["nist_ai_rmf_functions"]
    assert "Measure" in entry["nist_ai_rmf_functions"]