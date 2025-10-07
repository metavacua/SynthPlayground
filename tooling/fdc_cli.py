import argparse
import datetime
import json
import os
import shutil
import sys
import uuid
import re

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POSTMORTEM_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'postmortem.md')
POSTMORTEMS_DIR = os.path.join(ROOT_DIR, 'postmortems')
LOG_FILE_PATH = os.path.join(ROOT_DIR, 'logs', 'activity.log.jsonl')
FSM_DEF_PATH = os.path.join(ROOT_DIR, 'tooling', 'fdc_fsm.json')

ACTION_TYPE_MAP = {
    "set_plan": "plan_op",
    "plan_step_complete": "step_op",
    "submit": "submit_op",
    "create_file_with_block": "write_op",
    "overwrite_file_with_block": "write_op",
    "replace_with_git_merge_diff": "write_op",
    "read_file": "read_op",
    "list_files": "read_op",
    "grep": "read_op",
    "delete_file": "delete_op",
    "rename_file": "move_op",
    "run_in_bash_session": "tool_exec",
    "for_each_file": "loop_op"
}

# --- Helper Functions ---
def _log_event(log_entry):
    """Appends a new log entry to the activity log, ensuring it's on a new line."""
    content_to_write = json.dumps(log_entry) + '\n'
    with open(LOG_FILE_PATH, 'a+') as f:
        f.seek(0, os.SEEK_END)
        if f.tell() > 0:
            f.seek(f.tell() - 1)
            if f.read(1) != '\n':
                f.write('\n')
        f.write(content_to_write)

def _create_log_entry(task_id, action_type, details):
    """Creates a structured log entry dictionary."""
    return {
        "log_id": str(uuid.uuid4()),
        "session_id": os.getenv("JULES_SESSION_ID", "unknown"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "Phase 6", "task": {"id": task_id, "plan_step": -1},
        "action": {"type": action_type, "details": details},
        "outcome": {"status": "SUCCESS", "message": f"FDC CLI: {action_type} for task {task_id}."}
    }

def _validate_action(line_num, line_content, state, fsm, fs, placeholders):
    """Validates a single, non-loop action."""
    for key, val in placeholders.items():
        line_content = line_content.replace(key, val)

    parts = line_content.split()
    command = parts[0]
    args = parts[1:]

    action_type = ACTION_TYPE_MAP.get(command)
    if command == "run_in_bash_session" and "close" in args:
        action_type = "close_op"

    if not action_type:
        print(f"Error on line {line_num+1}: Unknown command '{command}'.", file=sys.stderr)
        sys.exit(1)

    transitions = fsm["transitions"].get(state)
    if not transitions or action_type not in transitions:
        print(f"Error on line {line_num+1}: Invalid FSM transition. Cannot perform '{action_type}' from state '{state}'.", file=sys.stderr)
        sys.exit(1)

    if command == "create_file_with_block" and args[0] in fs:
        print(f"Error on line {line_num+1}: Semantic error. Cannot create '{args[0]}' because it already exists.", file=sys.stderr); sys.exit(1)
    if command in ["read_file", "delete_file", "replace_with_git_merge_diff"] and args[0] not in fs:
        print(f"Error on line {line_num+1}: Semantic error. Cannot access '{args[0]}' because it does not exist.", file=sys.stderr); sys.exit(1)

    if command == "create_file_with_block": fs.add(args[0])
    if command == "overwrite_file_with_block": fs.add(args[0])
    if command == "delete_file": fs.remove(args[0])
    if command == "rename_file": fs.remove(args[0]); fs.add(args[1])

    next_state = transitions[action_type]
    print(f"  Line {line_num+1}: OK. Action '{command}' ({action_type}) transitions from {state} -> {next_state}")
    return next_state, fs

def _validate_plan_recursive(lines, start_index, indent_level, state, fs, placeholders, fsm):
    """Recursively validates a block of a plan."""
    i = start_index
    while i < len(lines):
        line_num, line_content_raw = lines[i]
        line_content = line_content_raw.strip()

        if not line_content or line_content.startswith('#'):
            i += 1
            continue

        current_indent = len(line_content_raw) - len(line_content_raw.lstrip(' '))
        if current_indent < indent_level: return state, fs, i
        if current_indent > indent_level: print(f"Error on line {line_num+1}: Unexpected indentation.", file=sys.stderr); sys.exit(1)

        command = line_content.split()[0]
        if command == "for_each_file":
            loop_depth = len(placeholders) + 1
            placeholder_key = f"{{file{loop_depth}}}"
            dummy_file = f"dummy_file_for_loop_{loop_depth}"

            loop_body_start = i + 1
            j = loop_body_start
            while j < len(lines) and (len(lines[j][1]) - len(lines[j][1].lstrip(' '))) > indent_level: j += 1

            loop_fs = fs.copy()
            loop_fs.add(dummy_file)
            new_placeholders = placeholders.copy()
            new_placeholders[placeholder_key] = dummy_file

            state, loop_fs, _ = _validate_plan_recursive(lines, loop_body_start, indent_level + 2, state, loop_fs, new_placeholders, fsm)

            fs.update(loop_fs)
            i = j
        else:
            state, fs = _validate_action(line_num, line_content, state, fsm, fs, placeholders)
            i += 1

    return state, fs, i

# --- CLI Subcommands ---

def close_task(task_id):
    """Automates the closing of a Finite Development Cycle."""
    if not task_id: print("Error: --task-id is required.", file=sys.stderr); sys.exit(1)
    safe_task_id = "".join(c for c in task_id if c.isalnum() or c in ('-', '_'))
    new_path = os.path.join(POSTMORTEMS_DIR, f"{datetime.date.today()}-{safe_task_id}.md")
    try:
        shutil.copyfile(POSTMORTEM_TEMPLATE_PATH, new_path)
        print(f"Successfully created new post-mortem file: {new_path}")
    except Exception as e:
        print(f"Error creating post-mortem file: {e}", file=sys.stderr); sys.exit(1)
    _log_event(_create_log_entry(task_id, "POST_MORTEM", {"summary": f"Post-mortem initiated for '{task_id}'."}))
    _log_event(_create_log_entry(task_id, "TASK_END", {"summary": f"Development phase for FDC task '{task_id}' formally closed."}))
    print(f"Logged POST_MORTEM and TASK_END events for task: {task_id}")

def validate_plan(plan_filepath):
    """Validates a plan for both syntactic (FSM) and semantic (file state) correctness."""
    try:
        with open(FSM_DEF_PATH, 'r') as f: fsm = json.load(f)
        with open(plan_filepath, 'r') as f: lines = [(i, line) for i, line in enumerate(f)]
    except FileNotFoundError as e: print(f"Error: Could not find file {e.filename}", file=sys.stderr); sys.exit(1)

    simulated_fs = set()
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs: dirs.remove('.git')
        for name in files: simulated_fs.add(os.path.join(root, name).replace('./', ''))

    print(f"Starting validation with {len(simulated_fs)} files pre-loaded...")
    final_state, _, _ = _validate_plan_recursive(lines, 0, 0, fsm["start_state"], simulated_fs, {}, fsm)

    if final_state in fsm["accept_states"]:
        print(f"\nValidation successful! Plan is syntactically and semantically valid.")
    else:
        print(f"\nValidation failed. Plan ends in non-accepted state: '{final_state}'", file=sys.stderr); sys.exit(1)

def analyze_plan(plan_filepath):
    """Analyzes a plan file to determine its complexity, modality, and value."""
    try:
        with open(plan_filepath, 'r') as f: content = f.read()
        plan_lines_with_indent = content.splitlines()
        plan_lines = [line.strip() for line in plan_lines_with_indent if line.strip()]
    except FileNotFoundError: print(f"Error: Plan file not found at {plan_filepath}", file=sys.stderr); sys.exit(1)

    value = "Undefined"
    meta_match = re.search(r'# META\n# value: (.*?)\n# END META', content, re.DOTALL)
    if meta_match: value = meta_match.group(1).strip()

    loop_indents = [len(line) - len(line.lstrip(' ')) for line in plan_lines_with_indent if line.strip().startswith("for_each_file")]
    if not loop_indents:
        complexity = "Constant (O(1))"
    else:
        is_nested = any(indent > min(loop_indents) for indent in loop_indents)
        if is_nested:
            complexity = "Exponential (EXPTIME-Class)"
        else:
            complexity = "Polynomial (P-Class)"

    write_ops = {"write_op", "delete_op", "move_op"}
    has_write_op = any(ACTION_TYPE_MAP.get(line.split()[0]) in write_ops for line in plan_lines if not line.startswith("#") and not line.startswith("for_each_file"))
    modality = "Construction (Read-Write)" if has_write_op else "Analysis (Read-Only)"

    print(f"Plan Analysis Results:\n  - Complexity: {complexity}\n  - Modality:   {modality}\n  - Value:      {value}")

def main():
    """Main function for the FDC CLI tool."""
    parser = argparse.ArgumentParser(description="A tool to manage the Finite Development Cycle (FDC).")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    close_parser = subparsers.add_parser("close", help="Closes a task, initiating the post-mortem process.")
    close_parser.add_argument("--task-id", required=True, help="The unique identifier for the task.")

    validate_parser = subparsers.add_parser("validate", help="Validates a plan file against the FDC FSM.")
    validate_parser.add_argument("plan_file", help="The path to the plan file to validate.")

    analyze_parser = subparsers.add_parser("analyze", help="Analyzes a plan to determine its properties.")
    analyze_parser.add_argument("plan_file", help="The path to the plan file to analyze.")

    args = parser.parse_args()
    if args.command == "close": close_task(args.task_id)
    elif args.command == "validate": validate_plan(args.plan_file)
    elif args.command == "analyze": analyze_plan(args.plan_file)

if __name__ == "__main__":
    main()