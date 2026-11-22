"""Compare synthetic mock callbacks with AgentGuard disabled and enabled."""

from integration_demo import GUARD_TARGETS, _execute_tool_calls


def main() -> None:
    print("AgentSec-Bench reports trace findings; this section executes mock callbacks.")
    print("All callbacks return synthetic text and have no external side effects.\n")

    for scenario_id, (scenario, env_factory, tools, agent, guard) in GUARD_TARGETS.items():
        _, trace = agent.query(scenario.prompt, tools, env_factory())
        baseline = _execute_tool_calls(trace, tools, agent.role)
        protected = _execute_tool_calls(trace, tools, agent.role, guard)

        print(f"=== {scenario_id}: {agent.name} ===")
        for action in baseline:
            print(f"Without Guard: {action['tool_name']} EXECUTED -> {action['result']}")
        for action in protected:
            if action["status"] == "denied":
                print(f"With Guard: {action['tool_name']} DENIED before callback -> {action['reason']}")
            else:
                print(f"With Guard: {action['tool_name']} EXECUTED -> {action['result']}")
        print()


if __name__ == "__main__":
    main()
