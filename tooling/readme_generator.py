"""
A documentation generator that creates a module's README.md file.

This script is a key component of the "documentation as code" pipeline. It
automates the creation of a `README.md` file by dynamically combining content
from both machine-readable protocols and Python source code docstrings.

The generation process is as follows:
1.  **Parse `AGENTS.md`:** It reads the module's `AGENTS.md` file and extracts
    the `protocol_id` and `description` from every JSON protocol block to create
    a summary of the module's core protocols.
2.  **Parse Source Code:** It scans the module's `tooling/` subdirectory for all
    Python (`.py`) files. For each file, it parses the Abstract Syntax Tree (AST)
    to extract the module-level docstring.
3.  **Inject into Template:** It takes the generated protocol summaries and the
    extracted docstrings and injects them into a static Markdown template.
4.  **Write `README.md`:** The final, combined content is written to the
    `README.md` file in the same directory.

This ensures that the high-level `README.md` documentation always stays
synchronized with the ground-truth definitions in the `AGENTS.md` protocols and
the inline documentation within the tools themselves.
"""
import ast
import os
import re
import json
import argparse

# --- Static Content ---

# Manually written overview and architectural description.
# Using a template string allows for easy updates to the narrative.
README_TEMPLATE = """
# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key
components defined within this module. It is automatically generated from the
corresponding `AGENTS.md` file and the source code docstrings.

## Core Protocols

This module is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior within this scope. The key protocols are:

{core_protocols}

## Key Components

{key_components}
"""

# --- Dynamic Content Generation ---


def get_module_docstring(filepath: str) -> str:
    """
    Parses a Python file and extracts the module-level docstring.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
            tree = ast.parse(source, filename=filepath)
            docstring = ast.get_docstring(tree, clean=True)
            return docstring or "_No docstring found._"
    except (FileNotFoundError, SyntaxError) as e:
        print(f"Warning: Could not parse {filepath}. Reason: {e}")
        return f"_Error parsing file: {e}_"


def generate_core_protocols_section(agents_md_path: str) -> str:
    """
    Parses a given AGENTS.md file to extract protocol definitions and generate a Markdown summary.
    """
    if not os.path.exists(agents_md_path):
        return f"_Error: `{agents_md_path}` not found._"

    try:
        with open(agents_md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except IOError as e:
        return f"_Error reading `{agents_md_path}`: {e}_"

    protocol_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
    summary_blocks = re.findall(
        r"## Child Module: `(.*?)`\n\n(.*?)\n\n---", content, re.DOTALL
    )

    parts = []
    for block in protocol_blocks:
        try:
            protocol = json.loads(block)
            protocol_id = protocol.get("protocol_id")
            description = protocol.get("description")
            if protocol_id and description:
                parts.append(f"- **`{protocol_id}`**: {description}")
        except json.JSONDecodeError:
            continue

    for child_name, child_protocols in summary_blocks:
        parts.append(
            f"\n### Child Module: `{child_name}`\n\nThis module includes protocols from its child module `{child_name}`, as summarized below:"
        )
        parts.append(child_protocols)

    if not parts:
        return "_No protocols found in this module._"

    return "\n".join(parts)


def generate_key_components_section(module_path: str) -> str:
    """
    Generates the Markdown for the "Key Components" section by documenting
    any `.py` files found in a `tooling/` subdirectory of the module.
    """
    tooling_dir = os.path.join(module_path, "tooling")
    if not os.path.isdir(tooling_dir):
        return "_No `tooling/` directory found in this module._"

    key_files = [
        f
        for f in os.listdir(tooling_dir)
        if f.endswith(".py") and not f.startswith("test_")
    ]

    if not key_files:
        return "_No key component scripts found in the `tooling/` directory._"

    parts = []
    for filename in sorted(key_files):
        filepath = os.path.join(tooling_dir, filename)
        docstring = get_module_docstring(filepath)
        parts.append(f"- **`{os.path.join('tooling', filename)}`**:")
        indented_doc = "\\n".join([f"  > {line}" for line in docstring.splitlines()])
        parts.append(indented_doc)

    return "\n\n".join(parts)


# --- Main Execution Logic ---


def main(source_file, output_file):
    """
    Main function to generate the README.md content and write it to a file.
    """
    module_path = os.path.dirname(output_file)
    print(f"--- Generating README.md for module: {module_path} ---")

    print(f"--> Generating 'Core Protocols' section from {source_file}...")
    core_protocols_md = generate_core_protocols_section(source_file)

    print("--> Generating 'Key Components' section...")
    key_components_md = generate_key_components_section(module_path)

    print("--> Assembling final README.md content...")
    final_readme_content = README_TEMPLATE.format(
        core_protocols=core_protocols_md,
        key_components=key_components_md,
    ).strip()

    print(f"--> Writing README to {output_file}...")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_readme_content)
        print("--> README.md generated successfully.")
    except IOError as e:
        print(f"Error: Could not write to {output_file}. Reason: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a README.md from a corresponding AGENTS.md file."
    )
    parser.add_argument(
        "--source-file", required=True, help="Path to the source AGENTS.md file."
    )
    parser.add_argument(
        "--output-file", required=True, help="Path for the output README.md file."
    )
    args = parser.parse_args()
    main(args.source_file, args.output_file)
