"""
Analyzes agent activity logs to identify opportunities for self-improvement.

This script is a command-line tool that serves as a key part of the agent's
meta-cognitive loop. It parses the structured activity log
(`logs/activity.log.jsonl`) to identify patterns that may indicate
inefficiencies or errors in the agent's workflow.

The analyses currently implemented are:
- **Planning Efficiency Analysis:** It scans the logs for tasks that required
  multiple `set_plan` actions. A high number of plan revisions for a single
  task can suggest that the initial planning phase was insufficient, the task
  was poorly understood, or the agent struggled to adapt to unforeseen
  challenges.
- **Protocol Adherence Analysis:** It checks for violations of key protocols,
  such as the `best-practices-001` rule which mandates that every filesystem
  write operation is followed by a read operation to verify the result.

By flagging these issues, the script provides a starting point for a deeper
post-mortem analysis, helping the agent (or its developers) to understand the
root causes of planning churn and protocol deviations, fostering a cycle of
continuous improvement.

The tool is designed to be extensible, with future analyses (such as error
rate tracking or tool usage anti-patterns) to be added as the system evolves.
"""
import argparse
import json
from collections import defaultdict

LOG_FILE_PATH = "logs/activity.log.jsonl"
ACTION_TYPE_MAP = {"set_plan": "PLAN_UPDATE"}

# Tool categories based on the `best-practices-001` protocol
WRITE_TOOLS = {
    "create_file_with_block",
    "overwrite_file_with_block",
    "replace_with_git_merge_diff",
    "delete_file",
    "rename_file",
}
READ_TOOLS = {"read_file", "list_files", "grep"}


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


def analyze_verification_adherence(log_file):
    """
    Analyzes the log to ensure write actions are followed by read actions.

    This function enforces the `best-practices-001` protocol, which mandates
    that every filesystem write operation must be followed by a verification
    step (a read/check operation) to confirm the outcome.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        list: A list of dictionaries, each detailing a violation.
    """
    violations = []
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            try:
                entry = json.loads(line)
                action = entry.get("action", {})
                details = action.get("details", {})
                tool_name = details.get("tool_name")

                if tool_name in WRITE_TOOLS:
                    # Check the next log entry for verification
                    is_verified = False
                    if i + 1 < len(lines):
                        try:
                            next_entry = json.loads(lines[i + 1])
                            next_action = next_entry.get("action", {})
                            next_details = next_action.get("details", {})
                            next_tool_name = next_details.get("tool_name")
                            if next_tool_name in READ_TOOLS:
                                is_verified = True
                        except json.JSONDecodeError:
                            # If the next line is malformed, we can't verify.
                            pass

                    if not is_verified:
                        violation = {
                            "task_id": entry.get("task", {}).get("id"),
                            "log_id": entry.get("log_id"),
                            "violating_tool": tool_name,
                        }
                        violations.append(violation)

            except json.JSONDecodeError:
                continue
    except FileNotFoundError:
        return []
    return violations


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

    print("\n[2] Analyzing for 'Verify-After-Write' Protocol Adherence...")
    verification_violations = analyze_verification_adherence(args.log_file)
    if not verification_violations:
        print("  - Result: No 'verify-after-write' protocol violations found.")
    else:
        print("  - WARNING: Found violations of the 'verify-after-write' protocol:")
        for v in verification_violations:
            print(
                f"    - Task ID: {v['task_id']}, Log ID: {v['log_id']}, "
                f"Tool: {v['violating_tool']} was not followed by a verification step."
            )

    print("\n[3] Analyzing for Critical Protocol Violations (reset_all)...")
    violation_tasks = analyze_protocol_violations(args.log_file)
    if not violation_tasks:
        print("  - Result: No critical protocol violations found.")
    else:
        print(
            "  - WARNING: Found tasks with critical protocol violations (use of `reset_all`):"
        )
        for task_id in violation_tasks:
            print(f"    - Task ID: {task_id}")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    main()
