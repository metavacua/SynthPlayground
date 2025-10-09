"""
Analyzes agent activity logs to identify opportunities for self-improvement.

This script is a command-line tool that serves as a key part of the agent's
meta-cognitive loop. It parses the structured activity log
(`logs/activity.log.jsonl`) to identify patterns that may indicate
inefficiencies or errors in the agent's workflow.

The primary analysis currently implemented is:
- **Planning Efficiency Analysis:** It scans the logs for tasks that required
  multiple `set_plan` actions. A high number of plan revisions for a single
  task can suggest that the initial planning phase was insufficient, the task
  was poorly understood, or the agent struggled to adapt to unforeseen
  challenges.

By flagging these tasks, the script provides a starting point for a deeper
post-mortem analysis, helping the agent (or its developers) to understand the
root causes of the planning churn and to develop strategies for more effective
upfront planning in the future.

The tool is designed to be extensible, with future analyses (such as error
rate tracking or tool usage anti-patterns) to be added as the system evolves.
"""
import argparse
import json
from collections import defaultdict

LOG_FILE_PATH = "logs/activity.log.jsonl"
ACTION_TYPE_MAP = {"set_plan": "PLAN_UPDATE"}


def analyze_planning_efficiency(log_file):
    """
    Analyzes the log file to find tasks with multiple plan revisions.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        dict: A dictionary mapping task IDs to the number of plan updates.
    """
    task_plan_updates = defaultdict(int)
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    # Support both direct action types and mapped tool names
                    action_type = entry.get("action", {}).get("type")
                    tool_name = (
                        entry.get("action", {}).get("details", {}).get("tool_name")
                    )

                    is_plan_update = (
                        action_type == "PLAN_UPDATE"
                        or ACTION_TYPE_MAP.get(tool_name) == "PLAN_UPDATE"
                    )

                    if is_plan_update:
                        task_id = entry.get("task", {}).get("id")
                        if task_id:
                            task_plan_updates[task_id] += 1
                except json.JSONDecodeError:
                    print(f"Warning: Skipping malformed JSON line: {line.strip()}")
                    continue
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file}")
        return {}

    return {task: count for task, count in task_plan_updates.items() if count > 1}


def main():
    """
    Main function to run the self-improvement analysis CLI.
    """
    parser = argparse.ArgumentParser(
        description="Analyzes agent activity logs to identify areas for improvement."
    )
    parser.add_argument(
        "--log-file",
        default=LOG_FILE_PATH,
        help=f"Path to the log file. Defaults to {LOG_FILE_PATH}",
    )
    args = parser.parse_args()

    print("Running analysis for planning inefficiencies...")
    inefficient_tasks = analyze_planning_efficiency(args.log_file)

    if not inefficient_tasks:
        print(
            "\nAnalysis Complete: No tasks with significant planning inefficiencies found."
        )
    else:
        print(
            "\nAnalysis Complete: Found tasks with multiple plan revisions, indicating potential inefficiencies:"
        )
        for task_id, count in inefficient_tasks.items():
            print(f"  - Task ID: {task_id}, Plan Revisions: {count}")


if __name__ == "__main__":
    main()
