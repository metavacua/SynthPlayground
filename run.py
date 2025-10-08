import argparse
import json
import sys
import os
import time

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

    # 2. Generate a unique log file path and assign it to the state
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = int(time.time())
    log_file = os.path.join(log_dir, f"jules_agent_state_{timestamp}.json")
    initial_state.log_file_path = log_file

    # 3. Initialize and run the master control graph
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 4. Save the full state to the log file
    with open(log_file, "w") as f:
        json.dump(final_state.full_to_json(), f, indent=2)

    # 5. Print the final summary report
    print("\n--- Task Complete ---")
    print(f"Final State: {graph.current_state}")
    if final_state.error:
        print(f"Error: {final_state.error}")
    else:
        print("\n--- Final Report ---")
        print(final_state.final_report)

    print("\n--- State Summary ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print(f"\nFull state log saved to: {log_file}")
    print("--- End of Execution ---")

if __name__ == "__main__":
    main()