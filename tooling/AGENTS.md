# AGENTS.md

**Directory:** `/tooling`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Tooling directory - agent development and build tools

## Protocols

This AGENTS.md file contains 11 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Tooling directory - agent development and build tools
directory: /tooling
generatedAt: '2025-12-27T01:58:32.742535Z'
protocols:
- associated_tools:
  - read_file
  description: A foundational protocol that dictates the agent's initial actions upon
    starting any task.
  protocol_id: agent-bootstrap-001
  rules:
  - description: Upon initialization for any task, the agent's first and highest-priority
      action must be to locate, read, and parse the AGENTS.md file in the repository
      root. This ensures the agent is properly contextualized before any planning
      or execution begins.
    enforcement: This rule is enforced by the agent's core startup logic. The agent
      must verify the load of AGENTS.md before proceeding to the planning phase.
    rule_id: bootstrap-load-agents-md
    tags:
    - compliance
  version: 1.0.0
- associated_tools:
  - tooling/agent_shell.py
  description: A protocol governing the use of the interactive agent shell as the
    primary entry point for all tasks.
  protocol_id: agent-shell-001
  rules:
  - description: All agent tasks must be initiated through the `agent_shell.py` script.
      This script is the designated, API-driven entry point that ensures proper initialization
      of the MasterControlGraph FSM, centralized logging, and programmatic lifecycle
      management. Direct execution of other tools or scripts is forbidden for task
      initiation.
    enforcement: This is a procedural rule. The agent's operational framework should
      only expose the agent_shell.py as the means of starting a new task.
    rule_id: shell-is-primary-entry-point
    tags:
    - core
  version: 1.0.0
- associated_tools:
  - tooling/capability_verifier.py
  description: A protocol for using the capability verifier tool to empirically test
    the agent's monotonic improvement.
  protocol_id: capability-verification-001
  rules:
  - description: The `capability_verifier.py` tool should be used to test the agent's
      ability to acquire a new capability defined by a failing test file. The tool
      orchestrates the failure, self-correction, and verification process.
    enforcement: The tool is used by invoking it from the command line with the path
      to the target test file.
    rule_id: verify-capability-acquisition
    tags:
    - core
  version: 1.0.0
- associated_tools:
  - run_in_bash_session
  description: A protocol for ensuring a reliable execution environment through formal
    dependency management.
  protocol_id: dependency-management-001
  rules:
  - description: Upon starting a task, after loading AGENTS.md, the agent MUST install
      all required Python packages listed in the `requirements.txt` file. This ensures
      the environment is correctly configured before any other tools are executed.
    enforcement: The agent's core startup logic should be designed to execute `pip
      install -r requirements.txt` as one of its initial actions.
    rule_id: dependency-install-on-start
    tags:
    - compliance
  version: 1.0.0
- associated_tools: []
  description: A protocol for maintaining an up-to-date file index to accelerate tool
    performance.
  protocol_id: file-indexing-001
  rules:
  - description: Before submitting any changes that alter the file structure (create,
      delete, rename), the agent MUST rebuild the repository's file index. This ensures
      that tools relying on the index, such as the FDC validator, have an accurate
      view of the filesystem.
    enforcement: This is a procedural rule. The agent's pre-submission checklist should
      include a step to run 'python tooling/some_indexer.py build'.
    rule_id: update-index-before-submit
    tags:
    - core
  version: 1.0.0
- associated_tools:
  - tooling/self_correction_orchestrator.py
  description: A protocol that empowers the agent to modify its own core tooling,
    enabling a recursive self-improvement cycle.
  protocol_id: meta-mutation-001
  rules:
  - description: The agent is authorized to use the 'modify_tooling' action within
      the self_correction_orchestrator.py to apply patches to its own source code
      or other tools in the tooling/ directory. This action must be triggered by a
      structured lesson in knowledge_core/lessons.jsonl.
    enforcement: The self_correction_orchestrator.py must validate that the 'modify_tooling'
      action is well-formed and targets a valid file within the tooling/ directory.
    rule_id: authorize-tooling-modification
- associated_tools:
  - tooling/environmental_probe.py
  - google_search
  - view_text_website
  description: Defines the mandatory, four-tiered orientation cascade that must be
    executed at the start of any task to establish a coherent model of the agent's
    identity, environment, and the world state.
  protocol_id: orientation-cascade-001
  rules:
  - description: 'Level 1 (Self-Awareness): The agent must first establish its own
      identity and inherent limitations by reading the `knowledge_core/agent_meta.json`
      artifact.'
    enforcement: The `start` command of the FDC toolchain executes this step and fails
      if the artifact is missing or invalid.
    rule_id: l1-self-awareness
  - description: 'Level 2 (Repository Sync): The agent must understand the current
      state of the local repository by loading primary artifacts from the `knowledge_core/`
      directory.'
    enforcement: The `start` command of the FDC toolchain executes this step.
    rule_id: l2-repository-sync
  - description: 'Level 3 (Environmental Probing & Targeted RAG): The agent must discover
      the rules and constraints of its operational environment by executing a probe
      script and using targeted RAG to resolve ''known unknowns''.'
    enforcement: The `start` command of the FDC toolchain executes this step, utilizing
      tools like `google_search` and `view_text_website`.
    rule_id: l3-environmental-probing
  - description: 'Level 4 (Deep Research Cycle): To investigate ''unknown unknowns'',
      the agent must initiate a formal, self-contained Finite Development Cycle (FDC)
      of the ''Analysis Modality''.'
    enforcement: This is a special case of recursion, explicitly allowed and managed
      by the FDC toolchain.
    rule_id: l4-deep-research-cycle
  version: 1.0.0
- associated_tools:
  - tooling/fdc_cli.py
  - google_search
  - view_text_website
  description: A set of non-negotiable, high-priority mandates that govern the agent's
    behavior across all tasks.
  protocol_id: standing-orders-001
  rules:
  - description: All Finite Development Cycles (FDCs) MUST be initiated using the
      FDC toolchain's 'start' command. This is non-negotiable.
    enforcement: Enforced by the agent's core operational loop and the `start` command
      in `tooling/fdc_cli.py`.
    rule_id: aorp-mandate
  - description: For any task involving external technologies, Just-In-Time External
      RAG is REQUIRED to verify current best practices. Do not trust internal knowledge.
    enforcement: This is a core principle of the L3 orientation phase, utilizing tools
      like `google_search`.
    rule_id: rag-mandate
  - description: 'Use the `fdc_cli.py` tool for all core FDC state transitions: task
      initiation (''start''), plan linting (''lint''), and task closure (''close'').'
    enforcement: The agent's internal logic is designed to prefer these specific tool
      commands for FDC state transitions.
    rule_id: fdc-toolchain-mandate
  version: 1.0.0
- associated_tools:
  - tooling/auditor.py
  - tooling/protocol_compiler.py
  description: A meta-protocol to ensure the agent's toolchain remains synchronized
    with the architecture of its governing protocols.
  protocol_id: toolchain-review-on-schema-change-001
  rules:
  - description: If a change is made to the core protocol schema (`protocol.schema.json`)
      or to the compilers that process it (`protocol_compiler.py`), a formal audit
      of the entire `tooling/` directory MUST be performed as a subsequent step. This
      audit should verify that all tools are compatible with the new protocol structure.
    enforcement: This is a procedural rule for any agent developing the protocol system.
      Adherence can be partially checked by post-commit hooks or review processes
      that look for a tooling audit in any change that modifies the specified core
      files.
    rule_id: toolchain-audit-on-schema-change
    tags:
    - core
  version: 1.0.0
- associated_tools:
  - tooling/auditor.py
  description: A protocol for the unified repository auditing tool, which combines
    multiple health and compliance checks into a single interface.
  protocol_id: unified-auditor-001
  rules:
  - description: The `auditor.py` script should be used to run comprehensive checks
      on the repository's health. It can be run with 'all' to check protocols, plans,
      and documentation completeness.
    enforcement: The tool is invoked via the command line, typically through the `make
      audit` target.
    rule_id: run-all-audits
    tags:
    - core
  version: 1.0.0
- associated_tools:
  - tooling/doc_builder.py
  description: A protocol for the unified documentation builder, which generates various
    documentation artifacts from the repository's sources of truth.
  protocol_id: unified-doc-builder-001
  rules:
  - description: The `doc_builder.py` script is the single entry point for generating
      all user-facing documentation, including system-level docs, README files, and
      GitHub Pages. It should be called with the appropriate '--format' argument.
    enforcement: The tool is invoked via the command line, typically through the `make
      docs`, `make readme`, or `make pages` targets.
    rule_id: use-doc-builder-for-all-docs
    tags:
    - core
  version: 1.0.0

```

## Protocol Summary

### AGENT-BOOTSTRAP-001

A foundational protocol that dictates the agent's initial actions upon starting any task.

**Rules:**

- `bootstrap-load-agents-md`: Upon initialization for any task, the agent's first and highest-priority action must be to locate, r...

### AGENT-SHELL-001

A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.

**Rules:**

- `shell-is-primary-entry-point`: All agent tasks must be initiated through the `agent_shell.py` script. This script is the designated...

### CAPABILITY-VERIFICATION-001

A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.

**Rules:**

- `verify-capability-acquisition`: The `capability_verifier.py` tool should be used to test the agent's ability to acquire a new capabi...

### DEPENDENCY-MANAGEMENT-001

A protocol for ensuring a reliable execution environment through formal dependency management.

**Rules:**

- `dependency-install-on-start`: Upon starting a task, after loading AGENTS.md, the agent MUST install all required Python packages l...

### FILE-INDEXING-001

A protocol for maintaining an up-to-date file index to accelerate tool performance.

**Rules:**

- `update-index-before-submit`: Before submitting any changes that alter the file structure (create, delete, rename), the agent MUST...

### META-MUTATION-001

A protocol that empowers the agent to modify its own core tooling, enabling a recursive self-improvement cycle.

**Rules:**

- `authorize-tooling-modification`: The agent is authorized to use the 'modify_tooling' action within the self_correction_orchestrator.p...

### ORIENTATION-CASCADE-001

Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.

**Rules:**

- `l1-self-awareness`: Level 1 (Self-Awareness): The agent must first establish its own identity and inherent limitations b...
- `l2-repository-sync`: Level 2 (Repository Sync): The agent must understand the current state of the local repository by lo...
- `l3-environmental-probing`: Level 3 (Environmental Probing & Targeted RAG): The agent must discover the rules and constraints of...
- ... and 1 more rules

### STANDING-ORDERS-001

A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.

**Rules:**

- `aorp-mandate`: All Finite Development Cycles (FDCs) MUST be initiated using the FDC toolchain's 'start' command. Th...
- `rag-mandate`: For any task involving external technologies, Just-In-Time External RAG is REQUIRED to verify curren...
- `fdc-toolchain-mandate`: Use the `fdc_cli.py` tool for all core FDC state transitions: task initiation ('start'), plan lintin...

### TOOLCHAIN-REVIEW-ON-SCHEMA-CHANGE-001

A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

**Rules:**

- `toolchain-audit-on-schema-change`: If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that pr...

### UNIFIED-AUDITOR-001

A protocol for the unified repository auditing tool, which combines multiple health and compliance checks into a single interface.

**Rules:**

- `run-all-audits`: The `auditor.py` script should be used to run comprehensive checks on the repository's health. It ca...

### UNIFIED-DOC-BUILDER-001

A protocol for the unified documentation builder, which generates various documentation artifacts from the repository's sources of truth.

**Rules:**

- `use-doc-builder-for-all-docs`: The `doc_builder.py` script is the single entry point for generating all user-facing documentation, ...

## Notes

*This AGENTS.md file is a build artifact. Do not edit directly.*
*Make changes to source files in `protocols/` directory and regenerate.*

## Build Instructions

To regenerate this file, run:
```bash
python3 tooling/builder.py --target agents-md
```
