# AgentSec-Crosswalk

Maps AgentSec-Bench's security tests and threat categories to recognized
security frameworks — OWASP (Agentic Security Initiative controls, already
tagged per scenario) and NIST AI RMF (Govern/Map/Measure/Manage functions).

## Status

Initial crosswalk implemented. Reads AgentSec-Bench's real scenario metadata
(threat category, OWASP control ID) directly and pairs each with the
relevant NIST AI RMF function(s), producing a structured crosswalk report.
This is a first-pass mapping, not an exhaustive or authoritative compliance
mapping — it establishes the mechanism and initial coverage.