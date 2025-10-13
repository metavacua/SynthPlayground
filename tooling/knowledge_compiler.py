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
import yaml
import glob

KNOWLEDGE_CORE_PATH = "knowledge_core/lessons.jsonl"


def load_and_parse_sequents(sequents_dir="sequents/"):
    """
    Loads all generated sequent files and returns a list of proven rules.
    """
    all_rules = []
    if not os.path.exists(sequents_dir):
        print(f"Warning: Sequents directory '{sequents_dir}' not found.")
        return all_rules

    for filepath in glob.glob(os.path.join(sequents_dir, "*.agents.md")):
        with open(filepath, 'r') as f:
            try:
                data = yaml.safe_load(f)
                # The top-level key is 'sequent', but we check to be safe
                sequent_data = data.get("sequent", {})
                calculus_title = data.get("title", "Unknown Calculus")

                # The succedent contains the list of proven rules
                succedent = sequent_data.get("succedent", [])
                for rule in succedent:
                    rule['calculus'] = calculus_title # Add provenance
                    all_rules.append(rule)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML from {filepath}: {e}")
    return all_rules


def extract_lessons_from_postmortem(postmortem_content: str) -> list:
    """
    Parses a post-mortem report to extract lessons learned.
    Handles multiple possible section headers and formats.
    """
    lessons_section_match = re.search(
        r"## (?:3\.\s+Corrective Actions & Lessons Learned|5\.\s+Proposed Corrective Actions)\n(.+?)(?:\n---|\Z)",
        postmortem_content,
        re.DOTALL,
    )
    if not lessons_section_match:
        return []

    lessons_section = lessons_section_match.group(1)

    # Pattern to capture each numbered list item
    item_pattern = re.compile(
        r"^\d\.\s+(.*?)(?=\n^\d\.\s+|\Z)", re.DOTALL | re.MULTILINE
    )
    items = item_pattern.findall(lessons_section)

    cleaned_lessons = []
    for item in items:
        lesson = ""
        action = ""

        action_match = re.search(r"\*\*Action:\*\*(.*)", item, re.DOTALL)

        if action_match:
            action = action_match.group(1).strip()
            # The lesson is whatever comes before "**Action:**"
            lesson = item[:action_match.start()].strip()
            # If there's an explicit **Lesson:**, prefer that.
            lesson_explicit_match = re.search(r"\*\*Lesson:\*\*(.*)", lesson, re.DOTALL)
            if lesson_explicit_match:
                lesson = lesson_explicit_match.group(1).strip()
        else:
            # No "**Action:**" found, so the whole item is the action.
            action = item.strip()

        # If we failed to find a lesson text, generate one.
        if not lesson:
            lesson = f"A corrective action was proposed: {action}"

        if lesson or action:
            cleaned_lessons.append({
                "lesson": lesson.replace("\n", " "),
                "action": action.replace("\n", " "),
            })

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
        r"update rule\s+'([^']*)'\s+in protocol\s+'([^']*)'\s+to\s+'([^']*)'", re.IGNORECASE
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
        "parameters": {"description": action_text}
    }


def format_lesson_entry(metadata: dict, lesson_data: dict) -> dict:
    """
    Formats an extracted lesson into a structured JSON object.
    """
    actionable_command = parse_action_to_command(lesson_data['action'])

    return {
        "lesson_id": str(uuid.uuid4()),
        "task_id": metadata["task_id"],
        "date": metadata["date"],
        "insight": lesson_data["lesson"],
        "action": actionable_command,
        "status": "pending"
    }


def sequents_to_rdf(sequents_data):
    """
    Converts a list of parsed sequent rules into an RDF graph.
    """
    from rdflib import Graph, URIRef, Literal, Namespace
    from rdflib.namespace import RDF, RDFS, PROV

    g = Graph()
    BUILD_NS = Namespace("http://example.com/build#")

    g.bind("build", BUILD_NS)
    g.bind("prov", PROV)

    for rule in sequents_data:
        rule_uri = BUILD_NS[rule['id']]
        g.add((rule_uri, RDF.type, BUILD_NS.ProofRule))
        g.add((rule_uri, RDFS.label, Literal(rule['proposition'])))
        g.add((rule_uri, BUILD_NS.calculus, Literal(rule['calculus'])))

        # Add conclusion
        conclusion_bnode = BUILD_NS[f"{rule['id']}-conclusion"]
        g.add((rule_uri, PROV.generated, conclusion_bnode))
        g.add((conclusion_bnode, RDF.type, PROV.Entity))
        g.add((conclusion_bnode, RDFS.label, Literal(json.dumps(rule['provenance']['conclusion']))))

        # Add hypotheses
        for i, hypo in enumerate(rule['provenance']['hypotheses']):
            hypo_bnode = BUILD_NS[f"{rule['id']}-hypo-{i}"]
            g.add((rule_uri, PROV.used, hypo_bnode))
            g.add((hypo_bnode, RDF.type, PROV.Entity))
            g.add((hypo_bnode, RDFS.label, Literal(json.dumps(hypo))))

    return g


def main():
    parser = argparse.ArgumentParser(
        description="Compiles lessons from post-mortems or calculi from .tex files into the knowledge core."
    )
    parser.add_argument(
        "--source",
        choices=['postmortem', 'calculus'],
        required=True,
        help="The source of knowledge to compile."
    )
    parser.add_argument(
        "path", help="The path to the source file or directory."
    )
    args = parser.parse_args()

    if args.source == 'postmortem':
        if not os.path.exists(args.path):
            print(f"Error: Post-mortem file not found at '{args.path}'")
            return

        with open(args.path, "r") as f:
            content = f.read()

        metadata = extract_metadata_from_postmortem(content)
        lessons = extract_lessons_from_postmortem(content)

        if not lessons:
            print("No lessons found in the specified post-mortem file.")
            return

        print(f"Found {len(lessons)} new lesson(s) in '{args.path}'.")
        with open(KNOWLEDGE_CORE_PATH, "a") as f:
            for lesson in lessons:
                formatted_entry = format_lesson_entry(metadata, lesson)
                f.write(json.dumps(formatted_entry) + "\n")
        print(f"Successfully compiled {len(lessons)} lesson(s) into '{KNOWLEDGE_CORE_PATH}'.")

    elif args.source == 'calculus':
        from rdflib import Graph
        sequents_data = load_and_parse_sequents(args.path)
        if not sequents_data:
            print(f"No valid sequent files found in '{args.path}'.")
            return

        rdf_graph = sequents_to_rdf(sequents_data)

        # Integrate with main knowledge graph
        kg_path = "knowledge_core/protocols.ttl"
        main_graph = Graph()
        if os.path.exists(kg_path):
            main_graph.parse(kg_path, format="turtle")

        print(f"Integrating {len(rdf_graph)} new triples from calculi into the knowledge graph.")
        main_graph += rdf_graph

        main_graph.serialize(destination=kg_path, format="turtle")
        print(f"Successfully updated '{kg_path}'.")


if __name__ == "__main__":
    main()
