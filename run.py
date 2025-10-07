import argparse
import json
import sys

# Add tooling directory to path to import other tools
sys.path.insert(0, './tooling')
from state import AgentState
from master_control import MasterControlGraph

def main():
    """
    The main entry point for the agent.

    This script initializes the agent's state, runs the master control graph
    to enforce the protocol, and prints the final result.
    """
    parser = argparse.ArgumentParser(
        description="Jules, an extremely skilled software engineer, at your service."
    )
    parser.add_argument(
        "task",
        type=str,
        help="The task description for the agent to work on."
    )
    args = parser.parse_args()

    print(f"--- Initializing New Task: {args.task} ---")

    # 1. Initialize the agent's state for the new task
    initial_state = AgentState(task=args.task)

    # 2. Initialize and run the master control graph
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 3. Print the final report
    print("\n--- Task Complete ---")
    print(f"Final State: {graph.current_state}")
    if final_state.error:
        print(f"Error: {final_state.error}")
    else:
        print("\n--- Final Report ---")
        print(final_state.final_report)

    print("\n--- Full State Log ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print("--- End of Execution ---")

if __name__ == "__main__":
    main()