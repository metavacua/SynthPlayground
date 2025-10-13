"""
A streamlined command-line tool for validating plan files against a
Finite State Machine (FSM) definition.

This script is a critical part of the agent's development protocol, used by the
`MasterControlGraph` to validate plan content before execution. It is the sole
remaining component of the original `fdc_cli.py` after the refactoring to an
API-driven architecture.

The script takes a single argument: the path to a plan file. It then:
1.  Parses the plan into a sequence of commands.
2.  Reads an FSM definition, potentially switching FSMs if the plan contains
    a `# FSM:` directive.
3.  Simulates the execution of the plan against the FSM, ensuring all state
    transitions are valid.
4.  Exits with a status code of 0 for a valid plan and 1 for an invalid plan.
"""
import argparse
import json
import os
import sys

# Add tooling directory to path to import other tools
sys.path.insert(0, "./tooling")
from plan_parser import parse_plan, Command

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_FSM_PATH = os.path.join(ROOT_DIR, "tooling", "fsm.json")
MAX_RECURSION_DEPTH = 10  # Safety limit for hierarchical plans

# Maps tool names to the action types defined in the FSM
ACTION_TYPE_MAP = {
    "set_plan": "plan_op",
    "message_user": "step_op",
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
    "call_plan": "call_plan_op",
}


def _validate_command(command: Command, state: str, fsm: dict) -> str:
    """
    Validates a single command against the FSM and returns the next state.
    """
    tool_name = command.tool_name
    action_type = ACTION_TYPE_MAP.get(tool_name)

    if not action_type:
        print(f"Error: Unknown command '{tool_name}' in plan.", file=sys.stderr)
        sys.exit(1)

    # Find the transition for the current state and action
    transitions = next((t for t in fsm["transitions"] if t["source"] == state), None)
    if not transitions:
        print(f"Error: No transitions found for state '{state}'.", file=sys.stderr)
        sys.exit(1)

    # The trigger in the FSM corresponds to the action type
    next_state = next((t["dest"] for t in fsm["transitions"] if t["source"] == state and t["trigger"] == action_type), None)

    if not next_state:
        # Let's try to find a trigger that matches the command name
        next_state = next((t["dest"] for t in fsm["transitions"] if t["source"] == state and t["trigger"] == tool_name), None)

    if not next_state:
        # Let's try to find a trigger that is a prefix of the action type
        for t in fsm["transitions"]:
            if t["source"] == state and action_type.startswith(t["trigger"]):
                next_state = t["dest"]
                break

    if not next_state:
        print(
            f"Error: Invalid FSM transition. Cannot perform action '{action_type}' (from tool '{tool_name}') from state '{state}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"  OK: '{tool_name}' ({action_type}) transitions from {state} -> {next_state}")
    return next_state


def validate_plan(plan_filepath: str):
    """
    Validates a plan file against the appropriate FSM.
    """
    try:
        with open(plan_filepath, "r") as f:
            plan_content = f.read()
    except FileNotFoundError:
        print(f"Error: Plan file not found at '{plan_filepath}'", file=sys.stderr)
        sys.exit(1)

    # --- FSM Loading ---
    fsm_path = DEFAULT_FSM_PATH
    first_line = plan_content.lstrip().split("\n", 1)[0]
    if first_line.startswith("# FSM:"):
        fsm_path_rel = first_line.split(":", 1)[1].strip()
        fsm_path = os.path.join(ROOT_DIR, fsm_path_rel)
        print(f"  - Detected FSM directive. Using FSM: {fsm_path_rel}")

    try:
        with open(fsm_path, "r") as f:
            fsm = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not load FSM from '{fsm_path}'. {e}", file=sys.stderr)
        sys.exit(1)

    # --- Plan Parsing and Validation ---
    commands = parse_plan(plan_content)
    if not commands:
        print("Warning: Plan is empty or contains only comments.", file=sys.stderr)
        # An empty plan is considered valid.
        print("\nValidation successful! (Empty Plan)")
        return

    current_state = fsm["initial_state"]
    print(f"Starting validation with initial state: '{current_state}'")

    for command in commands:
        # The 'call_plan' directive is handled by the executor, not the validator.
        # For validation purposes, we assume it's a valid step but don't change state.
        if command.tool_name == "call_plan":
            print(f"  OK: 'call_plan' is a meta-directive, skipping state transition.")
            continue
        current_state = _validate_command(command, current_state, fsm)

    # --- Final State Check ---
    if current_state in fsm["final_states"]:
        print(f"\nValidation successful! Plan ends in accepted state: '{current_state}'")
    else:
        print(f"\nValidation failed. Plan ends in non-accepted state: '{current_state}'", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the FDC CLI."""
    parser = argparse.ArgumentParser(
        description="Validate a plan file against the FDC Finite State Machine."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validates a plan file against the FDC FSM."
    )
    validate_parser.add_argument(
        "plan_file", help="The path to the plan file to validate."
    )

    args = parser.parse_args()

    if args.command == "validate":
        validate_plan(args.plan_file)


if __name__ == "__main__":
    main()
