import argparse
import datetime
import json
import os
import shutil
import sys
import uuid

# Define paths relative to the script's location or a known root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POSTMORTEM_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'postmortem.md')
POSTMORTEMS_DIR = os.path.join(ROOT_DIR, 'postmortems')
LOG_FILE_PATH = os.path.join(ROOT_DIR, 'logs', 'activity.log.jsonl')

def log_event(log_entry):
    """Appends a new log entry to the activity log."""
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def create_log_entry(task_id, action_type, details):
    """Creates a structured log entry dictionary."""
    return {
        "log_id": str(uuid.uuid4()),
        "session_id": os.getenv("JULES_SESSION_ID", "unknown-session"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "Phase 6",
        "task": {"id": task_id, "plan_step": -1}, # -1 indicates a tool-driven step
        "action": {
            "type": action_type,
            "details": details
        },
        "outcome": {"status": "SUCCESS", "message": f"FDC CLI: {action_type} executed successfully for task {task_id}."}
    }

def close_task(task_id):
    """
    Automates the closing of a Finite Development Cycle.
    - Creates a new post-mortem file from the template.
    - Logs the POST_MORTEM and TASK_END events.
    """
    if not task_id:
        print("Error: --task-id is required.", file=sys.stderr)
        sys.exit(1)

    # 1. Create the new post-mortem file
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    # Sanitize task_id for filename
    safe_task_id = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in task_id)
    new_postmortem_filename = f"{today_str}-{safe_task_id}.md"
    new_postmortem_path = os.path.join(POSTMORTEMS_DIR, new_postmortem_filename)

    try:
        shutil.copyfile(POSTMORTEM_TEMPLATE_PATH, new_postmortem_path)
        print(f"Successfully created new post-mortem file: {new_postmortem_path}")
    except FileNotFoundError:
        print(f"Error: Post-mortem template not found at {POSTMORTEM_TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error creating post-mortem file: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Log the POST_MORTEM event
    post_mortem_log = create_log_entry(
        task_id,
        "POST_MORTEM",
        {"summary": f"Post-mortem initiated for task '{task_id}'. File created at {new_postmortem_path}."}
    )
    log_event(post_mortem_log)
    print(f"Logged POST_MORTEM event for task: {task_id}")

    # 3. Log the TASK_END event
    task_end_log = create_log_entry(
        task_id,
        "TASK_END",
        {"summary": f"Development phase for FDC task '{task_id}' formally closed."}
    )
    log_event(task_end_log)
    print(f"Logged TASK_END event for task: {task_id}")
    print("\nFDC close process complete. Please fill out the post-mortem report.")


def main():
    """Main function for the FDC CLI tool."""
    parser = argparse.ArgumentParser(description="A tool to manage the Finite Development Cycle (FDC).")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # Define the 'close' subcommand
    close_parser = subparsers.add_parser("close", help="Closes a task, initiating the post-mortem process.")
    close_parser.add_argument("--task-id", required=True, help="The unique identifier for the task being closed.")

    args = parser.parse_args()

    if args.command == "close":
        close_task(args.task_id)
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()