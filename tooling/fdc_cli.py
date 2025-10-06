import argparse
import datetime
import json
import os
import shutil
import sys
import uuid

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POSTMORTEM_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'postmortem.md')
POSTMORTEMS_DIR = os.path.join(ROOT_DIR, 'postmortems')
LOG_FILE_PATH = os.path.join(ROOT_DIR, 'logs', 'activity.log.jsonl')
FSM_DEF_PATH = os.path.join(ROOT_DIR, 'tooling', 'fdc_fsm.json')

# Maps specific tool commands to generic FSM action types
ACTION_TYPE_MAP = {
    "set_plan": "process_op",
    "plan_step_complete": "process_op",
    "submit": "process_op",
    "create_file_with_block": "write_op",
    "overwrite_file_with_block": "write_op",
    "replace_with_git_merge_diff": "write_op",
    "read_file": "read_op",
    "list_files": "read_op",
    "grep": "read_op",
    "delete_file": "delete_op",
    "rename_file": "move_op",
    "run_in_bash_session": "tool_exec",
    "fdc_cli.py": "tool_exec" # Simplified for tool execution
}

# --- Core Functions ---

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
        "phase": "Phase 6", "task": {"id": task_id, "plan_step": -1},
        "action": {"type": action_type, "details": details},
        "outcome": {"status": "SUCCESS", "message": f"FDC CLI: {action_type} executed for task {task_id}."}
    }

def close_task(task_id):
    """Automates the closing of a Finite Development Cycle."""
    if not task_id:
        print("Error: --task-id is required.", file=sys.stderr); sys.exit(1)

    today_str = datetime.date.today().strftime('%Y-%m-%d')
    safe_task_id = "".join(c for c in task_id if c.isalnum() or c in ('-', '_'))
    new_postmortem_filename = f"{today_str}-{safe_task_id}.md"
    new_postmortem_path = os.path.join(POSTMORTEMS_DIR, new_postmortem_filename)

    try:
        shutil.copyfile(POSTMORTEM_TEMPLATE_PATH, new_postmortem_path)
        print(f"Successfully created new post-mortem file: {new_postmortem_path}")
    except Exception as e:
        print(f"Error creating post-mortem file: {e}", file=sys.stderr); sys.exit(1)

    log_event(create_log_entry(task_id, "POST_MORTEM", {"summary": f"Post-mortem initiated for '{task_id}'."}))
    log_event(create_log_entry(task_id, "TASK_END", {"summary": f"Development phase for FDC task '{task_id}' formally closed."}))
    print(f"Logged POST_MORTEM and TASK_END events for task: {task_id}")
    print("\nFDC close process complete. Please fill out the post-mortem report.")

def validate_plan(plan_filepath):
    """Validates a plan for both syntactic (FSM) and semantic (file state) correctness."""
    try:
        with open(FSM_DEF_PATH, 'r') as f: fsm = json.load(f)
        with open(plan_filepath, 'r') as f: plan_actions = [line.strip() for line in f if line.strip()]
    except FileNotFoundError as e:
        print(f"Error: Could not find file {e.filename}", file=sys.stderr); sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: FSM definition at {FSM_DEF_PATH} is not valid JSON.", file=sys.stderr); sys.exit(1)

    current_state = fsm["start_state"]
    simulated_fs = set() # Stores paths of files that logically exist

    print(f"Starting validation in state: {current_state}")
    for i, line in enumerate(plan_actions):
        parts = line.split()
        command = parts[0]
        args = parts[1:]

        # Determine action type for FSM
        action_type = ACTION_TYPE_MAP.get(command)

        # Special handling for the close command when run via bash
        if command == "run_in_bash_session" and "tooling/fdc_cli.py" in args and "close" in args:
            action_type = "close_op"

        if not action_type:
            print(f"Error on line {i+1}: Unknown command '{command}'.", file=sys.stderr); sys.exit(1)

        # 1. Syntactic Validation (FSM)
        transitions = fsm["transitions"].get(current_state)
        if not transitions or action_type not in transitions:
            print(f"Error on line {i+1}: Invalid FSM transition. Cannot perform '{action_type}' from state '{current_state}'.", file=sys.stderr); sys.exit(1)

        # 2. Semantic Validation (File State)
        if command == "create_file_with_block":
            filepath = args[0]
            if filepath in simulated_fs:
                print(f"Error on line {i+1}: Semantic error. Cannot create '{filepath}' because it already exists.", file=sys.stderr); sys.exit(1)
            simulated_fs.add(filepath)
        elif command in ["read_file", "delete_file", "replace_with_git_merge_diff"]:
            filepath = args[0]
            if filepath not in simulated_fs:
                print(f"Error on line {i+1}: Semantic error. Cannot access '{filepath}' because it does not exist.", file=sys.stderr); sys.exit(1)
            if command == "delete_file":
                simulated_fs.remove(filepath)
        elif command == "rename_file":
            source, dest = args[0], args[1]
            if source not in simulated_fs:
                print(f"Error on line {i+1}: Semantic error. Cannot rename '{source}' because it does not exist.", file=sys.stderr); sys.exit(1)
            if dest in simulated_fs:
                print(f"Error on line {i+1}: Semantic error. Cannot rename to '{dest}' because it already exists.", file=sys.stderr); sys.exit(1)
            simulated_fs.remove(source)
            simulated_fs.add(dest)
        elif command == "overwrite_file_with_block":
             simulated_fs.add(args[0])


        next_state = transitions[action_type]
        print(f"  Step {i+1}: OK. Action '{command}' ({action_type}) transitions from {current_state} -> {next_state}")
        current_state = next_state

    if current_state in fsm["accept_states"]:
        print(f"\nValidation successful! Plan is both syntactically and semantically valid.")
    else:
        print(f"\nValidation failed. Plan ends in non-accepted state: '{current_state}'", file=sys.stderr); sys.exit(1)

def main():
    """Main function for the FDC CLI tool."""
    parser = argparse.ArgumentParser(description="A tool to manage the Finite Development Cycle (FDC).")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    close_parser = subparsers.add_parser("close", help="Closes a task, initiating the post-mortem process.")
    close_parser.add_argument("--task-id", required=True, help="The unique identifier for the task being closed.")

    validate_parser = subparsers.add_parser("validate", help="Validates a plan file against the FDC FSM.")
    validate_parser.add_argument("plan_file", help="The path to the plan file to validate.")

    args = parser.parse_args()

    if args.command == "close":
        close_task(args.task_id)
    elif args.command == "validate":
        validate_plan(args.plan_file)

if __name__ == "__main__":
    main()