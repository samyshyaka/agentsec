"""Root-level commands for the AgentSec monorepo."""

import argparse
import runpy
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = (
    "agentguard",
    "agenttrace",
    "agentsec-scorecard",
    "agentsec-bench",
    "criticalagent-blueprints",
    "agentsec-crosswalk",
)


def _run_project_tests() -> None:
    print("\n=== Tests: monorepo demo ===", flush=True)
    subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "tests"],
        cwd=ROOT,
        check=True,
    )
    for project in PROJECTS:
        print(f"\n=== Tests: {project} ===", flush=True)
        subprocess.run(
            [sys.executable, "-m", "pytest", "-v"],
            cwd=ROOT / project,
            check=True,
        )


def _run_script(path: Path) -> None:
    runpy.run_path(str(path), run_name="__main__")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agentsec",
        description="Run AgentSec demos and checks.",
    )
    parser.add_argument("command", choices=("demo", "test", "validate", "blueprints"))
    command = parser.parse_args().command

    if command == "demo":
        _run_script(ROOT / "agentsec-bench" / "scripts" / "integration_demo.py")
    elif command == "test":
        _run_project_tests()
    elif command == "validate":
        _run_script(ROOT / "agentsec-bench" / "scripts" / "check_scenarios.py")
    else:
        for script in (
            "demo.py",
            "demo_healthcare.py",
            "demo_utilities.py",
        ):
            _run_script(ROOT / "criticalagent-blueprints" / "scripts" / script)


if __name__ == "__main__":
    main()
