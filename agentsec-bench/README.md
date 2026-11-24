# AgentSec-Bench

A reproducible security evaluation framework for tool-using AI agents,
extending beyond AgentDojo's prompt-injection focus into authorization,
tool misuse, privilege escalation, and data exfiltration.

[![DOI](https://zenodo.org/badge/1367669000.svg)](https://doi.org/10.5281/zenodo.23107265)

## Citation

If you use AgentSec-Bench in research, please cite the archived release:

**DOI:** `10.5281/zenodo.23107266`

See [`CITATION.cff`](CITATION.cff) for the full citation metadata.

## Status

Working prototype. Currently supports:

- Core Scenario / Agent / Tool / Evaluator interfaces
- 9 scenarios across 8 threat categories (see `docs/threat-model.md` for the full breakdown):
  - Unauthorized tool invocation (UTI-001, UTI-002), prompt injection (PI-001), data exfiltration (EX-001),
    privilege escalation (PE-001), unexpected code execution (CE-001), rogue agent behavior (RA-001),
    memory/context poisoning (MP-001), human-agent trust exploitation (HT-001)
- Two independent detection mechanisms:
  - Role-based authorization checks
  - Destination-based checks (catches cases role checks alone miss)
- 26 automated tests (ground-truth validation + agent behavior checks)
- JSON results export with OWASP control mapping
- HTML report generation
- Docker-based reproducibility (Dockerfile provided; not yet build-tested end-to-end on this machine, see Reproducibility section below)
- Baseline comparison harness against AgentDojo - the comparison plan (which scenarios map to AgentDojo tasks, which test threat categories AgentDojo doesn't cover) runs locally. Live execution support is optional and requires explicit `--live` opt-in, SDK installation and API keys. No live API calls are made by the default command.
- End-to-end integration demo (`scripts/integration_demo.py`) tying together AgentSec-Bench, AgentTrace, AgentGuard, AgentSec-Scorecard and AgentSec-Crosswalk. CriticalAgent-Blueprints has separate sector demos and is not wired into this script.

## Project layout

- `agentsec_bench/core/` - the Scenario, Agent, Tool, and Evaluator base interfaces everything else builds on.
- `agentsec_bench/scenarios/` - the scenario definitions (the attack/misuse cases being tested).
- `agentsec_bench/tools/` - the mock tools scenarios use (expense, refund, inbox, CRM, admin, devops, workspace, vendor, reporting).
- `agentsec_bench/agents/` - the agent implementations under test, including the scripted stand-ins and the LLM-backed agents (`llm_agent.py`, `llm_agent_anthropic.py`).
- `tests/` - the automated test suite (ground-truth validation + agent behavior checks).
- `run_test.py` - runs all scenarios end-to-end.
- `check_scenarios.py` - validates scenario ground truth.
- `generate_report.py` - produces the HTML report.
- `run_comparison.py` / `comparison_config.py` - baseline comparison harness (builds the AgentDojo comparison plan, and runs live agents against all 9 scenarios once funded API keys are available).
- `guard_integration_demo.py` - executes the same synthetic tool callbacks with AgentGuard disabled and enabled for four scenarios.
- `integration_demo.py` - Bench + Trace + Guard + Scorecard + Crosswalk demo; writes output under this project's ignored `integration_demo_output/` folder.

## Known detection gaps

Running `integration_demo.py` surfaces a real, currently-unaddressed gap:
`HT-001` (human/agent trust exploitation) is the one scenario, of the 9, where a
successful attack is caught by neither of AgentSec-Bench's own detection
mechanisms (role-based or destination-based) nor by AgentTrace's
`SequenceAnalyzer`. It shows up as a `0.0/100` category score in the
Scorecard summary. This is a genuine coverage gap, not a bug in the demo -
worth prioritizing if further detection work is scoped for this threat
category.

## Not yet done

- Live baseline comparison results against AgentDojo. Earlier repository notes describe API testing, but live calls were not independently verified during this work. The current command requires the `live` extra, explicit `--live` opt-in and funded API access.
- Detection coverage for `HT-001` (human/agent trust exploitation) - see "Known detection gaps" above
- Broader scenario coverage

## Running it
    uv sync
    uv run python scripts/run_test.py            # run all scenarios
    uv run python scripts/check_scenarios.py      # validate ground truth
    uv run pytest -v                              # run test suite
    uv run python scripts/generate_report.py      # produce report.html
    uv run python scripts/run_comparison.py       # build the plan only; no API calls

From the monorepo root, use the integrated environment and demo:

    uv sync
    uv run python scripts/agentsec.py demo

Live comparisons are opt-in and may incur charges. From the monorepo root run
`uv sync --extra live`, then `uv run python agentsec-bench/scripts/run_comparison.py --live`.

To run a live model against the synthetic PI-001 prompt-injection scenario with
AgentGuard enforcement, run from the monorepo root:

    uv sync --extra live
    $env:OPENAI_API_KEY = "<your-key>"
    uv run python agentsec-bench/scripts/live_guard_demo.py --provider openai --model <supported-model-id> --live

For Anthropic, set `ANTHROPIC_API_KEY` and use `--provider anthropic`. By
default the demo runs independent unprotected and protected model sessions;
`--mode baseline` or `--mode guarded` runs just one. Only synthetic prompt and
tool content is sent to the provider, and callbacks are local mocks with no
external side effects. Requests may incur charges. The trace reports proposed
actions, while Guard decisions and callback logs show whether the mock action
ran. Results vary by model and run and are not a security guarantee.

## Reproducibility

Prerequisites: Python 3.12 (see `.python-version`) and [uv](https://docs.astral.sh/uv/) for
dependency management. No API keys or external services are required for the current
scripted-agent scenarios - everything runs locally and deterministically.

Setup:

    git clone <repo-url>
    cd agentsec-bench
    uv sync

This installs the exact dependency versions pinned in this project's `uv.lock`.
All scenario agents are scripted (not live LLM calls), so `scripts/run_test.py`
produces the same scenario results on every run. To run the multi-project
integration demo, use the monorepo root environment and command above; it
installs all six local projects together.

Alternative: a `Dockerfile` is included for running the benchmark in a container
without installing Python/uv locally:

    docker build -t agentsec-bench .
    docker run --rm agentsec-bench

Note: the Dockerfile has been updated to match the current `scripts/` layout but has
not yet been build-tested end-to-end on this machine (local Docker install was
blocked by a Windows Update servicing error). Worth a real build/run pass in CI or
on another machine before relying on it.
