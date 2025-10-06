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
FSM_DEF_PATH = os.path.join(ROOT_DIR, 'tooling', 'fdc_fsm.json')

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

    today_str = datetime.date.today().strftime('%Y-%m-%d')
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

    post_mortem_log = create_log_entry(
        task_id,
        "POST_MORTEM",
        {"summary": f"Post-mortem initiated for task '{task_id}'. File created at {new_postmortem_path}."}
    )
    log_event(post_mortem_log)
    print(f"Logged POST_MORTEM event for task: {task_id}")

    task_end_log = create_log_entry(
        task_id,
        "TASK_END",
        {"summary": f"Development phase for FDC task '{task_id}' formally closed."}
    )
    log_event(task_end_log)
    print(f"Logged TASK_END event for task: {task_id}")
    print("\nFDC close process complete. Please fill out the post-mortem report.")

def validate_plan(plan_filepath):
    """
    Validates a plan against the FDC FSM definition.
    """
    try:
        with open(FSM_DEF_PATH, 'r') as f:
            fsm = json.load(f)
    except FileNotFoundError:
        print(f"Error: FSM definition not found at {FSM_DEF_PATH}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: FSM definition at {FSM_DEF_PATH} is not valid JSON.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(plan_filepath, 'r') as f:
            plan_actions = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Plan file not found at {plan_filepath}", file=sys.stderr)
        sys.exit(1)

    current_state = fsm["start_state"]
    print(f"Starting validation in state: {current_state}")

    for i, action in enumerate(plan_actions):
        print(f"Step {i+1}: Action '{action}'")

        # The action key is the entire line from the plan file.
        action_key = action

        if action_key not in fsm["alphabet"]:
            print(f"Error on line {i+1}: Action '{action_key}' is not in the FSM alphabet.", file=sys.stderr)
            sys.exit(1)

        transitions = fsm["transitions"].get(current_state)
        if not transitions or action_key not in transitions:
            print(f"Error on line {i+1}: Invalid transition. Cannot perform action '{action_key}' from state '{current_state}'.", file=sys.stderr)
            sys.exit(1)

        next_state = transitions[action_key]
        print(f"  Transition: {current_state} -> {next_state}")
        current_state = next_state

    if current_state in fsm["accept_states"]:
        print(f"\nValidation successful! Plan ends in accepted state: {current_state}")
    else:
        print(f"\nValidation failed. Plan ends in non-accepted state: '{current_state}'", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function for the FDC CLI tool."""
    parser = argparse.ArgumentParser(description="A tool to manage the Finite Development Cycle (FDC).")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # 'close' subcommand
    close_parser = subparsers.add_parser("close", help="Closes a task, initiating the post-mortem process.")
    close_parser.add_argument("--task-id", required=True, help="The unique identifier for the task being closed.")

    # 'validate' subcommand
    validate_parser = subparsers.add_parser("validate", help="Validates a plan file against the FDC FSM.")
    validate_parser.add_argument("plan_file", help="The path to the plan file to validate.")

    args = parser.parse_args()

    if args.command == "close":
        close_task(args.task_id)
    elif args.command == "validate":
        validate_plan(args.plan_file)
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()