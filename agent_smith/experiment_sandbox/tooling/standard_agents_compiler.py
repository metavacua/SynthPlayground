"""
A compiler that generates a simplified, standard-compliant `AGENTS.md` file.

This script acts as an "adapter" to make the repository more accessible to
third-party AI agents that expect a conventional set of instructions. While the
repository's primary `AGENTS.md` is a complex, hierarchical, and
machine-readable artifact for its own specialized agent, the `AGENTS.standard.md`
file produced by this script offers a simple, human-readable summary of the
most common development commands.

The script works by:
1.  **Parsing the Makefile:** It dynamically parses the project's `Makefile`,
    which is the single source of truth for high-level commands. It specifically
    extracts the exact commands for common targets like `install`, `test`,
    `lint`, and `format`. This ensures the generated instructions are never
    stale.
2.  **Injecting into a Template:** It injects these extracted commands into a
    pre-defined, user-friendly Markdown template.
3.  **Generating the Artifact:** The final output is written to
    `AGENTS.standard.md`, providing a simple, stable, and conventional entry
    point for external tools, effectively bridging the gap between the complex
    internal protocol system and the broader agent ecosystem.
"""
import os

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_FILE = os.path.join(ROOT_DIR, "AGENTS.standard.md")
MAKEFILE_PATH = os.path.join(ROOT_DIR, "Makefile")

# --- AGENTS.md Template ---
AGENTS_MD_TEMPLATE = """\
# AGENTS.md

This file provides instructions for AI coding agents to interact with this project. It is generated from the project's `Makefile` to ensure it is always up-to-date.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture. The agent's core protocols are managed programmatically. For detailed, machine-readable protocols, refer to the primary `AGENTS.md` file. This `AGENTS.standard.md` file provides a simplified summary for external tools.

## Build & Commands

Here are the essential commands for working with this repository.

### Dependency Installation

To install all required Python packages, run:
```bash
{install_command}
```

### Running Tests

To run the full suite of unit tests, use the following command:
```bash
{test_command}
```

## Code Style

This project uses standard Python code quality tools.

### Linting

To check the code for style issues, run the linter:
```bash
{lint_command}
```

### Formatting

To automatically format the code, run:
```bash
{format_command}
```

## Project Structure

- `protocols/`: Source files for the agent's governing protocols.
- `tooling/`: Scripts for compilation, validation, and other development tasks.
- `knowledge_core/`: Compiled knowledge artifacts used by the agent.

For more detailed information, please consult the `README.md`.
"""


def parse_makefile_command(target_name, makefile_content):
    """
    Parses a Makefile to find the main command for a specific target,
    skipping any 'echo' lines. This version iterates through lines for robustness.
    """
    lines = makefile_content.splitlines()
    try:
        # Find the line number of the target definition
        target_line_index = next(
            i for i, line in enumerate(lines) if line.startswith(f"{target_name}:")
        )
    except StopIteration:
        # If the target isn't found, fallback to the make command
        return f"make {target_name}"

    # Search for command lines in the lines following the target definition
    for i in range(target_line_index + 1, len(lines)):
        line = lines[i]

        # Command blocks end when a line does not start with a tab
        if not line.startswith("\t"):
            break

        command = line.strip()
        # If the line is an echo command, skip to the next line
        if command.startswith("@echo"):
            continue

        # We've found the first non-echo command. Return it after stripping the '@'.
        return command.lstrip("@").strip()

    # If no suitable command was found in the block, fallback
    return f"make {target_name}"


def main():
    """
    Generates a standard-compliant AGENTS.md file by parsing commands
    from the project's Makefile.
    """
    try:
        with open(MAKEFILE_PATH, "r") as f:
            makefile_content = f.read()
    except FileNotFoundError:
        print(f"Error: Makefile not found at {MAKEFILE_PATH}")
        return

    # Parse the commands from the Makefile
    install_command = parse_makefile_command("install", makefile_content)
    test_command = parse_makefile_command("test", makefile_content)
    lint_command = parse_makefile_command("lint", makefile_content)
    format_command = parse_makefile_command("format", makefile_content)

    # Populate the template
    content = AGENTS_MD_TEMPLATE.format(
        install_command=install_command,
        test_command=test_command,
        lint_command=lint_command,
        format_command=format_command,
    )

    try:
        with open(TARGET_FILE, "w") as f:
            f.write(content)
        print(f"Successfully generated standard-compliant AGENTS.md at {TARGET_FILE}")
    except IOError as e:
        print(f"Error: Failed to write to {TARGET_FILE}: {e}")


if __name__ == "__main__":
    main()
