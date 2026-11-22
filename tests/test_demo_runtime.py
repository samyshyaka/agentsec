from collections.abc import Callable
import runpy
from pathlib import Path

from agentguard.guard import AgentGuard
from agentguard.policy import ToolPolicy
from agentsec_bench.core.types import Tool, ToolCall, ToolPermission
from pydantic import BaseModel

from criticalagent_blueprints.demo_runtime import execute_trace


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_DEMO = ROOT / "agentsec-bench" / "scripts" / "integration_demo.py"


class DemoArgs(BaseModel):
    value: str


def _make_tool(callback: Callable[[str], str]) -> Tool:
    return Tool(
        name="simulated_action",
        description="A local-only test action.",
        parameters=DemoArgs,
        permission=ToolPermission(),
        run=callback,
    )


def test_blueprint_demo_executes_unprotected_but_not_when_guard_denies():
    executed = []
    tool = _make_tool(lambda value: executed.append(value) or f"simulated {value}")
    trace = [ToolCall(tool_name="simulated_action", args={"value": "action"})]
    guard = AgentGuard(
        [ToolPolicy(tool_name="simulated_action", allowed_roles=["authorized"])],
        default_deny=True,
    )

    baseline = execute_trace(trace, [tool], "default")
    protected = execute_trace(trace, [tool], "default", guard)

    assert baseline[0]["status"] == "executed"
    assert protected[0]["status"] == "denied"
    assert executed == ["action"]


def test_blueprint_demo_executes_allowed_call_under_guard():
    executed = []
    tool = _make_tool(lambda value: executed.append(value) or f"simulated {value}")
    guard = AgentGuard(
        [ToolPolicy(tool_name="simulated_action", allowed_roles=["default"])],
        default_deny=True,
    )

    result = execute_trace(
        [ToolCall(tool_name="simulated_action", args={"value": "safe"})],
        [tool],
        "default",
        guard,
    )

    assert result[0]["status"] == "executed"
    assert executed == ["safe"]


def test_integration_demo_executes_same_action_before_and_after_enforcement():
    namespace = runpy.run_path(str(INTEGRATION_DEMO), run_name="agentsec_demo_test")
    execute_tool_calls = namespace["_execute_tool_calls"]
    executed = []
    tool = _make_tool(lambda value: executed.append(value) or f"simulated {value}")
    trace = [ToolCall(tool_name="simulated_action", args={"value": "action"})]
    guard = AgentGuard(
        [ToolPolicy(tool_name="simulated_action", allowed_roles=["authorized"])],
        default_deny=True,
    )

    baseline = execute_tool_calls(trace, [tool], "default")
    protected = execute_tool_calls(trace, [tool], "default", guard)

    assert baseline[0]["status"] == "executed"
    assert protected[0]["status"] == "denied"
    assert executed == ["action"]


def test_integration_demo_reports_blocked_actions():
    namespace = runpy.run_path(str(INTEGRATION_DEMO), run_name="agentsec_demo_test")
    blocked_count, guard_total, action_runs = namespace["run_guard_demo"]()

    assert (blocked_count, guard_total) == (4, 4)
    for run in action_runs:
        denied = next(action for action in run["guarded_actions"] if action["status"] == "denied")
        matching_baseline = next(
            action for action in run["baseline_actions"]
            if action["tool_name"] == denied["tool_name"]
        )
        assert matching_baseline["status"] == "executed"
