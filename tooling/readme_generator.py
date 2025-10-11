"""
Generates the project's README.md file.

This script combines a static, manually written overview with dynamically
generated sections that summarize key components of the system. The goal is
to produce a README that is both informative and easy to maintain, as it
automatically reflects the current state of the documented source code.

The script is designed to be run from the root of the repository and is
integrated into the `Makefile` build process.
"""
import ast
import os

# --- Configuration ---

OUTPUT_FILE = "README.md"
KEY_COMPONENTS_DIR = "tooling/"
# A curated list of files to document in the "Key Components" section.
# This keeps the README high-level and focused on the core architecture.
KEY_FILES_TO_DOCUMENT = [
    "master_control.py",
    "fdc_cli.py",
    "protocol_compiler.py",
    "doc_generator.py",
    "protocol_auditor.py",
    "self_improvement_cli.py",
]

# --- Static Content ---

# Manually written overview and architectural description.
# Using a template string allows for easy updates to the narrative.
README_TEMPLATE = """
# Project Chimera: An Agent Self-Improvement Protocol

## Overview

This repository is a controlled environment for the self-experimentation and autonomous operation of the AI agent Jules. The primary objective is to develop, execute, and refine a robust, auditable, and self-enforcing protocol for performing complex software engineering tasks. The system is designed around a core principle: **the protocol is the code.**

The project automatically generates this README, its system documentation, and its core operational protocols (`AGENTS.md`) from source. This ensures that the documentation and the codebase are always in sync.

## Core Architecture: The Integrated FSM Workflow

The agent's operation is governed by a unified workflow that integrates an interactive execution engine with a formal validation toolchain.

1.  **Execution Engine (`tooling/master_control.py`):** A Finite State Machine (FSM) that orchestrates the agent's actions. It is the heart of the system, driving the agent through the formal phases of a task.
2.  **Validation & Management Toolchain (`tooling/fdc_cli.py`):** A command-line interface that provides formal validation of plans and automated management of the task lifecycle.

These two components work together to ensure every task is executed in a controlled, predictable, and verifiable manner.

## Key Components

{key_components}

## Build System & Usage

This project uses a `Makefile` to automate common development tasks.

-   `make build`: The main command. Generates all documentation (`README.md`, `SYSTEM_DOCUMENTATION.md`) and compiles all protocols (`AGENTS.md`, `SECURITY.md`).
-   `make test`: Runs the complete unit test suite.
-   `make format`: Formats all Python code using `black`.
-   `make lint`: Lints all Python code using `flake8`.
-   `make clean`: Removes all generated artifacts.

"""

# --- Dynamic Content Generation ---

def get_module_docstring(filepath: str) -> str:
    """
    Parses a Python file and extracts the module-level docstring.

    Args:
        filepath: The path to the Python file.

    Returns:
        The module docstring, or a placeholder if none is found.
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


def generate_key_components_section() -> str:
    """
    Generates the Markdown for the "Key Components" section by reading
    the docstrings of the curated list of files.
    """
    parts = []
    for filename in KEY_FILES_TO_DOCUMENT:
        filepath = os.path.join(KEY_COMPONENTS_DIR, filename)
        if os.path.exists(filepath):
            docstring = get_module_docstring(filepath)
            # Format as a definition list for clarity
            parts.append(f"- **`{filepath}`**:")
            # Indent the docstring for better readability
            indented_doc = "\\n".join([f"  > {line}" for line in docstring.splitlines()])
            parts.append(indented_doc)

    if not parts:
        return "_No key components were documented. Check configuration._"

    return "\n\n".join(parts)

# --- Main Execution Logic ---

def main():
    """
    Main function to generate the README.md content and write it to a file.
    """
    print("--> Generating 'Key Components' section...")
    key_components_md = generate_key_components_section()

    print("--> Assembling final README.md content...")
    # Replace the placeholder in the template with the generated content
    final_readme_content = README_TEMPLATE.format(
        key_components=key_components_md
    ).strip()

    print(f"--> Writing README to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_readme_content)
        print("--> README.md generated successfully.")
    except IOError as e:
        print(f"Error: Could not write to {OUTPUT_FILE}. Reason: {e}")


if __name__ == "__main__":
    main()