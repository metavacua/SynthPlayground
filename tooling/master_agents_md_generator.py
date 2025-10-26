
import argparse
import json
import os
from datetime import datetime
import yaml

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
        config = yaml.safe_load(f)

    summary_parts = []
    summary_parts.append("### Build Groups\n")
    for group_name, members in config.get("build_groups", {}).items():
        summary_parts.append(
            f"- **`{group_name}`**: Runs the following targets: `{', '.join(members)}`"
        )

    summary_parts.append("\n### Individual Targets\n")
    for target_name, details in config.get("targets", {}).items():
        description = details.get("description", "No description available.")
        summary_parts.append(f"- **`{target_name}`**: {description}")

    return "\n".join(summary_parts)


def generate_enriched_protocols(knowledge_path: str) -> str:
    """
    Parses the integrated knowledge graph and generates a formatted string
    of protocols and rules.
    """
    if not os.path.exists(knowledge_path):
        return "_Enriched knowledge core not found._"

    with open(knowledge_path, "r") as f:
        data = json.load(f)

    protocol_contents = []
    if "@graph" in data:
        for protocol in data["@graph"]:
            protocol_contents.append(f"### Protocol: `{protocol['protocol_id']}`")
            protocol_contents.append(f"**Description**: {protocol['description']}\n")
            if "rules" in protocol and protocol["rules"]:
                protocol_contents.append("**Rules:**\n")
                for rule in protocol["rules"]:
                    protocol_contents.append(f"- **`{rule['rule_id']}`**: {rule['description']}")
            protocol_contents.append("\n---")

    return "\n".join(protocol_contents)

def generate_yaml_ld_string(knowledge_path: str) -> str:
    """
    Converts the JSON-LD knowledge graph to a YAML-LD string.
    """
    if not os.path.exists(knowledge_path):
        return ""

    with open(knowledge_path, "r") as f:
        data = json.load(f)

    return yaml.dump(data)


def main():
    parser = argparse.ArgumentParser(
        description="Generates the master AGENTS.md file."
    )
    parser.add_argument(
        "--build-config",
        required=True,
        help="Path to the build_config.yaml file.",
    )
    parser.add_argument(
        "--knowledge-file",
        required=True,
        help="Path to the integrated_knowledge.jsonld file.",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path to the root AGENTS.md file.",
    )
    args = parser.parse_args()

    # --- Generate Content ---
    build_summary = summarize_build_commands(args.build_config)
    enriched_protocols = generate_enriched_protocols(args.knowledge_file)
    yaml_ld_string = generate_yaml_ld_string(args.knowledge_file)

    # --- Populate Template ---
    final_content = AGENTS_MD_TEMPLATE.format(
        generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        build_commands_summary=build_summary,
        enriched_protocols=enriched_protocols,
    )

    # --- Update all AGENTS.md files ---
    for root, _, files in os.walk("."):
        for file in files:
            if file == "AGENTS.md":
                filepath = os.path.join(root, file)
                with open(filepath, "w") as f:
                    f.write(final_content.strip())
                    f.write("\n\n```yaml\n")
                    f.write(yaml_ld_string)
                    f.write("```\n")
                print(f"Successfully generated AGENTS.md at '{filepath}'")


if __name__ == "__main__":
    main()
