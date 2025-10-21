# AGENTS.md

This file provides instructions for AI coding agents to interact with this project.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture. The agent's core protocols are managed programmatically. For detailed, machine-readable protocols, please see the JSON block at the end of this file.

## Build & Commands

Here are the essential commands for working with this repository.

### Dependency Installation

To install all required Python packages, run:
```bash
make install
```

### Running Tests

To run the full suite of unit tests, use the following command:
```bash
make test
```

### Code Style

This project uses standard Python code quality tools.

To check the code for style issues, run the linter:
```bash
make lint
```

To automatically format the code, run:
```bash
make format
```

### Documentation

To build the project documentation, run:
```bash
make docs
```

To generate the README, run:
```bash
make readme
```

### Auditing and Security

To run the security scanner, use:
```bash
make security
```

To run a full audit of the project, use:
```bash
make audit
```

To audit the documentation, use:
```bash
make audit-docs
```

### Cleaning

To remove all build artifacts and clean the project directory, run:
```bash
make clean
```

## Project Structure

- `protocols/`: Source files for the agent's governing protocols.
- `tooling/`: Scripts for compilation, validation, and other development tasks.
- `knowledge_core/`: Compiled knowledge artifacts used by the agent.
