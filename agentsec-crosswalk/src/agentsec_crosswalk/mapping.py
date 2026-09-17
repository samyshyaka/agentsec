from agentsec_bench.types import ThreatCategory

# NIST AI RMF (1.0) core functions relevant to each threat category.
# Note: AgentSec-Bench's ThreatCategory enum currently has two values
# (PROMPT_INJECTION, UNAUTHORIZED_TOOL_INVOCATION); scenarios covering
# data exfiltration and privilege escalation are tagged as
# UNAUTHORIZED_TOOL_INVOCATION in the actual code. This is a first-pass
# mapping, not an exhaustive/authoritative compliance mapping.
NIST_AI_RMF_MAPPING = {
    ThreatCategory.UNAUTHORIZED_TOOL_INVOCATION: ["Govern", "Manage"],
    ThreatCategory.PROMPT_INJECTION: ["Map", "Measure"],
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