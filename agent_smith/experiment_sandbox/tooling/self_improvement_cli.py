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
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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


def analyze_protocol_violations(log_file):
    """
    Scans the log file for critical protocol violations, such as the
    unauthorized use of `reset_all`.

    This function checks for two conditions:
    1. A `SYSTEM_FAILURE` log explicitly blaming `reset_all`.
    2. A `TOOL_EXEC` log where the command contains "reset_all".

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        list: A list of unique task IDs where `reset_all` was used.
    """
    violation_tasks = set()
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    action = entry.get("action", {})
                    action_type = action.get("type")
                    details = action.get("details", {})

                    is_violation = False
                    # Case 1: The tool use was logged as a system failure.
                    if action_type == "SYSTEM_FAILURE":
                        if details.get("tool_name") == "reset_all":
                            is_violation = True

                    # Case 2: The tool was logged as a standard tool execution.
                    elif action_type == "TOOL_EXEC":
                        if "reset_all" in details.get("command", ""):
                            is_violation = True

                    if is_violation:
                        task_id = entry.get("task", {}).get("id")
                        if task_id:
                            violation_tasks.add(task_id)

                except json.JSONDecodeError:
                    # Ignore malformed lines, they are not our concern here.
                    continue
    except FileNotFoundError:
        # If the log file doesn't exist, there are no violations.
        return []
    return list(violation_tasks)


def analyze_error_rates(log_file):
    """
    Analyzes the log file to calculate action success/failure rates.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        dict: A dictionary containing total counts, success/failure counts,
              and a breakdown of failures by action type.
    """
    total_actions = 0
    success_count = 0
    failure_count = 0
    failures_by_type = defaultdict(int)

    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    total_actions += 1
                    outcome = entry.get("outcome", {})
                    status = outcome.get("status")
                    action_type = entry.get("action", {}).get("type")

                    if status == "SUCCESS":
                        success_count += 1
                    elif status == "FAILURE":
                        failure_count += 1
                        if action_type:
                            failures_by_type[action_type] += 1

                except json.JSONDecodeError:
                    continue  # Ignore malformed lines
    except FileNotFoundError:
        return {}

    if total_actions == 0:
        return {}

    return {
        "total_actions": total_actions,
        "success_count": success_count,
        "failure_count": failure_count,
        "success_rate": (success_count / total_actions) * 100,
        "failure_rate": (failure_count / total_actions) * 100,
        "failures_by_type": dict(failures_by_type),
    }


import subprocess

def run_self_improvement_task(model: str):
    """
    Invokes the agent_shell.py to run a self-improvement task for a specific model.
    """
    print(f"\n--- Initiating Self-Improvement Task for Model {model} ---")
    try:
        # We construct the command to call the agent shell
        command = ["python", "tooling/agent_shell.py", "--model", model]
        # We use subprocess.run to execute the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("--- Self-Improvement Task Output ---")
        print(result.stdout)
        print("--- Self-Improvement Task Completed ---")
    except FileNotFoundError:
        print("\n[ERROR] `python` command not found. Make sure Python is in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] The self-improvement task for Model {model} failed.")
        print(f"  - Return Code: {e.returncode}")
        print(f"  - STDOUT: {e.stdout}")
        print(f"  - STDERR: {e.stderr}")

def main():
    """
    Main function to run the self-improvement analysis CLI.
    """
    parser = argparse.ArgumentParser(
        description="Analyzes agent activity logs or runs new self-improvement tasks."
    )
    parser.add_argument(
        "--log-file",
        default=LOG_FILE_PATH,
        help=f"Path to the log file for analysis. Defaults to {LOG_FILE_PATH}",
    )
    parser.add_argument(
        "--run-improvement-for-model",
        choices=["A", "B"],
        default=None,
        help="If specified, runs a new self-improvement task under the given CSDC model (A or B), bypassing log analysis.",
    )
    args = parser.parse_args()

    if args.run_improvement_for_model:
        run_self_improvement_task(args.run_improvement_for_model)
        return

    # --- Run Analyses ---
    print("--- Running Self-Improvement Analysis ---")

    print("\n[1] Analyzing for Planning Inefficiencies...")
    inefficient_tasks = analyze_planning_efficiency(args.log_file)
    if not inefficient_tasks:
        print("  - Result: No tasks with significant planning inefficiencies found.")
    else:
        print("  - Result: Found tasks with multiple plan revisions:")
        for task_id, count in inefficient_tasks.items():
            print(f"    - Task ID: {task_id}, Plan Revisions: {count}")

    print("\n[2] Analyzing for Critical Protocol Violations...")
    violation_tasks = analyze_protocol_violations(args.log_file)
    if not violation_tasks:
        print("  - Result: No critical protocol violations found.")
    else:
        print(
            "  - WARNING: Found tasks with critical protocol violations (use of `reset_all`):"
        )
        for task_id in violation_tasks:
            print(f"    - Task ID: {task_id}")

    print("\n[3] Analyzing for Error Rates...")
    error_stats = analyze_error_rates(args.log_file)
    if not error_stats:
        print("  - Result: No actions logged or log file not found.")
    else:
        print(f"  - Overall Success Rate: {error_stats['success_rate']:.2f}%")
        print(f"  - Overall Failure Rate: {error_stats['failure_rate']:.2f}%")
        if error_stats['failures_by_type']:
            print("  - Failures by Action Type:")
            for action_type, count in sorted(error_stats['failures_by_type'].items()):
                print(f"    - {action_type}: {count} failure(s)")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    main()
