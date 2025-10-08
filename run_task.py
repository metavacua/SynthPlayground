import sys
import json
from tooling.state import AgentState
from tooling.master_control import MasterControlGraph

def main():
    """
    The main entry point for the agent's FSM-enforced development workflow.
    """
    if len(sys.argv) < 2:
        print("Usage: python run_task.py \"<your task description>\"")
        sys.exit(1)

    task_description = sys.argv[1]
    print(f"--- Initializing New Task: {task_description} ---")

    # 1. Initialize the agent's state for the new task
    initial_state = AgentState(task=task_description)
    initial_state.messages.append({
        "role": "user",
        "content": task_description
    })

    # 2. Initialize and run the master control graph
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 3. Print the final summary and save the state to a log
    print("\n--- Task Complete ---")
    print(f"Final Summary: {final_state.final_summary}")

    # Save the final state to a log file for auditing purposes.
    final_state.save_to_log()

    print("\n--- Final State Object (Summary) ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print("--------------------------")

if __name__ == "__main__":
    main()