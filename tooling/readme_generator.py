"""
A tool for automatically generating a `README.md` file for a given module.

This script creates a structured and human-readable `README.md` file by
combining static templates with dynamically generated content extracted from the
module's own source files. It is a key part of the project's "self-documenting"
philosophy, ensuring that the high-level documentation stays synchronized with
the source of truth (the code and protocols).

The generator performs two main dynamic functions:

1.  **Protocol Summary Generation:** It parses the module's `AGENTS.md` file to
    find all defined protocol blocks (both those native to the module and those
    imported from child modules). It then formats this information into a clear,
    list-based summary that provides a high-level overview of the module's
    governing rules.

2.  **Key Component Documentation:** It scans the module's `tooling/` subdirectory
    (if it exists) and finds all Python scripts within it. For each script, it
    parses the source code to extract the module-level docstring. This provides
    a concise summary of the key tools and components that make up the module's
    functionality.

The final output is a consistent, auto-updating README that serves as the primary
entry point for any human or agent seeking to understand the purpose, rules, and
capabilities of the module.
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
