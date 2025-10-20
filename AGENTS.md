#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# AGENTS.md

This file provides instructions for AI coding agents to interact with this project. It is generated from the project's `Makefile` to ensure it is always up-to-date.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture. The agent's core protocols are managed programmatically. For detailed, machine-readable protocols, refer to the primary `AGENTS.md` file. This `AGENTS.standard.md` file provides a simplified summary for external tools.

## Build & Commands

Here are the essential commands for working with this repository.

### Dependency Installation

To install all required Python packages, run:
```bash
$(BUILDER) --target install
```

### Running Tests

To run the full suite of unit tests, use the following command:
```bash
$(BUILDER) --target test
```

## Code Style

This project uses standard Python code quality tools.

### Linting

To check the code for style issues, run the linter:
```bash
$(BUILDER) --target lint
```

### Formatting

To automatically format the code, run:
```bash
$(BUILDER) --target format
```

## Project Structure

- `protocols/`: Source files for the agent's governing protocols.
- `tooling/`: Scripts for compilation, validation, and other development tasks.
- `knowledge_core/`: Compiled knowledge artifacts used by the agent.

For more detailed information, please consult the `README.md`.

"""

import re
import subprocess

def main():
    """
    This script is a self-executing Markdown file.
    It parses its own content to find and execute shell commands.
    """
    # Use the __doc__ attribute to get the docstring, which is the Markdown content.
    markdown_content = __doc__

    commands = re.findall(r'```bash\n(.*?)\n```', markdown_content, re.DOTALL)

    for command in commands:
        # Replace the $(BUILDER) variable with the actual builder command.
        command = command.replace("$(BUILDER)", "python3 tooling/builder.py")
        print(f"--- Executing: {command.strip()} ---")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"--- Command failed with exit code {e.returncode} ---")
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
        print("--- Done ---")

if __name__ == "__main__":
    main()
