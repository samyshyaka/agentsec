# AgentSec-Crosswalk

## Status

Maps each AgentSec-Bench scenario to the OWASP Agentic Security Initiative
(ASI) control it exercises and the NIST AI RMF function(s) it falls under
(Govern, Map, Measure, Manage), built directly from live AgentSec-Bench
scenario instances rather than a hand-maintained spreadsheet - so the
crosswalk can't silently drift out of sync with the scenarios themselves.

`scripts/generate_crosswalk.py` builds this mapping for all 9 current
AgentSec-Bench scenarios, prints a summary table, and writes it to
`crosswalk.json`.

The crosswalk also now includes a coverage-gap report: it diffs the
observed OWASP ASI controls and NIST AI RMF functions against the full
control/function universe and reports which ones have zero scenario
coverage. As of the current 9 scenarios, 7 of 10 OWASP ASI controls are
covered (ASI01, ASI02, ASI03, ASI05, ASI06, ASI09, ASI10 - missing ASI04,
ASI07, ASI08); all 4 NIST AI RMF functions are covered. This report is
written alongside the crosswalk to `crosswalk_gaps.json` and printed by the
same script run.

The OWASP ASI control universe used for the gap report (`ASI01`-`ASI10`) is
defined in `src/agentsec_crosswalk/gaps.py` and should be checked against
the authoritative OWASP ASI reference doc if that list is ever revised.

## Project layout

- `src/agentsec_crosswalk/mapping.py` - the OWASP/NIST AI RMF mapping table and `crosswalk_entry()`, which builds one crosswalk row from a real AgentSec-Bench scenario instance.
- `src/agentsec_crosswalk/gaps.py` - the coverage-gap report: diffs observed OWASP ASI controls and NIST AI RMF functions against the full universe of each and reports what has zero scenario coverage.
- `scripts/generate_crosswalk.py` - builds the crosswalk for all current AgentSec-Bench scenarios, prints a summary table plus the gap report, and writes `crosswalk.json` and `crosswalk_gaps.json`.
- `tests/test_mapping.py` - test suite for `crosswalk_entry()` against real scenario classes.
- `tests/test_gaps.py` - test suite for the coverage-gap report.

## Not yet done

- Gap report currently covers OWASP ASI controls and NIST AI RMF functions only; does not yet break gaps down by threat category or scenario type.
- No mapping yet to CriticalAgent-Blueprints' sector reference architectures - a scenario/control gap doesn't yet say which sector blueprints are affected.