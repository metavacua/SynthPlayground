import argparse
import sys
import os
import datetime
import json
import shutil
import uuid

# Adjusting the path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.tooling.master_control import MasterControlGraph
from src.tooling.lib.plan_analyzer import analyze_plan

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
POSTMORTEM_TEMPLATE_PATH = os.path.join(ROOT_DIR, "postmortem.md")
POSTMORTEMS_DIR = os.path.join(ROOT_DIR, "postmortems")
LOG_FILE_PATH = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
FSM_DEF_PATH = os.path.join(ROOT_DIR, "src/tooling", "fdc_fsm.json")

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
    "for_each_file": "loop_op",
    "define_set_of_names": "define_names_op",
    "define_diagonalization_function": "define_diag_op",
}

# --- FDC Functions ---

def _log_event(log_entry):
    """Appends a new log entry to the activity log, ensuring it's on a new line."""
    content_to_write = json.dumps(log_entry) + "\n"
    with open(LOG_FILE_PATH, "a+") as f:
        # Check if the file is not empty
        f.seek(0, os.SEEK_END)
        if f.tell() > 0:
            # Check if the last character is a newline
            f.seek(f.tell() - 1)
            if f.read(1) != "\n":
                f.write("\n")
        f.write(content_to_write)


def _create_log_entry(task_id, action_type, details):
    """Creates a structured log entry dictionary."""
    return {
        "log_id": str(uuid.uuid4()),
        "session_id": os.getenv("JULES_SESSION_ID", "unknown"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "Phase 6",
        "task": {"id": task_id, "plan_step": -1},
        "action": {"type": action_type, "details": details},
        "outcome": {
            "status": "SUCCESS",
            "message": f"FDC CLI: {action_type} for task {task_id}.",
        },
    }


def close_task(task_id):
    """Automates the closing of a Finite Development Cycle."""
    if not task_id:
        print("Error: --task-id is required.", file=sys.stderr)
        sys.exit(1)
    safe_task_id = "".join(c for c in task_id if c.isalnum() or c in ("-", "_"))
    new_path = os.path.join(
        POSTMORTEMS_DIR, f"{datetime.date.today()}-{safe_task_id}.md"
    )
    try:
        shutil.copyfile(POSTMORTEM_TEMPLATE_PATH, new_path)
        print(f"Successfully created new post-mortem file: {new_path}")
    except Exception as e:
        print(f"Error creating post-mortem file: {e}", file=sys.stderr)
        sys.exit(1)

    _log_event(
        _create_log_entry(
            task_id,
            "POST_MORTEM",
            {"summary": f"Post-mortem initiated for '{task_id}'."},
        )
    )
    _log_event(
        _create_log_entry(
            task_id,
            "TASK_END",
            {"summary": f"Development phase for FDC task '{task_id}' formally closed."},
        )
    )

    print(f"Logged POST_MORTEM and TASK_END events for task: {task_id}")


def _validate_action(line_num, line_content, state, fsm, fs, placeholders):
    """Validates a single, non-loop action."""
    # Substitute placeholders like {file1}, {file2}
    for key, val in placeholders.items():
        line_content = line_content.replace(key, val)

    parts = line_content.split()
    command = parts[0]
    args = parts[1:]
    action_type = ACTION_TYPE_MAP.get(command)
    if command == "run_in_bash_session" and "close" in args:
        action_type = "close_op"
    if not action_type:
        print(
            f"Error on line {line_num+1}: Unknown command '{command}'.", file=sys.stderr
        )
        sys.exit(1)

    # Syntactic check
    transitions = fsm["transitions"].get(state)
    if action_type not in (transitions or {}):
        print(
            f"Error on line {line_num+1}: Invalid FSM transition. Cannot perform '{action_type}' from state '{state}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Semantic check
    if command == "create_file_with_block" and args[0] in fs:
        print(
            f"Error on line {line_num+1}: Semantic error. Cannot create '{args[0]}' because it already exists.",
            file=sys.stderr,
        )
        sys.exit(1)
    if (
        command in ["read_file", "delete_file", "replace_with_git_merge_diff"]
        and args[0] not in fs
    ):
        print(
            f"Error on line {line_num+1}: Semantic error. Cannot access '{args[0]}' because it does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Apply state changes
    if command == "create_file_with_block":
        fs.add(args[0])
    if command == "delete_file":
        fs.remove(args[0])

    next_state = transitions[action_type]
    print(
        f"  Line {line_num+1}: OK. Action '{command}' ({action_type}) transitions from {state} -> {next_state}"
    )
    return next_state, fs


def _validate_plan_recursive(
    lines, start_index, indent_level, state, fs, placeholders, fsm
):
    """Recursively validates a block of a plan."""
    i = start_index
    while i < len(lines):
        line_num, line_content = lines[i]
        current_indent = len(line_content) - len(line_content.lstrip(" "))

        if current_indent < indent_level:
            return state, fs, i  # End of current block
        if current_indent > indent_level:
            print(
                f"Error on line {line_num+1}: Unexpected indentation.", file=sys.stderr
            )
            sys.exit(1)

        line_content = line_content.strip()
        command = line_content.split()[0]

        if command == "for_each_file":
            loop_depth = len(placeholders) + 1
            placeholder_key = f"file{loop_depth}"
            dummy_file = f"dummy_file_for_loop_{loop_depth}"

            # Find loop body
            loop_body_start = i + 1
            j = loop_body_start
            while (
                j < len(lines)
                and (len(lines[j][1]) - len(lines[j][1].lstrip(" "))) > indent_level
            ):
                j += 1

            # Validate one logical iteration of the.
            loop_fs = fs.copy()
            loop_fs.add(dummy_file)
            new_placeholders = placeholders.copy()
            new_placeholders[placeholder_key] = dummy_file

            state, loop_fs, _ = _validate_plan_recursive(
                lines,
                loop_body_start,
                indent_level + 2,
                state,
                loop_fs,
                new_placeholders,
                fsm,
            )

            fs.update(loop_fs)  # Merge FS changes
            i = j
        else:
            state, fs = _validate_action(
                line_num, line_content, state, fsm, fs, placeholders
            )
            i += 1

    return state, fs, i


from src.tooling.lib.plan_validator import validate_plan


def start_task(task_id):
    """Initiates the AORP cascade for a new task."""
    if not task_id:
        print("Error: --task-id is required.", file=sys.stderr)
        sys.exit(1)

    print("--- FDC: Initiating Advanced Orientation and Research Protocol (AORP) ---")
    print(f"--- Task ID: {task_id} ---")

    # --- L1: Self-Awareness & Identity Verification ---
    print("\n--- L1: Self-Awareness & Identity Verification ---")
    try:
        with open(os.path.join(ROOT_DIR, "knowledge_core", "agent_meta.json"), "r") as f:
            agent_meta = json.load(f)
            print("Successfully loaded knowledge_core/agent_meta.json:")
            print(json.dumps(agent_meta, indent=2))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error during L1: Could not read or parse agent_meta.json. {e}", file=sys.stderr)
        sys.exit(1)

    # --- L2: Repository State Synchronization ---
    print("\n--- L2: Repository State Synchronization ---")
    try:
        kc_path = os.path.join(ROOT_DIR, "knowledge_core")
        artifacts = [f for f in os.listdir(kc_path) if os.path.isfile(os.path.join(kc_path, f)) and f != 'agent_meta.json']
        print("Found knowledge_core artifacts:")
        for artifact in artifacts:
            print(f"- {artifact}")
    except FileNotFoundError as e:
        print(f"Error during L2: Could not list knowledge_core directory. {e}", file=sys.stderr)
        sys.exit(1)

    # --- L3: Environmental Probing ---
    print("\n--- L3: Environmental Probing ---")
    probe_script_path = os.path.join(ROOT_DIR, "src/tooling", "environmental_probe.py")
    if not os.path.exists(probe_script_path):
        print(f"Error during L3: Probe script not found at {probe_script_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Executing: python3 {probe_script_path}")
    # We are already running in a bash session, so we can just run the script
    # and it will inherit the environment.
    os.system(f"python3 {probe_script_path}")


    # --- Logging ---
    _log_event(
        _create_log_entry(
            task_id,
            "TASK_START",
            {"summary": f"AORP cascade completed for FDC task '{task_id}'."},
        )
    )
    print(f"\n--- AORP Complete. Logged TASK_START event for task: {task_id} ---")

# --- CSDC Functions ---

def validate_csdc_plan(plan_file, model, complexity):
    """Validates a plan against the CSDC constraints."""
    print(f"--- CSDC: Analyzing plan '{plan_file}' ---")
    analysis_results = analyze_plan(plan_file, return_results=True)

    if analysis_results["complexity_class"] != complexity:
        print(
            f"Error: Plan complexity mismatch. Expected '{complexity}', but found '{analysis_results['complexity_class']}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Complexity check passed: Plan is in class {analysis_results['complexity_class']}.")

    print(f"\n--- CSDC: Validating plan against Model {model} ---")

    try:
        with open(plan_file, "r") as f:
            plan_content = f.read()
    except FileNotFoundError:
        print(f"Error: Plan file not found at {plan_file}", file=sys.stderr)
        sys.exit(1)

    validator = MasterControlGraph()
    is_valid, error_message = validator.validate_plan_for_model(plan_content, model)

    if is_valid:
        print("\nValidation successful! Plan is valid for the specified model and complexity.")
    else:
        print(f"\nValidation failed: {error_message}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="A unified CLI for managing the agent's development and execution cycles."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )

    # --- FDC Subcommand ---
    fdc_parser = subparsers.add_parser(
        "fdc", help="Manage the Finite Development Cycle (FDC)."
    )
    fdc_subparsers = fdc_parser.add_subparsers(
        dest="fdc_command", help="FDC subcommands", required=True
    )
    fdc_start_parser = fdc_subparsers.add_parser(
        "start", help="Starts a task, initiating the AORP cascade."
    )
    fdc_start_parser.add_argument(
        "--task-id", required=True, help="The unique identifier for the task."
    )
    fdc_close_parser = fdc_subparsers.add_parser(
        "close", help="Closes a task, initiating the post-mortem process."
    )
    fdc_close_parser.add_argument(
        "--task-id", required=True, help="The unique identifier for the task."
    )
    fdc_validate_parser = fdc_subparsers.add_parser(
        "validate", help="Validates a plan file against the FDC FSM."
    )
    fdc_validate_parser.add_argument(
        "plan_file", help="The path to the plan file to validate."
    )
    fdc_analyze_parser = fdc_subparsers.add_parser(
        "analyze", help="Analyzes a plan to determine its complexity class."
    )
    fdc_analyze_parser.add_argument(
        "plan_file", help="The path to the plan file to analyze."
    )

    # --- CSDC Subcommand ---
    csdc_parser = subparsers.add_parser(
        "csdc", help="Manage the Context-Sensitive Development Cycle (CSDC)."
    )
    csdc_parser.add_argument(
        "plan_file", help="The path to the plan file to validate."
    )
    csdc_parser.add_argument(
        "--model",
        required=True,
        choices=["A", "B"],
        help="The development model to use for validation (A or B).",
    )
    csdc_parser.add_argument(
        "--complexity",
        required=True,
        choices=["P", "EXP"],
        help="The expected complexity class of the plan (P for Polynomial, EXP for Exponential).",
    )

    # --- Master Control Subcommand ---
    master_control_parser = subparsers.add_parser(
        "mc", help="Interact with the Master Control loop."
    )
    master_control_parser.add_argument(
        "task",
        type=str,
        help="The high-level task for the agent to accomplish.",
    )

    args = parser.parse_args()

    if args.command == "fdc":
        if args.fdc_command == "start":
            start_task(args.task_id)
        elif args.fdc_command == "close":
            close_task(args.task_id)
        elif args.fdc_command == "validate":
            validate_plan(args.plan_file)
        elif args.fdc_command == "analyze":
            analyze_plan(args.plan_file)
    elif args.command == "csdc":
        validate_csdc_plan(args.plan_file, args.model, args.complexity)
    elif args.command == "mc":
        from src.tooling.agent_shell import run_agent_loop
        print("--- Invoking Agent Shell ---")
        final_state = run_agent_loop(task_description=args.task)
        print("\n--- Final State ---")
        print(json.dumps(final_state.to_json(), indent=2))
        print("--- Workflow Complete ---")


if __name__ == "__main__":
    main()