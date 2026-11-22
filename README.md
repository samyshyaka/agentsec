# Open Agent Security Initiative

Six related open-source projects for evaluating, monitoring and defending
tool-using AI agents. The examples use synthetic data and local mock tools.
Each project keeps its own folder, license, tests and project history.

## Quick start

Requirements: Python 3.12 or later and [uv](https://docs.astral.sh/uv/).

```powershell
git clone https://github.com/samyshyaka/agentsec.git
cd agentsec
uv sync
uv run python scripts/agentsec.py demo
```

The demo runs locally without API keys or paid services. It shows a scripted
agent's mock actions executing without AgentGuard, then runs the same proposed
calls through AgentGuard and reports denied callbacks and reasons. It also runs
AgentSec-Bench, AgentTrace, AgentSec-Scorecard and AgentSec-Crosswalk. The
separate CriticalAgent-Blueprints command runs the bank, hospital and utility
examples:

```powershell
uv run python scripts/agentsec.py blueprints
```

Run all six test suites and the demo regression tests:

```powershell
uv run python scripts/agentsec.py test
uv run python scripts/agentsec.py validate
```

Demo artifacts go to the ignored `agentsec-bench/integration_demo_output/`
folder; the quickstart does not overwrite the committed research results or
Scorecard history.

**Important interpretation:** AgentSec-Bench evaluates proposed tool-call
traces; its evaluator does not itself execute tools. The integration demo's
before/after action demonstration separately invokes the local mock callbacks
and uses `AgentGuard.enforce()` around the protected calls. These mock callbacks
only return synthetic text and have no external side effects. The Scorecard
number reports AgentSec-Bench trace detections, not an AgentGuard protection
score or a general security guarantee.

Live OpenAI/Anthropic comparisons are optional, require API keys and may incur
charges. They are not part of `uv sync`, the default demo or the test command.
To explicitly install the SDKs and opt in to live requests:

```powershell
uv sync --extra live
uv run python agentsec-bench/scripts/run_comparison.py --live
```

The comparison script only builds a plan unless `--live` is provided.

To try a live model with AgentGuard on the synthetic prompt-injection case,
use the focused demo below. It runs both an unprotected and protected session
by default; the provider sees only synthetic prompt/tool content, and mock
callbacks have no external side effects. A run may make multiple API requests
and incur charges:

```powershell
uv sync --extra live
$env:OPENAI_API_KEY = "<your-key>"
uv run python agentsec-bench/scripts/live_guard_demo.py --provider openai --model <supported-model-id> --live
```

For Anthropic, set `ANTHROPIC_API_KEY` and use `--provider anthropic`. Use
`--mode baseline` or `--mode guarded` to run only one condition. Without
`--live`, the command prints a dry-run notice and makes no requests. The trace
shows what the model proposed; AgentGuard decisions and mock callback logs show
whether an action actually executed. These model-dependent results are
illustrative, not a security guarantee.

## Scenario coverage

AgentSec-Bench currently registers **9 runnable scenarios** in its standard
benchmark matrix, covering 8 threat categories. CriticalAgent-Blueprints has
additional sector-specific scenarios and demos; these are separate from the
Bench matrix. The repository also contains archived research datasets with
15-scenario and 60-scenario experiment sets. Those archived cases are not all
implemented as runnable scenarios in the current Bench package.

## The six projects

| Project | What it does |
|---|---|
| [agentsec-bench](agentsec-bench/) | Nine deterministic security scenarios across eight threat categories, scripted agents, trace evaluation, reporting and optional live-LLM comparison support. |
| [agentguard](agentguard/) | Runtime tool authorization, call limits, confirmations, audit decisions and outcome checks. Unknown tools can be denied with `default_deny=True`. |
| [agenttrace](agenttrace/) | Converts AgentSec-Bench-reported results into typed events and applies four rule-based trace detections. It is not a general runtime telemetry collector. |
| [agentsec-scorecard](agentsec-scorecard/) | Scores AgentSec-Bench detections, reports category/framework coverage and tracks historical trends. |
| [criticalagent-blueprints](criticalagent-blueprints/) | Synthetic banking, healthcare and utility reference scenarios with runnable Bench and Guard demonstrations. These are prototypes, not production systems. |
| [agentsec-crosswalk](agentsec-crosswalk/) | Maps Bench scenarios to OWASP Agentic Security Initiative controls and NIST AI RMF functions and lists current coverage gaps. |

## How they fit together

AgentSec-Bench evaluates scripted or live-agent traces. AgentTrace analyzes
those reported traces; Scorecard summarizes Bench's detection signals; and
Crosswalk maps the scenarios. AgentGuard is an independent enforcement layer
that can be placed around tool callbacks. CriticalAgent-Blueprints combines
synthetic sector scenarios with Bench and Guard. The root demo exercises the
first five projects; `scripts/agentsec.py blueprints` runs the three sector
demos.

These are research and development tools, not certifications or assurances
that an agent is secure. See the Bench [threat model](agentsec-bench/docs/threat-model.md),
[limitations](agentsec-bench/docs/limitations.md) and [benchmark card](agentsec-bench/docs/benchmark-card.md).

## Individual projects

The root `uv sync` creates one environment containing all six local projects.
For an individual project, enter its folder and run `uv sync` followed by
`uv run pytest -v`. The full monorepo workflow is the root `scripts/agentsec.py`
command above.

## Releases, citation and licensing

Tags are prefixed with the project name. To cite the archived `agentsec-v0.1.0`
monorepo release, use the root [CITATION.cff](CITATION.cff) and its
[version DOI](https://doi.org/10.5281/zenodo.23965626). The Zenodo
[concept DOI](https://doi.org/10.5281/zenodo.23965625) points to the latest
monorepo version. For a specific project with its own archived release, use
that project's citation metadata and DOI (for example,
[AgentSec-Bench's CITATION.cff](agentsec-bench/CITATION.cff)). Each project
folder contains its own license.

## Original repositories

- https://github.com/samyshyaka/agentsec-bench
- https://github.com/samyshyaka/agentguard
- https://github.com/samyshyaka/agenttrace
- https://github.com/samyshyaka/agentsec-scorecard
- https://github.com/samyshyaka/criticalagent-blueprints
- https://github.com/samyshyaka/agentsec-crosswalk
