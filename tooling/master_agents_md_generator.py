"""
Generates the master AGENTS.md file by synthesizing information from the
integrated knowledge core and the build configuration.

This script creates an instruction-focused AGENTS.md file that is a direct
reflection of the repository's enriched knowledge, providing a dynamic and
intelligent set of protocols for an AI agent.
"""

import argparse
import json
import os
from datetime import datetime

# --- Template for the master AGENTS.md ---
AGENTS_MD_TEMPLATE = """
# AGENTS.md (Dynamically Generated)

**Last Generated:** {generation_date}

## Objective

To provide a systematic, non-negotiable protocol for task execution, self-correction, and knowledge acquisition within this repository. Adherence to this protocol is mandatory for all operations. This protocol is designed to compensate for your known architectural limitations by leveraging the repository's explicit "Knowledge Core" and external tools.

---

## Setup & Build Commands

The following build targets are the primary way to test, build, and maintain this repository. To run any target, use the command: `python3 tooling/builder.py --target <name>`

{build_commands_summary}

---

## Core Directives & Protocols

The agent's behavior is governed by the following set of formal protocols, which are dynamically generated from the repository's enriched knowledge core. You are required to adhere to these protocols at all times.

{enriched_protocols}
"""


def summarize_build_commands(config_path: str) -> str:
    """
    Reads the build configuration and creates a summary of available commands.
    """
    if not os.path.exists(config_path):
        return "_Build configuration not found._"

    with open(config_path, "r") as f:
        config = json.load(f)

    summary_parts = []
    summary_parts.append("### Build Groups\n")
    for group_name, members in config.get("build_groups", {}).items():
        summary_parts.append(f"- **`{group_name}`**: Runs the following targets: `{', '.join(members)}`")

    summary_parts.append("\n### Individual Targets\n")
    for target_name, details in config.get("targets", {}).items():
        description = details.get("description", "No description available.")
        summary_parts.append(f"- **`{target_name}`**: {description}")

    return "\n".join(summary_parts)


def generate_enriched_protocols(knowledge_path: str) -> str:
    """
    Parses the integrated knowledge graph and generates a formatted string
    of protocols, rules, and DBPedia links.
    """
    if not os.path.exists(knowledge_path):
        return "_Enriched knowledge core not found._"

    with open(knowledge_path, "r") as f:
        graph = json.load(f)

    protocols = {}
    rules = {}

    # First pass: identify all protocols and rules
    for node in graph:
        node_type = node.get("@type", [""])[0]
        if "Protocol" in node_type:
            protocols[node["@id"]] = {
                "label": node.get("http://www.w3.org/2000/01/rdf-schema#label", [{"@value": ""}])[0]["@value"],
                "rules": []
            }
        elif "Rule" in node_type:
            rules[node["@id"]] = node.get("http://www.w3.org/2000/01/rdf-schema#label", [{"@value": ""}])[0]["@value"]

    # Second pass: associate rules with protocols
    for node in graph:
        if "Protocol" in node.get("@type", [""])[0]:
            protocol_id = node["@id"]
            for rule_ref in node.get("http://example.org/ontology#hasRule", []):
                rule_id = rule_ref["@id"]
                if rule_id in rules:
                    protocols[protocol_id]["rules"].append(rules[rule_id])

    # Generate the formatted output
    protocol_contents = []
    for _, protocol in protocols.items():
        protocol_contents.append(f"### {protocol['label']}")
        if protocol['rules']:
            protocol_contents.append("\n**Rules:**\n")
            for rule in protocol['rules']:
                protocol_contents.append(f"- {rule}")
        protocol_contents.append("\n---")

    return "\n".join(protocol_contents)


def main():
    parser = argparse.ArgumentParser(
        description="Generates the master AGENTS.md file."
    )
    parser.add_argument(
        "--build-config",
        required=True,
        help="Path to the build_config.json file.",
    )
    parser.add_argument(
        "--knowledge-file",
        required=True,
        help="Path to the integrated_knowledge.json file.",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path to the output AGENTS.md file.",
    )
    args = parser.parse_args()

    # --- Generate Content ---
    build_summary = summarize_build_commands(args.build_config)
    enriched_protocols = generate_enriched_protocols(args.knowledge_file)

    # --- Populate Template ---
    final_content = AGENTS_MD_TEMPLATE.format(
        generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        build_commands_summary=build_summary,
        enriched_protocols=enriched_protocols,
    )

    # --- Write Output ---
    with open(args.output_file, "w") as f:
        f.write(final_content.strip())

    print(f"Successfully generated master AGENTS.md at '{args.output_file}'")


if __name__ == "__main__":
    main()
