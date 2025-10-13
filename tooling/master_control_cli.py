"""
The official command-line interface for the agent's master control loop.

This script is now a lightweight wrapper that passes control to the new,
API-driven `agent_shell.py`. It preserves the command-line interface while
decoupling the entry point from the FSM implementation.
"""
import argparse
import json
import sys

# Ensure the tooling directory is in the Python path
sys.path.insert(0, ".")
from tooling.agent_shell import run_agent_loop


def main():
    """
    The main entry point for the agent.

    This script parses the task description and invokes the agent shell.
    """
    parser = argparse.ArgumentParser(
        description="Run the Jules agent's master control loop."
    )
    parser.add_argument(
        "task",
        type=str,
        help="The high-level task for the agent to accomplish.",
    )
    args = parser.parse_args()

    print("--- Invoking Agent Shell ---")
    final_state = run_agent_loop(task_description=args.task)

    # 3. Print the final report
    print("\n--- Final State ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print("--- Workflow Complete ---")


if __name__ == "__main__":
    main()