from agentsec_bench.types import ThreatCategory
from agentsec_bench.scenarios_privilege import PrivilegeEscalationScenario
from agentsec_crosswalk.mapping import crosswalk_entry


def test_crosswalk_entry_pulls_real_scenario_metadata():
    scenario = PrivilegeEscalationScenario()
    entry = crosswalk_entry(scenario)
    assert entry["scenario_id"] == "PE-001"
    assert entry["owasp_control_id"] == scenario.owasp_control_id
    assert entry["threat_category"] == ThreatCategory.UNAUTHORIZED_TOOL_INVOCATION.value
    assert "Govern" in entry["nist_ai_rmf_functions"]


def test_unmapped_category_returns_empty_list():
    class FakeScenario:
        id = "FAKE-001"
        owasp_control_id = "ASI99"
        threat_category = "not_a_real_category"

    entry = crosswalk_entry(FakeScenario())
    assert entry["nist_ai_rmf_functions"] == []