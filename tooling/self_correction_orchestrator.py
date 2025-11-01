"""
Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.

This script is the engine of the automated feedback loop. It reads structured,
actionable lessons from `knowledge_core/lessons.jsonl` and uses the
`protocol_updater.py` tool to apply them to the source protocol files.
"""

import json
import os
import subprocess

LESSONS_FILE = "knowledge_core/lessons.jsonl"
UPDATER_SCRIPT = "tooling/protocol_updater.py"
CODE_SUGGESTER_SCRIPT = "tooling/code_suggester.py"


def load_lessons():
    """Loads all lessons from the JSONL file."""
    if not os.path.exists(LESSONS_FILE):
        return []

    with open(LESSONS_FILE, "r") as f:
        return [json.loads(line) for line in f]


def save_lessons(lessons):
    """Saves a list of lessons back to the JSONL file, overwriting it."""
    with open(LESSONS_FILE, "w") as f:
        for lesson in lessons:
            f.write(json.dumps(lesson) + "\n")


def run_command(command: list) -> bool:
    """Runs a command and returns True on success, False on failure."""
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Stderr: {e.stderr}")
        return False


def apply_merge_diff(filepath, merge_diff):
    """Applies a git-style merge diff to a file."""
    try:
        lines = merge_diff.split("\n")

        # A simple validation for the merge diff format
        if not (
            lines[0] == "<<<<<<< SEARCH"
            and "=======" in lines
            and lines[-1] == ">>>>>>> REPLACE"
        ):
            print("Error: Invalid merge diff format.")
            return False

        separator_index = lines.index("=======")
        search_block = "\n".join(lines[1:separator_index])
        replace_block = "\n".join(lines[separator_index + 1 : -1])

        with open(filepath, "r") as f:
            original_content = f.read()

        if search_block not in original_content:
            print(f"Error: Search block not found in {filepath}.")
            # For debugging, print what was expected vs what was found
            # print("Expected to find:\n---\n" + search_block + "\n---")
            return False

        new_content = original_content.replace(search_block, replace_block, 1)

        with open(filepath, "w") as f:
            f.write(new_content)

        print(f"Successfully applied patch to {filepath}")
        return True

    except Exception as e:
        print(f"An error occurred while applying merge diff: {e}")
        return False


def process_lessons(lessons: list, protocols_dir: str) -> bool:
    """
    Processes all pending lessons, applies them, and updates their status.
    Returns True if any changes were made, False otherwise.
    """
    changes_made = False
    for lesson in lessons:
        if lesson.get("status") != "pending":
            continue

        print(f"--- Processing pending lesson: {lesson['lesson_id']} ---")
        action = lesson.get("action", {})
        action_type = action.get("type")

        if action_type == "UPDATE_PROTOCOL":
            command_name = action.get("command")
            if not command_name:
                print(
                    f"Warning: Skipping lesson {lesson['lesson_id']} due to missing 'command' key in action."
                )
                continue

            params = action.get("parameters", {})
            command_executed = False

            if command_name == "add-tool":
                protocol_id = params.get("protocol_id")
                tool_name = params.get("tool_name")
                if protocol_id and tool_name:
                    command = [
                        "python3",
                        UPDATER_SCRIPT,
                        "--protocols-dir",
                        protocols_dir,
                        "add-tool",
                        "--protocol-id",
                        protocol_id,
                        "--tool-name",
                        tool_name,
                    ]
                    command_executed = True
            elif command_name == "update-rule":
                protocol_id = params.get("protocol_id")
                rule_id = params.get("rule_id")
                description = params.get("description")
                if protocol_id and rule_id and description:
                    command = [
                        "python3",
                        UPDATER_SCRIPT,
                        "--protocols-dir",
                        protocols_dir,
                        "update-rule",
                        "--protocol-id",
                        protocol_id,
                        "--rule-id",
                        rule_id,
                        "--description",
                        description,
                    ]
                    command_executed = True

            if command_executed:
                if run_command(command):
                    lesson["status"] = "applied"
                else:
                    lesson["status"] = "failed"
                changes_made = True
            else:
                print(
                    f"Warning: Skipping lesson with unhandled or malformed command: '{command_name}'"
                )

        elif action_type == "PROPOSE_CODE_CHANGE":
            params = action.get("parameters", {})
            filepath = params.get("filepath")
            diff = params.get("diff")

            if not (filepath and diff):
                print(
                    "Error: Malformed 'PROPOSE_CODE_CHANGE' lesson. Missing parameters."
                )
                lesson["status"] = "failed"
                changes_made = True
                continue

            # Note: The diff content needs careful handling for shell quoting.
            # We will pass it as a single string argument.
            command = [
                "python3",
                CODE_SUGGESTER_SCRIPT,
                "--filepath",
                filepath,
                "--diff",
                diff,
            ]

            if run_command(command):
                # For now, "applied" means the suggester ran successfully.
                # The actual execution of the generated plan is handled by the master controller.
                lesson["status"] = "applied"
                print(
                    "Code suggestion plan generated. Master controller will execute it."
                )
            else:
                lesson["status"] = "failed"
            changes_made = True

        elif action_type == "MODIFY_TOOLING":
            params = action.get("parameters", {})
            filepath = params.get("filepath")
            merge_diff = params.get("merge_diff")

            if not (filepath and merge_diff):
                print("Error: Malformed 'MODIFY_TOOLING' lesson. Missing parameters.")
                lesson["status"] = "failed"
                changes_made = True
                continue

            # We must ensure the file path is within the tooling directory for safety
            if not filepath.startswith("tooling/"):
                print(
                    f"Error: MODIFY_TOOLING is restricted to the 'tooling/' directory. Attempted path: {filepath}"
                )
                lesson["status"] = "failed"
                changes_made = True
                continue

            if apply_merge_diff(filepath, merge_diff):
                lesson["status"] = "applied"
                print(f"Successfully applied code modification to {filepath}")
            else:
                lesson["status"] = "failed"
                print(f"Failed to apply code modification to {filepath}")
            changes_made = True

        else:
            # This handles cases where the action type itself is unknown.
            print(f"Warning: Skipping lesson with unknown action type: '{action_type}'")

    return changes_made


def main():
    """
    Main function to run the self-correction workflow.
    """
    # This script is intended to be called from a controlled environment
    # like a test or a dedicated plan, so we don't use argparse here.
    # The search for protocols should start from the repository root.
    protocols_directory = "."

    print("--- Starting Protocol-Driven Self-Correction Cycle ---")
    print("Meta-Mutation: Orchestrator is now self-aware.")
    lessons = load_lessons()

    if not any(lesson.get("status") == "pending" for lesson in lessons):
        print("No pending lessons to process. Exiting.")
        return

    changes_were_applied = process_lessons(lessons, protocols_directory)

    print("\n--- Saving updated lesson statuses ---")
    save_lessons(lessons)

    if changes_were_applied:
        print("\n--- Protocol sources updated. Rebuilding AGENTS.md... ---")
        if not run_command(["make", "AGENTS.md"]):
            print("\nError: Failed to rebuild AGENTS.md after protocol updates.")
        else:
            print("\n--- AGENTS.md successfully rebuilt. ---")

    print("\n--- Self-Correction Cycle Complete ---")


if __name__ == "__main__":
    main()
