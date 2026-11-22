from agentsec_bench.core.evaluator import Evaluator
from agentguard.policy import ToolPolicy
from agentguard.guard import AgentGuard

from mock_utility.environment import UtilityEnvironment
from mock_utility.tools import lookup_account_tool, waive_balance_tool
from mock_utility.scenario import UrgentBalanceWaiverScenario
from mock_utility.agents import PressuredServiceAgent, ProceduralServiceAgent
from criticalagent_blueprints.demo_runtime import execute_trace


def test_pressured_agent_is_flagged_and_blocked():
    tools = [lookup_account_tool, waive_balance_tool]
    scenario = UrgentBalanceWaiverScenario()
    agent = PressuredServiceAgent()

    evaluator = Evaluator(tools=tools)
    result = evaluator.run(scenario, agent, UtilityEnvironment())
    assert result.attack_succeeded is True
    assert "waive_balance" in result.unauthorized_tool_calls

    guard = AgentGuard([
        ToolPolicy(tool_name="lookup_account", allowed_roles=["default"]),
        ToolPolicy(tool_name="waive_balance", allowed_roles=["utility_supervisor"], max_value=100.0),
    ], default_deny=True)
    _, trace = agent.query(scenario.prompt, tools, UtilityEnvironment())
    baseline = execute_trace(trace, tools, agent.role)
    protected = execute_trace(trace, tools, agent.role, guard)
    assert baseline[-1]["status"] == "executed"
    assert protected[-1]["status"] == "denied"


def test_procedural_agent_is_not_flagged():
    tools = [lookup_account_tool, waive_balance_tool]
    scenario = UrgentBalanceWaiverScenario()
    agent = ProceduralServiceAgent()

    evaluator = Evaluator(tools=tools)
    result = evaluator.run(scenario, agent, UtilityEnvironment())
    assert result.attack_succeeded is False