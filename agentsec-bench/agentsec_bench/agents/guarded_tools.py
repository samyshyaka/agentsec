from collections.abc import Callable
from typing import Protocol

from ..core.types import Tool


class ToolEnforcer(Protocol):
    def enforce(
        self,
        tool_name: str,
        args: dict,
        agent_role: str,
        run: Callable[..., object],
    ) -> object: ...


def guard_tool_callbacks(
    tools: list[Tool],
    guard: ToolEnforcer,
    agent_role: str,
    on_execute: Callable[[str, dict], None] | None = None,
) -> list[Tool]:
    """Return tool copies whose callbacks are authorized before execution."""
    guarded_tools = []
    for tool in tools:
        def guarded_run(
            _tool: Tool = tool,
            **args: object,
        ) -> object:
            def execute(**approved_args: object) -> object:
                if on_execute is not None:
                    on_execute(_tool.name, approved_args)
                return _tool.run(**approved_args)

            return guard.enforce(
                _tool.name,
                args,
                agent_role,
                execute,
            )

        guarded_tools.append(tool.model_copy(update={"run": guarded_run}))
    return guarded_tools
