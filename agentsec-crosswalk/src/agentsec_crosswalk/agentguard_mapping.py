"""
Maps AgentGuard's five implemented controls (confirmed in agentguard's own
test suite: Agent Identity, Tool Authorization, Least Privilege, Human
Approval Gates, Audit Logging) to the NIST AI RMF functions they support.

This is a control-level view, not a scenario-level one: crosswalk.json maps
which benchmark scenarios exercise which threats, while this maps which of
AgentGuard's real, implemented defensive controls mitigate which NIST AI RMF
functions - closing the loop between what AgentSec-Bench tests for and what
AgentGuard actually does about it.

OWASP ASI control alignment is deliberately left out here pending
confirmation against the official OWASP Agentic Security Initiative Top 10
reference doc - see the same caveat already in gaps.py. Do not treat any
OWASP ASI number for these controls as authoritative without that check.
"""

AGENTGUARD_CONTROLS = [
    {
        "control": "agent_identity",
        "description": "Assigns each agent a declared identity, role, and environment (AgentIdentity), giving authorization decisions a subject to evaluate.",
        "nist_ai_rmf_functions": ["Govern"],
    },
    {
        "control": "tool_authorization",
        "description": "Pre-execution check (AgentGuard.check) of a tool call against a ToolPolicy - role, value ceiling, destination, and call-count limits.",
        "nist_ai_rmf_functions": ["Govern", "Manage"],
    },
    {
        "control": "least_privilege",
        "description": "Static comparison of the tools granted to an agent's role against the tools that role has a declared need for (AgentGuard.least_privilege_violations).",
        "nist_ai_rmf_functions": ["Govern", "Manage"],
    },
    {
        "control": "human_approval_gates",
        "description": "Blocking human-in-the-loop approval (ApprovalQueue.cli_prompt) for tool calls flagged as requiring confirmation.",
        "nist_ai_rmf_functions": ["Manage"],
    },
    {
        "control": "audit_logging",
        "description": "Records every authorization decision to an audit log for after-the-fact review.",
        "nist_ai_rmf_functions": ["Measure", "Manage"],
    },
]


def agentguard_nist_coverage() -> dict:
    """Returns, for each NIST AI RMF function, which AgentGuard controls support it."""
    coverage = {}
    for entry in AGENTGUARD_CONTROLS:
        for fn in entry["nist_ai_rmf_functions"]:
            coverage.setdefault(fn, []).append(entry["control"])
    return coverage
