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


def analyze_planning_efficiency(log_file: str) -> dict:
    """
    Analyzes the log file to find tasks with multiple plan revisions.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        dict: A dictionary mapping task IDs to the number of plan updates.
    """
    plan_updates = defaultdict(int)
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    if log_entry.get("action", {}).get("type") == "PLAN_UPDATE":
                        task_id = log_entry.get("task_id")
                        if task_id:
                            plan_updates[task_id] += 1
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass  # It's okay if the log file doesn't exist yet

    # Filter for tasks with more than one plan update
    inefficient_tasks = {
        task_id: count for task_id, count in plan_updates.items() if count > 1
    }
    return inefficient_tasks


def analyze_error_rates(log_file: str) -> dict:
    """
    Analyzes the log file to calculate action success/failure rates.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        dict: A dictionary containing total counts, success/failure counts,
              and a breakdown of failures by action type.
    """
    total_actions = 0
    failures = 0
    failures_by_type = defaultdict(int)

    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    if log_entry.get("action"):
                        total_actions += 1
                        if log_entry.get("outcome", {}).get("status") == "FAILURE":
                            failures += 1
                            action_type = log_entry["action"].get("type")
                            if action_type:
                                failures_by_type[action_type] += 1
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass

    return {
        "total_actions": total_actions,
        "total_failures": failures,
        "failure_rate": (failures / total_actions) if total_actions > 0 else 0,
        "failures_by_action_type": dict(failures_by_type),
    }


def analyze_protocol_violations(log_file: str) -> list:
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
    violating_tasks = set()
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    task_id = log_entry.get("task_id")
                    if not task_id:
                        continue

                    action_type = log_entry.get("action", {}).get("type")
                    outcome_message = log_entry.get("outcome", {}).get("message", "")

                    # Condition 1: System failure explicitly blames reset_all
                    if (
                        action_type == "SYSTEM_FAILURE"
                        and "reset_all" in outcome_message
                    ):
                        violating_tasks.add(task_id)

                    # Condition 2: A tool execution log contains reset_all
                    if action_type == "TOOL_EXEC":
                        tool_name = (
                            log_entry.get("action", {})
                            .get("details", {})
                            .get("tool_name", "")
                        )
                        if "reset_all" in tool_name:
                            violating_tasks.add(task_id)

                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass

    return sorted(list(violating_tasks))


def main():
    """
    Main function to run the self-improvement analysis CLI.
    """
    parser = argparse.ArgumentParser(
        description="Analyzes agent activity logs for self-improvement opportunities."
    )
    parser.add_argument(
        "--log-file",
        default="logs/activity.log.jsonl",
        help="Path to the activity log file.",
    )
    args = parser.parse_args()

    print("--- Running Self-Improvement Analysis ---")

    # 1. Analyze Planning Efficiency
    inefficient_tasks = analyze_planning_efficiency(args.log_file)
    if inefficient_tasks:
        print(
            "\n[Analysis] Found tasks with multiple plan revisions (potential inefficiency):"
        )
        for task_id, count in inefficient_tasks.items():
            print(f"  - Task: {task_id}, Plan Updates: {count}")
    else:
        print("\n[Analysis] No tasks with significant planning inefficiency found.")

    # 2. Analyze Error Rates
    error_data = analyze_error_rates(args.log_file)
    print("\n[Analysis] Action Success/Failure Rates:")
    print(f"  - Total Actions: {error_data['total_actions']}")
    print(f"  - Total Failures: {error_data['total_failures']}")
    print(f"  - Failure Rate: {error_data['failure_rate']:.2%}")
    if error_data["failures_by_action_type"]:
        print("  - Failures by Action Type:")
        for action_type, count in error_data["failures_by_action_type"].items():
            print(f"    - {action_type}: {count}")

    # 3. Analyze Protocol Violations
    violations = analyze_protocol_violations(args.log_file)
    if violations:
        print(
            "\n[Analysis] CRITICAL: Found tasks with protocol violations (use of `reset_all`):"
        )
        for task_id in violations:
            print(f"  - Task: {task_id}")
    else:
        print("\n[Analysis] No critical protocol violations found.")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    main()
