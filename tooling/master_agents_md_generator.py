"""
Generates the master AGENTS.md file by synthesizing information from the
migrated manual protocols and the build configuration.

This script creates an instruction-focused AGENTS.md file that provides a
direct, actionable set of protocols for an AI agent to follow, in line with
the best practices from agents.md.
"""

import argparse
import json
import os
import re
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

The agent's behavior is governed by the following set of formal protocols. You are required to adhere to these protocols at all times.

{migrated_protocols}

---

## Knowledge Core

The `knowledge_core` directory is your primary knowledge base. All protocols are defined in `knowledge_core/enriched_protocols.ttl`. You must use the enriched data to improve your understanding of tasks.
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


def load_migrated_protocols(protocols_dir: str) -> str:
    """
    Reads all protocol markdown files from the manual_protocol directory
    and concatenates them into a single string.
    """
    if not os.path.isdir(protocols_dir):
        return "_No migrated protocols found._"

    protocol_contents = []
    # Sort files to ensure a consistent order
    for filename in sorted(os.listdir(protocols_dir)):
        if filename.endswith(".md"):
            filepath = os.path.join(protocols_dir, filename)
            with open(filepath, "r") as f:
                # Add a horizontal rule to separate protocols
                protocol_contents.append(f.read())
                protocol_contents.append("\n\n---\n\n")

    return "".join(protocol_contents)


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
        "--output-file",
        required=True,
        help="Path to the output AGENTS.md file.",
    )
    parser.add_argument(
        "--protocols-dir",
        default="protocols/manual_protocol",
        help="Path to the directory with migrated protocols.",
    )
    args = parser.parse_args()

    # --- Generate Content ---
    build_summary = summarize_build_commands(args.build_config)
    migrated_protocols = load_migrated_protocols(args.protocols_dir)

    # --- Populate Template ---
    final_content = AGENTS_MD_TEMPLATE.format(
        generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        build_commands_summary=build_summary,
        migrated_protocols=migrated_protocols,
    )

    # --- Write Output ---
    with open(args.output_file, "w") as f:
        f.write(final_content.strip())

    print(f"Successfully generated master AGENTS.md at '{args.output_file}'")


if __name__ == "__main__":
    main()
