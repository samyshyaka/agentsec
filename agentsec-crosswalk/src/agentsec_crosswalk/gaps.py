"""
Diffs the crosswalk's observed scenario coverage against the full universe of
OWASP ASI controls and NIST AI RMF functions, and reports which ones no
AgentSec-Bench scenario currently exercises. The crosswalk on its own only
ever shows what IS covered; this is the report that surfaces blind spots for
whoever is relying on it to argue a sector's reference architecture is
actually addressed by the benchmark.
"""

# Full OWASP Agentic Security Initiative Top 10 control IDs.
# Verified 2026-09-30 against the official OWASP Top 10 for Agentic
# Applications (genai.owasp.org, announced Dec 2025): ASI01 Agent Goal
# Hijack, ASI02 Tool Misuse, ASI03 Identity & Privilege Abuse, ASI04 Agentic
# Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution, ASI06
# Memory & Context Poisoning, ASI07 Insecure Inter-Agent Communication,
# ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10
# Rogue Agents.
ALL_OWASP_ASI_CONTROLS = [
    "ASI01", "ASI02", "ASI03", "ASI04", "ASI05",
    "ASI06", "ASI07", "ASI08", "ASI09", "ASI10",
]

ALL_NIST_AI_RMF_FUNCTIONS = ["Govern", "Map", "Measure", "Manage"]


def coverage_gap_report(entries: list[dict]) -> dict:
    """
    Given a list of crosswalk_entry() rows, reports which OWASP ASI controls
    and NIST AI RMF functions have zero scenario coverage.
    """
    covered_owasp = {
        e["owasp_control_id"] for e in entries if e.get("owasp_control_id")
    }
    covered_nist = set()
    for e in entries:
        covered_nist.update(e.get("nist_ai_rmf_functions", []))

    owasp_gaps = [c for c in ALL_OWASP_ASI_CONTROLS if c not in covered_owasp]
    nist_gaps = [f for f in ALL_NIST_AI_RMF_FUNCTIONS if f not in covered_nist]

    return {
        "scenario_count": len(entries),
        "owasp_controls_covered": sorted(covered_owasp),
        "owasp_controls_uncovered": owasp_gaps,
        "nist_functions_covered": sorted(covered_nist),
        "nist_functions_uncovered": nist_gaps,
    }