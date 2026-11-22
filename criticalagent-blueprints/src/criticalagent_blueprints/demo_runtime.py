"""Execute a synthetic ToolCall trace, optionally through AgentGuard."""

from agentguard.guard import AgentGuard
from agentsec_bench.core.types import Tool, ToolCall


def execute_trace(
    trace: list[ToolCall],
    tools: list[Tool],
    agent_role: str,
    guard: AgentGuard | None = None,
) -> list[dict[str, str]]:
    tools_by_name = {tool.name: tool for tool in tools}
    actions = []

    for call in trace:
        tool = tools_by_name.get(call.tool_name)
        if tool is None:
            raise ValueError(f"No tool implementation registered for {call.tool_name!r}")

        if guard is None:
            actions.append({
                "tool_name": call.tool_name,
                "status": "executed",
                "result": str(tool.run(**call.args)),
            })
            continue

        try:
            result = guard.enforce(call.tool_name, call.args, agent_role, tool.run)
        except PermissionError:
            decision = guard.audit_log[-1]
            if decision.allowed:
                raise
            actions.append({
                "tool_name": call.tool_name,
                "status": "denied",
                "reason": decision.reason,
            })
        else:
            actions.append({
                "tool_name": call.tool_name,
                "status": "executed",
                "result": str(result),
            })

    return actions
