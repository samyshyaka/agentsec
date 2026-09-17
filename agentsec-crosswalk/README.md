## Status

Initial crosswalk implemented and working. Reads AgentSec-Bench's real
scenario metadata (threat category, OWASP control ID) directly from all
5 of its scenarios and pairs each with relevant NIST AI RMF function(s)
(Govern/Map/Measure/Manage), producing a structured `crosswalk.json`.

Note: AgentSec-Bench's `ThreatCategory` enum currently defines two values
(prompt injection, unauthorized tool invocation) — scenarios describing
data exfiltration and privilege escalation are tagged as unauthorized
tool invocation in the underlying code. This crosswalk reflects the
actual code, not the broader narrative categories. This is a first-pass
mapping, not an exhaustive or authoritative compliance mapping.