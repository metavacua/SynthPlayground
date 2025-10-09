import argparse
import json
from collections import defaultdict

LOG_FILE_PATH = "logs/activity.log.jsonl"
ACTION_TYPE_MAP = {"set_plan": "PLAN_UPDATE"}


def read_log_entries(log_file):
    """
    Reads a log file and yields individual JSON entries,
    handling concatenated JSON objects on a single line.

    Args:
        log_file (str): Path to the log file.

    Yields:
        dict: A single log entry.
    """
    try:
        with open(log_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                decoder = json.JSONDecoder()
                pos = 0
                while pos < len(line):
                    try:
                        # Skip whitespace
                        while pos < len(line) and line[pos].isspace():
                            pos += 1
                        if pos == len(line):
                            break
                        obj, end_pos = decoder.raw_decode(line[pos:])
                        yield obj
                        pos += end_pos
                    except json.JSONDecodeError:
                        print(f"Warning: Skipping malformed JSON segment in line.")
                        # Move to the next potential start of a JSON object
                        next_brace = line.find("{", pos + 1)
                        if next_brace == -1:
                            break  # No more JSON objects in this line
                        pos = next_brace

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file}")


def analyze_planning_efficiency(log_file):
    """
    Analyzes the log file to find tasks with multiple plan revisions.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        dict: A dictionary mapping task IDs to the number of plan updates.
    """
    task_plan_updates = defaultdict(int)
    for entry in read_log_entries(log_file):
        action_type = entry.get("action", {}).get("type")
        tool_name = entry.get("action", {}).get("details", {}).get("tool_name")

        is_plan_update = (
            action_type == "PLAN_UPDATE"
            or ACTION_TYPE_MAP.get(tool_name) == "PLAN_UPDATE"
        )

        if is_plan_update:
            task_id = entry.get("task", {}).get("id")
            if task_id:
                task_plan_updates[task_id] += 1

    return {task: count for task, count in task_plan_updates.items() if count > 1}


def analyze_tool_errors(log_file):
    """
    Analyzes the log file to find tasks with tool execution errors.

    Args:
        log_file (str): Path to the activity log file.

    Returns:
        dict: A dictionary mapping task IDs to the number of errors.
    """
    task_errors = defaultdict(int)
    for entry in read_log_entries(log_file):
        outcome_status = entry.get("outcome", {}).get("status")

        if outcome_status == "FAILURE":
            task_id = entry.get("task", {}).get("id")
            if task_id:
                task_errors[task_id] += 1

    return dict(task_errors)


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

    print("--- Self-Improvement Analysis Report ---")

    # --- Planning Inefficiency Analysis ---
    print("\n[1] Running analysis for planning inefficiencies...")
    inefficient_tasks = analyze_planning_efficiency(args.log_file)
    if not inefficient_tasks:
        print("    -> No tasks with multiple plan revisions found.")
    else:
        print("    -> Found tasks with multiple plan revisions:")
        for task_id, count in inefficient_tasks.items():
            print(f"       - Task ID: {task_id}, Plan Revisions: {count}")

    # --- Tool Error Analysis ---
    print("\n[2] Running analysis for tool execution errors...")
    error_tasks = analyze_tool_errors(args.log_file)
    if not error_tasks:
        print("    -> No tasks with tool execution errors found.")
    else:
        print("    -> Found tasks with tool execution errors:")
        for task_id, count in error_tasks.items():
            print(f"       - Task ID: {task_id}, Error Count: {count}")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    main()
