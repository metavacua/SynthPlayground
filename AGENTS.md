# AGENTS.md (Dynamically Generated)

**Last Generated:** 2025-10-30 01:01:48 UTC

## Objective

To provide a systematic, non-negotiable protocol for task execution, self-correction, and knowledge acquisition within this repository. Adherence to this protocol is mandatory for all operations. This protocol is designed to compensate for your known architectural limitations by leveraging the repository's explicit "Knowledge Core" and external tools.

---

## Setup & Build Commands

The following build targets are the primary way to test, build, and maintain this repository. To run any target, use the command: `python3 tooling/builder.py --target <name>`

### Build Groups

- **`all`**: Runs the following targets: `protocols, knowledge-integrate, agents-md`
- **`knowledge`**: Runs the following targets: `knowledge-integrate`

### Individual Targets

- **`agents-md`**: Generate the master AGENTS.md file.
- **`ast-generate`**: Generate ASTs for all supported source files.
- **`extract-symbols`**: Extract symbols from ASTs to create a symbol map.
- **`remove-unused-imports`**: Remove unused imports from all Python files.
- **`format`**: Format the code using black.
- **`guardian-protocol`**: Compile the guardian protocol.
- **`install`**: Install Python dependencies.
- **`knowledge-integrate`**: Integrate knowledge from various sources.
- **`lint`**: Lint the code using flake8.
- **`protocols`**: Compile all protocol sources to a single YAML-LD file.
- **`test`**: Run the test suite using pytest.

---

## Core Directives & Protocols

The agent's behavior is governed by the following set of formal protocols, which are dynamically generated from the repository's enriched knowledge core. You are required to adhere to these protocols at all times.

### Protocol: `charter-protocol-001`
**Description**: The foundational principles governing the agent's operation within this repository.

**Rules:**

- **`CP-1`**: The agent must adhere to the formal, machine-readable protocols defined in the `protocols/` directory and compiled into the `AGENTS.md` file.
- **`CP-2`**: The agent must prioritize using the artifacts in the `knowledge_core/` directory over attempting to infer information from unstructured source code.

---
### Protocol: `git-workflow-protocol-001`
**Description**: The standard operating procedure for all git-related activities.

**Rules:**

- **`GWP-1`**: All changes must be proposed using the `submit` tool. Direct `git push` or `git commit` commands are forbidden.
- **`GWP-2`**: Before making any changes, create a new local branch for isolation.

---
### Protocol: `hello-world-protocol-001`
**Description**: A protocol for greeting the world.

**Rules:**

- **`greet-the-world`**: When this rule is invoked, the agent must use the `hello_world` tool to print the message 'Hello, World!'.

---

```yaml
'@context': protocols/protocol.context.jsonld
'@graph':
- description: The foundational principles governing the agent's operation within
    this repository.
  protocol_id: charter-protocol-001
  rules:
  - associated_tools: []
    description: The agent must adhere to the formal, machine-readable protocols defined
      in the `protocols/` directory and compiled into the `AGENTS.md` file.
    enforcement: strict
    rule_id: CP-1
  - associated_tools:
    - file_reader
    description: The agent must prioritize using the artifacts in the `knowledge_core/`
      directory over attempting to infer information from unstructured source code.
    enforcement: strict
    rule_id: CP-2
  version: 1.0.0
- description: The standard operating procedure for all git-related activities.
  protocol_id: git-workflow-protocol-001
  rules:
  - associated_tools:
    - submit
    description: All changes must be proposed using the `submit` tool. Direct `git
      push` or `git commit` commands are forbidden.
    enforcement: strict
    rule_id: GWP-1
  - associated_tools:
    - run_in_bash_session
    description: Before making any changes, create a new local branch for isolation.
    enforcement: strict
    rule_id: GWP-2
  version: 1.0.0
- description: A protocol for greeting the world.
  protocol_id: hello-world-protocol-001
  rules:
  - associated_tools:
    - hello_world
    description: When this rule is invoked, the agent must use the `hello_world` tool
      to print the message 'Hello, World!'.
    enforcement: strict
    rule_id: greet-the-world
  version: 1.0.0
```
