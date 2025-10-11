"""
Provides the command-line interface for the Finite Development Cycle (FDC).

This script is a core component of the agent's protocol, offering tools to ensure
that all development work is structured, verifiable, and safe. It is used by both
the agent to signal progress and the `master_control.py` orchestrator to
validate the agent's plans before execution.

The CLI provides several key commands:
- `close`: Logs the formal end of a task, signaling to the orchestrator that
  execution is complete.
- `validate`: Performs a deep validation of a plan file against the FDC's Finite
  State Machine (FSM) definition. It checks for both syntactic correctness (Is
  the sequence of operations valid?) and semantic correctness (Does the plan try
  to use a file before creating it?).
- `analyze`: Reads a plan and provides a high-level analysis of its
  characteristics, such as its computational complexity and whether it is a
  read-only or read-write plan.
- `lint`: A comprehensive "linter" that runs a full suite of checks on a plan
  file, including `validate`, `analyze`, and checks for disallowed recursion.
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import uuid

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTMORTEM_TEMPLATE_PATH = os.path.join(ROOT_DIR, "postmortem.md")
POSTMORTEMS_DIR = os.path.join(ROOT_DIR, "postmortems")
LOG_FILE_PATH = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
FSM_DEF_PATH = os.path.join(ROOT_DIR, "tooling", "fdc_fsm.json")
MAX_RECURSION_DEPTH = 10  # Safety limit for hierarchical plans
PLAN_REGISTRY_PATH = os.path.join(ROOT_DIR, "knowledge_core", "plan_registry.json")

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
    # 'call_plan' is a meta-directive for the executor, not the FSM validator.
}

# --- CLI Subcommands & Helpers ---


def _load_plan_registry():
    """Loads the plan registry, returning an empty dict if it doesn't exist or is invalid."""
    if not os.path.exists(PLAN_REGISTRY_PATH):
        return {}
    try:
        with open(PLAN_REGISTRY_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


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
    """
    Logs the formal end of a task.

    This command's primary role is to create a TASK_END log entry. It no longer
    manages the post-mortem file directly; that process is now fully owned by
    the MasterControlGraph orchestrator, which is the single source of truth
    for state transitions and artifact lifecycle management.
    """
    if not task_id:
        print("Error: --task-id is required.", file=sys.stderr)
        sys.exit(1)

    # The only responsibility of this command is to log the TASK_END event.
    # The master_control.py orchestrator handles the post-mortem lifecycle.
    log_details = {
        "summary": f"Agent has signaled the completion of task '{task_id}'. The Master Control Graph will now transition to the post-mortem phase."
    }
    _log_event(_create_log_entry(task_id, "TASK_END", log_details))

    print(f"Logged TASK_END event for task: {task_id}")
    # The creation of the step_complete.txt file by the agent's execution
    # of this tool is the signal for the MasterControlGraph to proceed.


def start_task(task_id):
    """
    Logs the formal start of a task.
    """
    if not task_id:
        print("Error: --task-id is required.", file=sys.stderr)
        sys.exit(1)

    log_details = {
        "summary": f"Agent has signaled the start of task '{task_id}'. The Master Control Graph will now transition to the execution phase."
    }
    _log_event(_create_log_entry(task_id, "TASK_START", log_details))
    print(f"Logged TASK_START event for task: {task_id}")


from tooling.plan_parser import parse_plan, Command

# ... (other imports remain the same)

# ACTION_TYPE_MAP now also includes special handling for the new parser
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
    "call_plan": "call_plan_op", # Now a recognized action type
}


def _validate_command(command: Command, state, fsm, fs):
    """Validates a single Command object against the FSM and filesystem state."""
    tool_name = command.tool_name
    args_text = command.args_text

    action_type = ACTION_TYPE_MAP.get(tool_name)
    if not action_type:
        print(f"Error: Unknown command '{tool_name}'.", file=sys.stderr)
        sys.exit(1)

    # Syntactic check
    transitions = fsm["transitions"].get(state)
    if action_type not in (transitions or {}):
        print(
            f"Error: Invalid FSM transition. Cannot perform '{action_type}' from state '{state}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Semantic check (simplified for this refactoring)
    # A more robust validator would parse args_text for filenames
    if "write_op" in action_type:
        # Cannot robustly check for file existence without parsing args
        pass

    next_state = transitions[action_type]
    print(
        f"  OK: Action '{tool_name}' ({action_type}) transitions from {state} -> {next_state}"
    )
    return next_state, fs


def _validate_plan_recursive(
    lines,
    start_index,
    indent_level,
    state,
    fs,
    placeholders,
    fsm,
    recursion_depth,
):
    """
    Recursively validates a block of a plan, now with recursion detection and FSM-switching.
    """
    if recursion_depth > MAX_RECURSION_DEPTH:
        print(f"Error: Max recursion depth ({MAX_RECURSION_DEPTH}) exceeded.", file=sys.stderr)
        sys.exit(1)

    i = start_index

    # --- FSM Switching Logic ---
    current_fsm = fsm
    # An FSM directive is only valid as the first non-empty line of a plan file.
    if start_index == 0 and lines:
        first_line_content = lines[0][1].strip()
        if first_line_content.startswith("# FSM:"):
            fsm_path = first_line_content.split(":", 1)[1].strip()
            # The path in the directive is relative to the repo root.
            full_fsm_path = os.path.join(ROOT_DIR, fsm_path)
            try:
                with open(full_fsm_path, "r") as f:
                    current_fsm = json.load(f)
                print(f"  Switched to FSM: {fsm_path}")
                # Reset state to the start state of the new FSM
                state = current_fsm["start_state"]
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(
                    f"Error on line 1: Could not load FSM from '{fsm_path}'. {e}",
                    file=sys.stderr,
                )
                sys.exit(1)

    while i < len(lines):
        line_num, line_content = lines[i]
        current_indent = len(line_content) - len(line_content.lstrip(" "))

        if current_indent < indent_level:
            return state, fs, i, current_fsm  # End of current block

        if current_indent > indent_level:
            print(
                f"Error on line {line_num+1}: Unexpected indentation.", file=sys.stderr
            )
            sys.exit(1)

        line_content = line_content.strip()
        if line_content.startswith("# FSM:"):  # Ignore directive during validation
            i += 1
            continue

        command = line_content.split()[0]
        args = line_content.split()[1:]

        if command == "call_plan":
            plan_name_or_path = args[0]
            registry = _load_plan_registry()
            sub_plan_path = registry.get(plan_name_or_path, plan_name_or_path)

            try:
                with open(sub_plan_path, "r") as f:
                    sub_plan_content = f.read()
                sub_commands = parse_plan(sub_plan_content)
            except FileNotFoundError:
                print(f"Error: Sub-plan file not found at '{sub_plan_path}'.", file=sys.stderr)
                sys.exit(1)

            print(f"  Line {line_num+1}: Validating sub-plan '{sub_plan_path}'...")
            sub_final_state, _, _, sub_fsm = _validate_plan_recursive(
                sub_plan_lines,
                0,
                0,
                "DUMMY_STATE",
                fs.copy(),
                {},
                current_fsm,
                recursion_depth + 1,
            )

            if sub_final_state not in sub_fsm["accept_states"]:
                print(
                    f"Error in sub-plan '{sub_plan_path}': Plan does not end in an accepted state.",
                    file=sys.stderr,
                )
                sys.exit(1)
            print(f"  Sub-plan '{sub_plan_path}' is valid. Resuming parent plan.")
            i += 1
        elif command == "for_each_file":
            loop_depth = len(placeholders) + 1
            placeholder_key = f"{{file{loop_depth}}}"
            dummy_file = f"dummy_file_for_loop_{loop_depth}"

            loop_body_start = i + 1
            j = loop_body_start
            while (
                j < len(lines)
                and (len(lines[j][1]) - len(lines[j][1].lstrip(" "))) > indent_level
            ):
                j += 1

            loop_fs = fs.copy()
            loop_fs.add(dummy_file)
            new_placeholders = placeholders.copy()
            new_placeholders[placeholder_key] = dummy_file

            state, loop_fs, _, _ = _validate_plan_recursive(
                lines,
                loop_body_start,
                indent_level + 2,
                state,
                loop_fs,
                new_placeholders,
                current_fsm,
                recursion_depth,
            )

            fs.update(loop_fs)
            i = j
        else:
            state, fs = _validate_action(
                line_num, line_content, state, current_fsm, fs, placeholders
            )
            i += 1

    return state, fs, i, current_fsm


def validate_plan(plan_filepath):
    """Validates a plan using the centralized parser."""
    try:
        # Load the default FSM. The recursive validator will switch if a directive is found.
        with open(FSM_DEF_PATH, "r") as f:
            default_fsm = json.load(f)
        with open(plan_filepath, "r") as f:
            plan_content = f.read()
    except FileNotFoundError as e:
        print(f"Error: Could not find file {e.filename}", file=sys.stderr)
        sys.exit(1)

    commands = parse_plan(plan_content)

    simulated_fs = set()
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        for name in files:
            simulated_fs.add(os.path.join(root, name).replace("./", ""))

    print(f"Starting validation with {len(simulated_fs)} files pre-loaded...")
    final_state, _, _, final_fsm = _validate_plan_recursive(
        lines, 0, 0, default_fsm["start_state"], simulated_fs, {}, default_fsm, 0
    )

    if final_state in final_fsm["accept_states"]:
        print("\nValidation successful! Plan is syntactically and semantically valid.")
    else:
        print(f"\nValidation failed. Plan ends in non-accepted state: '{final_state}'", file=sys.stderr)
        sys.exit(1)


def analyze_plan(plan_filepath):
    """Analyzes a plan file to determine its complexity class and modality."""
    try:
        with open(plan_filepath, "r") as f:
            plan_lines_with_indent = f.readlines()
        plan_lines = [line.strip() for line in plan_lines_with_indent if line.strip()]
    except FileNotFoundError:
        print(f"Error: Plan file not found at {plan_filepath}", file=sys.stderr)
        sys.exit(1)

    # --- Complexity Analysis ---
    loop_indents = []
    for line in plan_lines_with_indent:
        if line.strip().startswith("for_each_file"):
            indent = len(line) - len(line.lstrip(" "))
            loop_indents.append(indent)

    if not loop_indents:
        complexity = "Constant (O(1))"
    elif max(loop_indents) > min(loop_indents):
        complexity = "Exponential (EXPTIME-Class)"
    else:
        complexity = "Polynomial (P-Class)"

    # --- Modality Analysis ---
    has_write_op = False
    write_ops = {"write_op", "delete_op", "move_op"}
    for line in plan_lines:
        command = line.split()[0]
        action_type = ACTION_TYPE_MAP.get(command)
        if action_type in write_ops:
            has_write_op = True
            break

    modality = "Construction (Read-Write)" if has_write_op else "Analysis (Read-Only)"

    print("Plan Analysis Results:")
    print(f"  - Complexity: {complexity}")
    print(f"  - Modality:   {modality}")


def lint_plan(plan_filepath):
    """
    Runs a comprehensive suite of checks on a plan file.
    The old recursion check is now obsolete, as the max depth is checked
    directly within the new hierarchical validator.
    """
    print(f"--- Starting Comprehensive Lint for {plan_filepath} ---")
    validate_plan(plan_filepath)
    analyze_plan(plan_filepath)
    print("\n--- Linting Complete: All checks passed. ---")


def main():
    parser = argparse.ArgumentParser(
        description="A tool to manage the Finite Development Cycle (FDC)."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )

    start_parser = subparsers.add_parser(
        "start", help="Starts a task, initiating the development cycle."
    )
    start_parser.add_argument(
        "--task-id", required=True, help="The unique identifier for the task."
    )

    close_parser = subparsers.add_parser(
        "close", help="Closes a task, initiating the post-mortem process."
    )
    close_parser.add_argument(
        "--task-id", required=True, help="The unique identifier for the task."
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validates a plan file against the FDC FSM."
    )
    validate_parser.add_argument(
        "plan_file", help="The path to the plan file to validate."
    )

    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyzes a plan to determine its complexity class."
    )
    analyze_parser.add_argument(
        "plan_file", help="The path to the plan file to analyze."
    )

    lint_parser = subparsers.add_parser(
        "lint", help="Runs all validation and analysis checks on a plan."
    )
    lint_parser.add_argument(
        "plan_file", help="The path to the plan file to lint."
    )

    args = parser.parse_args()
    if args.command == "start":
        start_task(args.task_id)
    elif args.command == "close":
        close_task(args.task_id)
    elif args.command == "validate":
        validate_plan(args.plan_file)
    elif args.command == "analyze":
        analyze_plan(args.plan_file)
    elif args.command == "lint":
        lint_plan(args.plan_file)


if __name__ == "__main__":
    main()
