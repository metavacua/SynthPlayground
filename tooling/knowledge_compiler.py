"""
Extracts structured lessons from post-mortem reports and compiles them into a
centralized, long-term knowledge base.

This script is a core component of the agent's self-improvement feedback loop.
After a task is completed, a post-mortem report is generated that includes a
section for "Corrective Actions & Lessons Learned." This script automates the
process of parsing that section to extract key insights.

It identifies pairs of "Lesson" and "Action" statements and transforms them
into a standardized, machine-readable format. These formatted entries are then
appended to the `knowledge_core/lessons.jsonl` file, which serves as the
agent's persistent memory of what has worked, what has failed, and what can be
improved in future tasks.

The script is executed via the command line, taking the path to a completed
post-mortem file as its primary argument.
"""

import argparse
import re
import os
import json
import uuid
import datetime

KNOWLEDGE_CORE_PATH = "knowledge_core/lessons.jsonl"


def extract_lessons_from_postmortem(postmortem_content: str) -> list:
    """
    Parses a post-mortem report to extract lessons learned.
    Handles the new, more structured format.
    """
    lesson_match = re.search(
        r"\*\*Lesson:\*\*\s*(.+?)\n", postmortem_content, re.DOTALL
    )
    action_match = re.search(
        r"\*\*Action:\*\*\s*(.+?)\n", postmortem_content, re.DOTALL
    )

    if lesson_match and action_match:
        lesson = lesson_match.group(1).strip()
        action = action_match.group(1).strip()

        # Ignore placeholder content
        if "N/A" in lesson or "N/A" in action:
            return []

        return [{"lesson": lesson, "action": action}]

    return []


def extract_metadata_from_postmortem(postmortem_content: str) -> dict:
    """
    Parses a post-mortem report to extract metadata like Task ID and Date.
    """
    task_id_match = re.search(r"\*\*Task ID:\*\*\s*`(.+?)`", postmortem_content)
    date_match = re.search(r"\*\*Completion Date:\*\*\s*`(.+?)`", postmortem_content)
    return {
        "task_id": task_id_match.group(1) if task_id_match else "Unknown",
        "date": date_match.group(1) if date_match else str(datetime.date.today()),
    }


def parse_action_to_command(action_text: str) -> dict:
    """
    Parses a natural language action string into a machine-executable command.

    This is the core of translating insights into automated actions. It uses
    pattern matching to identify specific, supported commands.
    """
    # Pattern: "Add tool '...' to protocol '...'"
    add_tool_pattern = re.compile(
        r"add tool\s+'([^']*)'\s+to protocol\s+'([^']*)'", re.IGNORECASE
    )
    match = add_tool_pattern.search(action_text)
    if match:
        tool_name, protocol_id = match.groups()
        return {
            "type": "UPDATE_PROTOCOL",
            "command": "add-tool",
            "parameters": {
                "protocol_id": protocol_id,
                "tool_name": tool_name,
            },
        }

    # Pattern: "Update rule '...' in protocol '...' to '...'"
    update_rule_pattern = re.compile(
        r"update rule\s+'([^']*)'\s+in protocol\s+'([^']*)'\s+to\s+'([^']*)'",
        re.IGNORECASE,
    )
    match = update_rule_pattern.search(action_text)
    if match:
        rule_id, protocol_id, description = match.groups()
        return {
            "type": "UPDATE_PROTOCOL",
            "command": "update-rule",
            "parameters": {
                "protocol_id": protocol_id,
                "rule_id": rule_id,
                "description": description,
            },
        }

    # Pattern: "Deprecate tool '...' from protocol '...'"
    deprecate_tool_pattern = re.compile(
        r"deprecate tool\s+'([^']*)'\s+from protocol\s+'([^']*)'", re.IGNORECASE
    )
    match = deprecate_tool_pattern.search(action_text)
    if match:
        tool_name, protocol_id = match.groups()
        return {
            "type": "UPDATE_PROTOCOL",
            "command": "deprecate-tool",
            "parameters": {
                "protocol_id": protocol_id,
                "tool_name": tool_name,
            },
        }

    # Default fallback for actions that are not yet machine-executable
    return {
        "type": "UPDATE_PROTOCOL",
        "command": "placeholder",
        "parameters": {"description": action_text},
    }


def format_lesson_entry(metadata: dict, lesson_data: dict) -> dict:
    """
    Formats an extracted lesson into a structured JSON object.
    """
    actionable_command = parse_action_to_command(lesson_data["action"])

    return {
        "lesson_id": str(uuid.uuid4()),
        "task_id": metadata["task_id"],
        "date": metadata["date"],
        "lesson": lesson_data["lesson"],
        "action": actionable_command,
        "status": "pending",
    }


def process_postmortem_file(filepath):
    """Reads a single post-mortem file and returns its lessons."""
    if not os.path.exists(filepath):
        print(f"Error: Post-mortem file not found at '{filepath}'")
        return []

    with open(filepath, "r") as f:
        content = f.read()

    metadata = extract_metadata_from_postmortem(content)
    lessons_data = extract_lessons_from_postmortem(content)

    if not lessons_data:
        return []

    formatted_lessons = [
        format_lesson_entry(metadata, lesson) for lesson in lessons_data
    ]
    return formatted_lessons


def make_hashable(obj):
    if isinstance(obj, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
    if isinstance(obj, list):
        return tuple(make_hashable(elem) for elem in obj)
    return obj


def get_lesson_key(lesson_data: dict) -> tuple:
    """
    Creates a unique, hashable key for a lesson based on its content,
    ignoring metadata like IDs and dates.
    """
    key_content = {
        "lesson": lesson_data.get("lesson"),
        "action": lesson_data.get("action"),
    }
    return make_hashable(key_content)


def main():
    parser = argparse.ArgumentParser(
        description="Parses post-mortem reports and compiles lessons into a knowledge base."
    )
    parser.add_argument(
        "--source-path",
        required=True,
        help="Path to a post-mortem markdown file or a directory containing them.",
    )
    args = parser.parse_args()
    source_path = args.source_path

    # Ensure the knowledge_core directory exists
    os.makedirs(os.path.dirname(KNOWLEDGE_CORE_PATH), exist_ok=True)

    existing_lesson_keys = set()
    if os.path.exists(KNOWLEDGE_CORE_PATH):
        with open(KNOWLEDGE_CORE_PATH, "r") as f:
            for line in f:
                try:
                    lesson = json.loads(line)
                    existing_lesson_keys.add(get_lesson_key(lesson))
                except (json.JSONDecodeError, AttributeError):
                    continue

    files_to_process = []
    if os.path.isdir(source_path):
        files_to_process = [
            os.path.join(source_path, f)
            for f in os.listdir(source_path)
            if f.endswith(".md")
        ]
    elif os.path.isfile(source_path):
        if source_path.endswith(".md"):
            files_to_process.append(source_path)
    else:
        print(f"Error: The path '{source_path}' is not a valid file or directory.")
        return

    if not files_to_process:
        print(f"No markdown files found at '{source_path}'.")
        return

    new_lessons_added = 0
    with open(KNOWLEDGE_CORE_PATH, "a") as f:
        for filepath in files_to_process:
            lessons = process_postmortem_file(filepath)
            for lesson_data in lessons:
                lesson_key = get_lesson_key(lesson_data)
                if lesson_key not in existing_lesson_keys:
                    print(f"Found new, unique lesson in '{filepath}'.")
                    f.write(json.dumps(lesson_data) + "\n")
                    existing_lesson_keys.add(lesson_key)
                    new_lessons_added += 1

    if new_lessons_added > 0:
        print(
            f"Successfully compiled {new_lessons_added} new lesson(s) into '{KNOWLEDGE_CORE_PATH}'."
        )
    else:
        print("No new lessons found to compile.")


if __name__ == "__main__":
    main()
