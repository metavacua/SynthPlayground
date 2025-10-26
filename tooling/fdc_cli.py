"""
This script provides a command-line interface (CLI) for managing the Finite
Development Cycle (FDC).

The FDC is a structured workflow for agent-driven software development. This CLI
is the primary human interface for interacting with that cycle, providing
commands to:
- **start:** Initiates a new development task, triggering the "Advanced
  Orientation and Research Protocol" (AORP) to ensure the agent is fully
  contextualized.
- **close:** Formally concludes a task, creating a post-mortem template for
  analysis and lesson-learning.
- **validate:** Checks a given plan file for both syntactic and semantic
  correctness against the FDC's governing Finite State Machine (FSM). This
  ensures that a plan is executable and will not violate protocol.
- **analyze:** Examines a plan to determine its computational complexity (e.g.,
  Constant, Polynomial, Exponential) and its modality (Read-Only vs.
  Read-Write), providing insight into the plan's potential impact.
"""

import argparse
import datetime
import json
import os
import shutil
import sys
import uuid

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.file_system_utils import find_files
from tooling.fdc_cli_logic import create_log_entry, analyze_plan_content

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTMORTEM_TEMPLATE_PATH = os.path.join(ROOT_DIR, "postmortem.md")
POSTMORTEMS_DIR = os.path.join(ROOT_DIR, "postmortems")
LOG_FILE_PATH = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
FSM_DEF_PATH = os.path.join(ROOT_DIR, "tooling", "fdc_fsm.json")


# --- CLI Subcommands & Helpers ---


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
        create_log_entry(
            task_id,
            "POST_MORTEM",
            {"summary": f"Post-mortem initiated for '{task_id}'."},
        )
    )
    _log_event(
        create_log_entry(
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
            placeholder_key = f"{{file{loop_depth}}}"
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


def validate_plan(plan_filepath):
    try:
        with open(FSM_DEF_PATH, "r") as f:
            fsm = json.load(f)
        with open(plan_filepath, "r") as f:
            lines = [(i, line.rstrip("\n")) for i, line in enumerate(f) if line.strip()]
    except FileNotFoundError as e:
        print(f"Error: Could not find file {e.filename}", file=sys.stderr)
        sys.exit(1)

    # Initialize the simulated file system with the actual state of the repository
    simulated_fs = set(find_files("*"))

    print(f"Starting validation with {len(simulated_fs)} files pre-loaded...")
    final_state, _, _ = _validate_plan_recursive(
        lines, 0, 0, fsm["start_state"], simulated_fs, {}, fsm
    )

    if final_state in fsm["accept_states"]:
        print("\nValidation successful! Plan is syntactically and semantically valid.")
    else:
        print(
            f"\nValidation failed. Plan ends in non-accepted state: '{final_state}'",
            file=sys.stderr,
        )
        sys.exit(1)


def analyze_plan(plan_filepath, return_results=False):
    """Analyzes a plan file to determine its complexity class and modality."""
    try:
        with open(plan_filepath, "r") as f:
            plan_lines_with_indent = f.readlines()
    except FileNotFoundError:
        print(f"Error: Plan file not found at {plan_filepath}", file=sys.stderr)
        sys.exit(1)

    analysis_results = analyze_plan_content(plan_lines_with_indent)

    if return_results:
        return analysis_results

    print("Plan Analysis Results:")
    print(f"  - Complexity: {analysis_results['complexity_string']}")
    print(f"  - Modality:   {analysis_results['modality']}")


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
        with open(
            os.path.join(ROOT_DIR, "knowledge_core", "agent_meta.json"), "r"
        ) as f:
            agent_meta = json.load(f)
            print("Successfully loaded knowledge_core/agent_meta.json:")
            print(json.dumps(agent_meta, indent=2))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(
            f"Error during L1: Could not read or parse agent_meta.json. {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- L2: Repository State Synchronization ---
    print("\n--- L2: Repository State Synchronization ---")
    try:
        kc_path = os.path.join(ROOT_DIR, "knowledge_core")
        artifacts = find_files("*", base_dir=kc_path)
        artifacts = [f for f in artifacts if os.path.basename(f) != "agent_meta.json"]
        print("Found knowledge_core artifacts:")
        for artifact in artifacts:
            print(f"- {os.path.basename(artifact)}")
    except FileNotFoundError as e:
        print(
            f"Error during L2: Could not list knowledge_core directory. {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- L3: Environmental Probing ---
    print("\n--- L3: Environmental Probing ---")
    probe_script_path = os.path.join(ROOT_DIR, "tooling", "environmental_probe.py")
    if not os.path.exists(probe_script_path):
        print(
            f"Error during L3: Probe script not found at {probe_script_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Executing: python3 {probe_script_path}")
    # We are already running in a bash session, so we can just run the script
    # and it will inherit the environment.
    os.system(f"python3 {probe_script_path}")

    # --- Logging ---
    _log_event(
        create_log_entry(
            task_id,
            "TASK_START",
            {"summary": f"AORP cascade completed for FDC task '{task_id}'."},
        )
    )
    print(f"\n--- AORP Complete. Logged TASK_START event for task: {task_id} ---")


def main():
    parser = argparse.ArgumentParser(
        description="A tool to manage the Finite Development Cycle (FDC)."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )

    start_parser = subparsers.add_parser(
        "start", help="Starts a task, initiating the AORP cascade."
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

    args = parser.parse_args()
    if args.command == "start":
        start_task(args.task_id)
    elif args.command == "close":
        close_task(args.task_id)
    elif args.command == "validate":
        validate_plan(args.plan_file)
    elif args.command == "analyze":
        analyze_plan(args.plan_file)


if __name__ == "__main__":
    main()
