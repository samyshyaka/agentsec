from agentsec_bench.types import ThreatCategory

# First-pass mapping from AgentSec-Bench threat categories to NIST AI RMF
# functions. Not an exhaustive/authoritative compliance mapping.
NIST_AI_RMF_MAPPING = {
    ThreatCategory.UNAUTHORIZED_TOOL_INVOCATION: ["Govern", "Manage"],
    ThreatCategory.PROMPT_INJECTION: ["Map", "Measure"],
    ThreatCategory.DATA_EXFILTRATION: ["Measure", "Manage"],
    ThreatCategory.PRIVILEGE_ESCALATION: ["Govern", "Manage"],
    ThreatCategory.UNEXPECTED_CODE_EXECUTION: ["Govern", "Manage"],
    ThreatCategory.ROGUE_AGENT: ["Govern", "Manage"],
}


def crosswalk_entry(scenario):
    """Builds one crosswalk row directly from a real AgentSec-Bench scenario instance."""
    return {
        "scenario_id": scenario.id,
        "threat_category": scenario.threat_category.value
            if hasattr(scenario.threat_category, "value") else str(scenario.threat_category),
        "owasp_control_id": scenario.owasp_control_id,
        "nist_ai_rmf_functions": NIST_AI_RMF_MAPPING.get(scenario.threat_category, []),
    }