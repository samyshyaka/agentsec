import pytest
from pydantic import BaseModel

from agentguard.guard import AgentGuard
from agentguard.policy import ToolPolicy
from agentsec_bench.agents.guarded_tools import guard_tool_callbacks
from agentsec_bench.core.types import Tool, ToolPermission


class EmptyArgs(BaseModel):
    pass


class RecipientArgs(BaseModel):
    recipient: str


def test_guarded_tool_executes_allowed_callback_and_blocks_denied_callback():
    executed = []
    tools = [
        Tool(
            name="read_mock",
            description="Read synthetic data",
            parameters=EmptyArgs,
            permission=ToolPermission(),
            run=lambda **kwargs: "read",
        ),
        Tool(
            name="send_mock",
            description="Send synthetic data",
            parameters=RecipientArgs,
            permission=ToolPermission(),
            run=lambda **kwargs: "sent",
        ),
    ]
    guard = AgentGuard(
        policies=[
            ToolPolicy(tool_name="read_mock", allowed_roles=["default"]),
            ToolPolicy(tool_name="send_mock", allowed_destinations=[]),
        ],
        default_deny=True,
    )
    guarded = guard_tool_callbacks(
        tools,
        guard,
        "default",
        on_execute=lambda name, args: executed.append(name),
    )

    assert guarded[0].run() == "read"
    with pytest.raises(PermissionError, match="AgentGuard denied"):
        guarded[1].run(recipient="external@example.invalid")

    assert executed == ["read_mock"]
    assert [entry.decision for entry in guard.audit_log] == ["ALLOW", "DENY"]
