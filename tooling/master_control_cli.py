"""
The official command-line interface for the agent's master control loop.

This script provides a clean entry point for initiating a task. It handles
argument parsing, initializes the agent's state, and runs the main FSM-driven
workflow defined in `master_control.py`.
"""
import argparse
import json
import sys

# Ensure the tooling directory is in the Python path
sys.path.insert(0, ".")
from tooling.master_control import MasterControlGraph
from tooling.state import AgentState


def main():
    """
    The main entry point for the agent.

    This script initializes the agent's state, runs the master control graph
    to enforce the protocol, and prints the final result.
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

    print("--- Initializing Master Control Graph ---")

    # 1. Initialize the agent's state for the new task
    initial_state = AgentState(task=args.task)

    # 2. Initialize and run the master control graph
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 3. Print the final report
    print("\n--- Final State ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print("--- Workflow Complete ---")


if __name__ == "__main__":
    main()