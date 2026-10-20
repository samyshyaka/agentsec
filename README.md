# Open Agent Security Initiative

Six related open-source projects for evaluating, monitoring and defending tool-using AI agents, with a focus on critical-infrastructure settings such as healthcare, banking and utilities. This repository brings them together in one place. Each project keeps its own folder, its own README and its full git history.

## The six projects

| Project | What it does |
|---|---|
| [agentsec-bench](agentsec-bench/) | A reproducible security evaluation framework for tool-using agents. It goes beyond prompt injection to cover authorization, tool misuse, privilege escalation and data exfiltration. 9 scenarios across 8 threat categories. |
| [agentguard](agentguard/) | Runtime authorization and guardrail middleware. It checks each proposed tool call against policy (roles, value thresholds, destinations, call limits, human confirmation) before the action runs, and logs every decision. |
| [agenttrace](agenttrace/) | Turns AgentSec-Bench results into a typed stream of runtime events and runs four detection rules over it, such as an unauthorized tool call or an excessive call frequency. |
| [agentsec-scorecard](agentsec-scorecard/) | Scores AgentSec-Bench results (overall score, per-category breakdown, OWASP and NIST AI RMF coverage) and tracks the trend across runs. |
| [criticalagent-blueprints](criticalagent-blueprints/) | Reference architectures and synthetic environments for a community bank, a hospital and a municipal utility, evaluated with AgentSec-Bench (detection) and AgentGuard (prevention). |
| [agentsec-crosswalk](agentsec-crosswalk/) | Maps each AgentSec-Bench scenario to the OWASP Agentic Security Initiative controls and NIST AI RMF functions it exercises, and reports coverage gaps. |

## How they fit together

AgentSec-Bench runs attack scenarios against agents and produces results. AgentGuard prevents at runtime what the benchmark detects after the fact. AgentTrace and AgentSec-Scorecard analyze and score the benchmark output. AgentSec-Crosswalk relates the scenarios to OWASP and NIST. CriticalAgent-Blueprints applies the benchmark and the guard to sector-specific environments. The AgentSec-Bench README describes an end-to-end demo that runs all six together (`agentsec-bench/scripts/integration_demo.py`).

## Getting started

Requirements: [uv](https://docs.astral.sh/uv/) and Python 3.12 or later.

```
git clone https://github.com/samyshyaka/agentsec.git
cd agentsec/agentsec-bench
uv sync
uv run pytest -v
uv run python scripts/check_scenarios.py
```

The other projects work the same way: enter the project folder, then run `uv sync` and `uv run pytest -v`. Keep the folders side by side as they are in this repository, because the projects refer to each other by relative path (for example, agentsec-bench uses `../agentguard`).

## Releases and tags

Tags are prefixed with the project name, for example `agentsec-bench-v0.2-paper1` and `agentguard-v0.1-paper1`.

## Citing

If you use AgentSec-Bench in research, please cite the archived release: DOI 10.5281/zenodo.23107266 (v0.1.0). See `agentsec-bench/CITATION.cff` for the full metadata.

## Original repositories

These repositories are kept for their history, issues and pull requests. They point here.

- https://github.com/samyshyaka/agentsec-bench
- https://github.com/samyshyaka/agentguard
- https://github.com/samyshyaka/agenttrace
- https://github.com/samyshyaka/agentsec-scorecard
- https://github.com/samyshyaka/criticalagent-blueprints
- https://github.com/samyshyaka/agentsec-crosswalk

## Licence

Each project folder contains its own LICENSE file.