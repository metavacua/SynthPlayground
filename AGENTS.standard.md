# AGENTS.md

This file provides instructions for AI coding agents to interact with this project. It is generated from the project's `Makefile` to ensure it is always up-to-date.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture. The agent's core protocols are managed programmatically. For detailed, machine-readable protocols, refer to the primary `AGENTS.md` file. This `AGENTS.standard.md` file provides a simplified summary for external tools.

## Build & Commands

Here are the essential commands for working with this repository.

### Dependency Installation

To install all required Python packages, run:
```bash
pip install -r requirements.txt
```

### Running Tests

To run the full suite of unit tests, use the following command:
```bash
python3 -m unittest discover -v .
```

## Code Style

This project uses standard Python code quality tools.

### Linting

To check the code for style issues, run the linter:
```bash
flake8 .
```

### Formatting

To automatically format the code, run:
```bash
black .
```

## Project Structure

- `protocols/`: Source files for the agent's governing protocols.
- `tooling/`: Scripts for compilation, validation, and other development tasks.
- `knowledge_core/`: Compiled knowledge artifacts used by the agent.

For more detailed information, please consult the `README.md`.
