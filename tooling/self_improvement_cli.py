import argparse
import json
from collections import Counter

LOG_FILE_PATH = "logs/activity.log.jsonl"

def analyze_logs():
    """
    Analyzes the activity log to identify patterns and suggest improvements.
    """
    failures = []
    task_actions = {}

    try:
        with open(LOG_FILE_PATH, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)

                    # 1. Identify failures
                    if log_entry.get("outcome", {}).get("status") == "FAILURE":
                        failures.append(log_entry)

                    # 2. Track action counts per task
                    task_id = log_entry.get("task", {}).get("id")
                    if task_id:
                        if task_id not in task_actions:
                            task_actions[task_id] = Counter()
                        action_type = log_entry.get("action", {}).get("type")
                        if action_type:
                            task_actions[task_id][action_type] += 1

                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from line: {line.strip()}")
                    continue

        print("--- Self-Improvement Analysis Report ---")

        # Report on failures
        if failures:
            print(f"\n[!] Found {len(failures)} recorded failure(s):")
            for failure in failures:
                task_id = failure.get('task', {}).get('id', 'N/A')
                action_type = failure.get('action', {}).get('type', 'N/A')
                message = failure.get('outcome', {}).get('message', 'No message.')
                print(f"  - Task: {task_id}, Action: {action_type}, Message: {message}")
        else:
            print("\n[+] No direct failures recorded in logs.")

        # Report on potential inefficiencies
        print("\n--- Task Efficiency Analysis ---")
        for task_id, counts in task_actions.items():
            print(f"\n[*] Task: {task_id}")
            if counts['PLAN_UPDATE'] > 1:
                print(f"  - Potential Inefficiency: Task required {counts['PLAN_UPDATE']} plan updates.")
            total_actions = sum(counts.values())
            print(f"  - Total Actions: {total_actions}")

        # Generate and display tasks
        analysis_data = {'failures': failures, 'task_actions': task_actions}
        suggested_tasks = generate_tasks(analysis_data)

        print("\n--- Suggested Proactive Tasks ---")
        if suggested_tasks:
            for i, task in enumerate(suggested_tasks, 1):
                print(f"{i}. {task}")
        else:
            print("No immediate improvement tasks suggested based on current analysis.")

        print("\n--- End of Report ---")

    except FileNotFoundError:
        print(f"Error: Log file not found at {LOG_FILE_PATH}")

def generate_tasks(analysis_data):
    """
    Generates a prioritized list of new improvement tasks based on log analysis.
    """
    suggestions = []

    # Priority 1: Fixes for past failures
    for failure in analysis_data['failures']:
        task_id = failure.get('task', {}).get('id', 'N/A')
        action_type = failure.get('action', {}).get('type', 'N/A')
        message = failure.get('outcome', {}).get('message', 'No message.')
        suggestion = (
            f"Fix Past Failure: Investigate and create a patch for the failure in task '{task_id}'. "
            f"The failing action was '{action_type}' with message: '{message}'."
        )
        suggestions.append(suggestion)

    # Priority 2: Protocol/Planning Improvements
    for task_id, counts in analysis_data['task_actions'].items():
        if counts['PLAN_UPDATE'] > 1:
            suggestion = (
                f"Improve Protocol/Planning: The plan for task '{task_id}' was updated "
                f"{counts['PLAN_UPDATE']} times. Review the task logs to see if the protocol "
                f"can be clarified to prevent planning churn."
            )
            suggestions.append(suggestion)

    return suggestions

def main():
    """Main function for the Self-Improvement CLI tool."""
    parser = argparse.ArgumentParser(description="A tool to analyze agent performance and suggest improvements.")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # Define the 'analyze' subcommand
    analyze_parser = subparsers.add_parser("analyze", help="Analyzes the activity log for improvement opportunities.")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_logs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()