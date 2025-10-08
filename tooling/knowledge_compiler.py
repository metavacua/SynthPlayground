import argparse
import re
import os
import datetime

KNOWLEDGE_CORE_PATH = "knowledge_core/lessons_learned.md"
POSTMORTEM_TEMPLATE_PATH = "postmortem.md"  # For getting the entry template


def extract_lessons_from_postmortem(postmortem_content: str) -> list:
    """
    Parses a post-mortem report to extract lessons learned.
    """
    # First, isolate the Corrective Actions section to avoid parsing the wrong parts of the file
    lessons_section_match = re.search(
        r"## 3\.\s+Corrective Actions & Lessons Learned\n(.+?)\n---",
        postmortem_content,
        re.DOTALL,
    )
    if not lessons_section_match:
        return []

    lessons_section = lessons_section_match.group(1)

    # Regex to find all numbered "Lesson:" and "Action:" pairs
    # This pattern looks for a number, "Lesson:", captures the text,
    # then "Action:", and captures that text until it hits the next number or the end of the string.
    lesson_pattern = re.compile(
        r"\d\.\s+\*\*Lesson:\*\*\s*(.+?)\n\s+\*\*Action:\*\*\s*(.+?)(?=\n\d\.\s+\*\*Lesson:\*\*|\Z)",
        re.DOTALL,
    )

    extracted = re.findall(lesson_pattern, lessons_section)

    # Clean up whitespace and newlines from captured groups
    cleaned_lessons = []
    for lesson, action in extracted:
        cleaned_lessons.append(
            {
                "lesson": lesson.strip().replace("\n", " "),
                "action": action.strip().replace("\n", " "),
            }
        )

    return cleaned_lessons


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


def format_lesson_entry(metadata: dict, lesson_data: dict) -> str:
    """
    Formats an extracted lesson into the standard entry format.
    """
    # For now, we derive Insight from the lesson and use a placeholder for Observation.
    # This can be improved if the post-mortem format is updated.
    observation_placeholder = (
        "This lesson was derived from the post-mortem analysis of the parent task."
    )

    entry = (
        "---\n"
        f"**Task ID:** {metadata['task_id']}\n"
        f"**Date:** {metadata['date']}\n"
        f"**Observation:** {observation_placeholder}\n"
        f"**Insight:** {lesson_data['lesson']}\n"
        f"**Actionable Guidance:** {lesson_data['action']}\n"
        "---"
    )
    return entry


def main():
    parser = argparse.ArgumentParser(
        description="Parses a post-mortem report and compiles the lessons learned into the knowledge core."
    )
    parser.add_argument(
        "postmortem_path", help="The path to the completed post-mortem markdown file."
    )
    args = parser.parse_args()

    if not os.path.exists(args.postmortem_path):
        print(f"Error: Post-mortem file not found at '{args.postmortem_path}'")
        return

    with open(args.postmortem_path, "r") as f:
        content = f.read()

    metadata = extract_metadata_from_postmortem(content)
    lessons = extract_lessons_from_postmortem(content)

    if not lessons:
        print("No lessons found in the specified post-mortem file.")
        return

    print(f"Found {len(lessons)} new lesson(s) in '{args.postmortem_path}'.")

    with open(KNOWLEDGE_CORE_PATH, "a") as f:
        # Ensure there's a newline before the first new entry if the file isn't empty
        if f.tell() > 0:
            f.write("\n\n")

        for i, lesson in enumerate(lessons):
            formatted_entry = format_lesson_entry(metadata, lesson)
            f.write(formatted_entry)
            if i < len(lessons) - 1:
                f.write("\n\n")

    print(
        f"Successfully compiled {len(lessons)} lesson(s) into '{KNOWLEDGE_CORE_PATH}'."
    )


if __name__ == "__main__":
    main()
