import argparse
import sys
import os
import subprocess

# Ensure the tooling directory is in the Python path to allow for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tooling')))

from master_control import MasterControlGraph
from state import AgentState

def main():
    """
    The main entry point for initiating and running an agent task.

    This script ensures that every task is executed through the MasterControlGraph,
    enforcing the full, non-discretionary FSM-based workflow, including
    orientation, planning, execution, logging, and post-mortem analysis.
    """
    # --- Environment Bootstrap ---
    # Ensure all dependencies are installed before proceeding.
    # This makes the entry point self-sufficient and robust.
    print("--- Bootstrapping Environment: Installing dependencies... ---")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
            text=True
        )
        print("--- Dependencies are up-to-date. ---")
    except subprocess.CalledProcessError as e:
        print("FATAL: Failed to install dependencies.", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    # --- End Bootstrap ---

    parser = argparse.ArgumentParser(
        description="Run a full agent task through the Master Control FSM.",
        epilog="This is the designated entry point for all agent tasks to ensure protocol adherence."
    )
    parser.add_argument("task_description", help="A clear, concise description of the task for the agent.")
    args = parser.parse_args()

    print(f"--- Initializing Task: {args.task_description} ---")

    # 1. Initialize the agent's state for the new task
    initial_state = AgentState(task=args.task_description)

    # 2. Initialize and run the master control graph
    # This ensures the entire lifecycle is managed by the FSM
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 3. Print the final report upon completion or error
    print("\n--- Task Execution Complete ---")
    print("Final State:")
    print(final_state.to_json(indent=2))
    print("---------------------------------")

    if final_state.error:
        print(f"Task finished with an error: {final_state.error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()