# AURA_AGENTS.md

## 1. Introduction

This repository is orchestrated by Aura, a scripting language designed for agentic workflows. All agent behaviors are defined in `.aura` files.

## 2. Aura Programming Language

For a detailed specification of the Aura language, please see the [Aura Language Specification](docs/aura/specification.md).

## 3. Aura API Reference

Aura scripts can interact with the agent's tools via the `agent_call_tool` function.

### 3.1. Available Tools

The following tools are available to be called from Aura scripts:

- `hello_world`: A simple hello world tool.
- `read_file`: Reads a file and returns its contents.
- `get_env`: Gets the value of an environment variable.
- `validate_tdd`: Validates that TDD was followed.
- `validate_guardian`: Validates that the guardian protocol was followed.
- `install_dependencies`: Installs dependencies from requirements.txt.
