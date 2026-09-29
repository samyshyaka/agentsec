from agentsec_crosswalk.agentguard_mapping import AGENTGUARD_CONTROLS, agentguard_nist_coverage


def test_all_five_controls_present():
    control_names = {c["control"] for c in AGENTGUARD_CONTROLS}
    assert control_names == {
        "agent_identity",
        "tool_authorization",
        "least_privilege",
        "human_approval_gates",
        "audit_logging",
    }


def test_every_control_maps_to_at_least_one_nist_function():
    for control in AGENTGUARD_CONTROLS:
        assert len(control["nist_ai_rmf_functions"]) >= 1


def test_agentguard_nist_coverage_aggregates_by_function():
    coverage = agentguard_nist_coverage()
    assert "tool_authorization" in coverage["Govern"]
    assert "audit_logging" in coverage["Measure"]


def test_govern_and_manage_have_agentguard_coverage():
    coverage = agentguard_nist_coverage()
    assert coverage.get("Govern")
    assert coverage.get("Manage")
