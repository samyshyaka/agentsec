from agentsec_crosswalk.gaps import coverage_gap_report, ALL_OWASP_ASI_CONTROLS, ALL_NIST_AI_RMF_FUNCTIONS


def test_full_coverage_reports_no_gaps():
    entries = [
        {"owasp_control_id": c, "nist_ai_rmf_functions": ALL_NIST_AI_RMF_FUNCTIONS}
        for c in ALL_OWASP_ASI_CONTROLS
    ]
    report = coverage_gap_report(entries)
    assert report["owasp_controls_uncovered"] == []
    assert report["nist_functions_uncovered"] == []


def test_partial_coverage_reports_missing_controls():
    entries = [
        {"owasp_control_id": "ASI01", "nist_ai_rmf_functions": ["Govern", "Manage"]},
        {"owasp_control_id": "ASI02", "nist_ai_rmf_functions": ["Map", "Measure"]},
    ]
    report = coverage_gap_report(entries)
    assert "ASI04" in report["owasp_controls_uncovered"]
    assert "ASI01" not in report["owasp_controls_uncovered"]
    assert report["nist_functions_uncovered"] == []


def test_no_entries_reports_everything_uncovered():
    report = coverage_gap_report([])
    assert report["owasp_controls_uncovered"] == ALL_OWASP_ASI_CONTROLS
    assert report["nist_functions_uncovered"] == ALL_NIST_AI_RMF_FUNCTIONS
    assert report["scenario_count"] == 0


def test_missing_owasp_control_id_is_ignored_not_crashed():
    entries = [{"owasp_control_id": None, "nist_ai_rmf_functions": []}]
    report = coverage_gap_report(entries)
    assert report["owasp_controls_covered"] == []