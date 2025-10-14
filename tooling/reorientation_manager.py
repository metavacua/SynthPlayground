"""
Re-orientation Manager

This script is the core of the automated re-orientation process. It is
designed to be triggered by the build system whenever the agent's core
protocols (`AGENTS.md`) are re-compiled.

The manager performs the following key functions:
1.  **Diff Analysis:** It compares the old version of AGENTS.md with the new
    version to identify new protocols, tools, or other key concepts that have
    been introduced.
2.  **Temporal Orientation (Shallow Research):** For each new concept, it
    invokes the `temporal_orienter.py` tool to fetch a high-level summary from
    an external knowledge base like DBpedia. This ensures the agent has a
    baseline understanding of new terms.
3.  **Knowledge Storage:** The summaries from the temporal orientation are
    stored in a structured JSON file (`knowledge_core/temporal_orientations.json`),
    creating a persistent, queryable knowledge artifact.
4.  **Deep Research Trigger:** It analyzes the nature of the changes. If a
    change is deemed significant (e.g., the addition of a new core
    architectural protocol), it programmatically triggers a formal L4 Deep
    Research Cycle by creating a `deep_research_required.json` file.

This automated workflow ensures that the agent never operates with an outdated
understanding of its own protocols. It closes the loop between protocol
modification and the agent's self-awareness, making the system more robust,
adaptive, and reliable.
"""

import argparse
import json
import os
import re
import subprocess

DEEP_RESEARCH_TRIGGER_FILE = "deep_research_required.json"
TEMPORAL_ORIENTATIONS_FILE = "knowledge_core/temporal_orientations.json"
DEEP_RESEARCH_KEYWORDS = ["FDC", "CFDC", "protocol", "agent", "cycle", "architect"]


def parse_concepts_from_agents_md(content):
    """
    Parses an AGENTS.md file to extract a set of key concepts.
    This version uses a simple regex to find protocol IDs and tool names.
    """
    # Regex to find "protocol_id": "some-id"
    protocol_ids = set(re.findall(r'"protocol_id":\s*"([^"]+)"', content))
    # Regex to find tool paths like tooling/some_tool.py
    tool_names = set(re.findall(r"tooling/([a-zA-Z0-9_]+\.py)", content))
    return protocol_ids.union(tool_names)


def run_temporal_orientation(concept):
    """
    Runs the temporal_orienter.py tool for a given concept.
    """
    print(f"  - Running temporal orientation for concept: {concept}")
    try:
        # We need to format concepts to be valid for DBpedia (e.g., CamelCase)
        formatted_concept = "".join(
            word.capitalize() for word in concept.replace("_", " ").split()
        )
        result = subprocess.run(
            ["python3", "tooling/temporal_orienter.py", formatted_concept],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,  # Add a timeout to prevent hanging on network issues
        )
        summary = result.stdout.strip()
        if "No summary found" in summary or "An error occurred" in summary:
            return None
        return summary
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"    - Could not get summary for '{concept}': {e}")
        return None


def update_temporal_orientations(new_orientations):
    """
    Updates the temporal orientations knowledge base.
    """
    if not new_orientations:
        return

    print(
        f"  - Updating '{TEMPORAL_ORIENTATIONS_FILE}' with {len(new_orientations)} new entries."
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(TEMPORAL_ORIENTATIONS_FILE), exist_ok=True)

    # Load existing data
    if os.path.exists(TEMPORAL_ORIENTATIONS_FILE):
        with open(TEMPORAL_ORIENTATIONS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Add new data and save
    data.update(new_orientations)
    with open(TEMPORAL_ORIENTATIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def check_for_deep_research_trigger(new_concepts):
    """
    Checks if any of the new concepts should trigger a deep research cycle.
    """
    for concept in new_concepts:
        for keyword in DEEP_RESEARCH_KEYWORDS:
            if keyword.lower() in concept.lower():
                print(
                    f"  - Significant change detected: New concept '{concept}' contains keyword '{keyword}'."
                )
                return concept
    return None


def main():
    parser = argparse.ArgumentParser(description="Automated Re-orientation Manager.")
    parser.add_argument(
        "--old-agents-file",
        required=True,
        help="Path to the AGENTS.md file before the build.",
    )
    parser.add_argument(
        "--new-agents-file",
        required=True,
        help="Path to the AGENTS.md file after the build.",
    )
    args = parser.parse_args()

    print("[Re-orientation Manager] Starting analysis...")

    # Read file contents
    try:
        with open(args.old_agents_file, "r") as f:
            old_content = f.read()
    except FileNotFoundError:
        # If the old file doesn't exist, this is the first run. No diff possible.
        old_content = ""

    with open(args.new_agents_file, "r") as f:
        new_content = f.read()

    # Find the difference in concepts
    old_concepts = parse_concepts_from_agents_md(old_content)
    new_concepts = parse_concepts_from_agents_md(new_content)
    added_concepts = new_concepts - old_concepts

    if not added_concepts:
        print("[Re-orientation Manager] No new concepts detected. No action needed.")
        return

    print(
        f"[Re-orientation Manager] Detected {len(added_concepts)} new concepts: {', '.join(added_concepts)}"
    )

    # Perform temporal orientation for new concepts
    orientations = {}
    for concept in added_concepts:
        summary = run_temporal_orientation(concept)
        if summary:
            orientations[concept] = summary

    # Update the knowledge base
    update_temporal_orientations(orientations)

    # Check if a deep research cycle is needed
    research_topic = check_for_deep_research_trigger(added_concepts)
    if research_topic:
        print(
            f"[Re-orientation Manager] Triggering L4 Deep Research Cycle for topic: '{research_topic}'"
        )
        with open(DEEP_RESEARCH_TRIGGER_FILE, "w") as f:
            json.dump({"topic": research_topic}, f, indent=2)
    else:
        print("[Re-orientation Manager] No deep research trigger detected.")

    print("[Re-orientation Manager] Process complete.")


if __name__ == "__main__":
    main()
