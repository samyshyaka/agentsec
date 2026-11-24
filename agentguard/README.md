# AgentGuard

Runtime authorization and guardrail middleware for AI agents that use tools.

## Status

Working prototype.

AgentGuard sits alongside [AgentSec-Bench](https://github.com/samyshyaka/agentsec-bench)
as an enforcement layer: where AgentSec-Bench detects unauthorized or manipulated
tool use after the fact, AgentGuard prevents it at runtime, before the action executes.

Currently implemented:
- A policy model (`ToolPolicy`) defining allowed roles, value thresholds, and
  allowed destinations per tool
- Runtime enforcement (`AgentGuard.check()`) that evaluates a proposed tool call
  against policy before execution
- Optional deny-by-default mode (`AgentGuard(..., default_deny=True)`) for
  unconfigured tools. The compatibility default remains allow when no policy is
  defined; applications with security-sensitive tools should opt into strict
  mode and define an explicit policy for each permitted tool.
- Audit logging of every decision, allowed or denied
- Broader policy types: role blocklists (`denied_roles`) and per-tool call-rate
  limits (`max_calls`), alongside the original role/value/destination checks
- A "requires confirmation" policy type (`requires_confirmation`) for actions
  that should never be fully automatic - a call that passes every other check
  is still held for human sign-off instead of running immediately.
  `AgentGuard.enforce()` raises `ConfirmationRequiredError` (a subtype of
  `PermissionError`) until it's called again with `confirmed=True`.
- `AgentGuard.enforce()`, a pipeline-style entry point that checks policy and
  executes the tool call in one step (raising `PermissionError` on denial, or
  `ConfirmationRequiredError` when human sign-off is needed first), so it can
  be dropped directly into an agent's tool-execution loop instead of requiring
  the caller to check() and branch manually

The monorepo's root demo executes the same synthetic tool callbacks without
protection and then wraps them with `AgentGuard.enforce()`. It shows both
callback execution and denial before the protected callback runs. The
AgentSec-Bench evaluator itself only evaluates returned traces; it does not
execute tools.

## Project layout

- `agentguard/policy.py` - the `ToolPolicy` model (allowed roles, value thresholds, allowed destinations, call limits, and confirmation requirements per tool).
- `agentguard/guard.py` - `AgentGuard.check()` and `AgentGuard.enforce()`, the runtime enforcement logic plus audit logging.
- `test_guard.py` - test suite for the policy and enforcement logic.


## Live-model testing status

- A live-model demo path is available in the monorepo at
  `agentsec-bench/scripts/live_guard_demo.py`. It exercises AgentGuard against
  a live model using the synthetic PI-001 prompt-injection scenario and local
  mock callbacks. The path is covered by offline tests, but has not yet been
  independently verified with a live provider request; it is not part of the
  default test suite and requires explicit opt-in.