# AGENTS.md

**Directory:** `/postmortems`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Default protocol set for unmapped directories

## Protocols

This AGENTS.md file contains 7 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Default protocol set for unmapped directories
directory: /postmortems
generatedAt: '2025-12-27T01:58:32.595430Z'
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
  - create_file_with_block
  - overwrite_file_with_block
  - replace_with_git_merge_diff
  - delete_file
  - read_file
  - list_files
  - grep
  description: A set of best practices derived from observing successful, data-driven
    workflow patterns.
  protocol_id: best-practices-001
  rules:
  - description: After every file creation or modification action (`create_file_with_block`,
      `overwrite_file_with_block`, `replace_with_git_merge_diff`), the agent MUST
      use a subsequent read-only tool (`read_file`, `list_files`, `grep`) to verify
      that the action was executed successfully and had the intended effect. A plan
      step should only be marked as complete after this verification.
    enforcement: This is a core operational discipline. Future tooling, such as a
      trace validator, could enforce this by analyzing the execution log against this
      protocol.
    rule_id: verify-after-write
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
- description: A protocol that defines non-compliance with AGENTS.md and specifies
    corrective actions.
  protocol_id: non-compliance-protocol-001
  rules:
  - description: Defines non-compliance as a violation of any rule, convention, or
      procedure in AGENTS.md or its source protocols.
    enforcement: This is a definitional rule. Enforcement is achieved through the
      agent's adherence to the specific non-compliance rules that follow.
    rule_id: non-compliance-definition
  - associated_tools:
    - restore_file
    - run_in_bash_session
    description: Prohibits the direct editing of build artifacts like AGENTS.md or
      README.md. Changes must be made to source files, followed by a rebuild.
    enforcement: Agent must revert direct edits and modify source files, then run
      the appropriate build command.
    rule_id: non-compliance-direct-editing
  - associated_tools:
    - run_in_bash_session
    description: Requires adherence to all documented testing procedures before submitting
      changes.
    enforcement: Agent must halt execution and run the required tests, debugging any
      failures before proceeding.
    rule_id: non-compliance-test-procedure
  - description: Forbids changes that contradict documented architectural patterns
      or coding conventions.
    enforcement: Agent must revert non-compliant changes and re-implement them according
      to standards.
    rule_id: non-compliance-architectural-deviation
  - associated_tools:
    - run_in_bash_session
    description: Requires the agent to maintain an up-to-date understanding of protocols
      by recompiling AGENTS.md when necessary.
    enforcement: Agent should run 'make AGENTS.md' to refresh its protocol knowledge
      and re-evaluate its plan.
    rule_id: non-compliance-self-awareness-failure
  version: 1.0.0
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

### BEST-PRACTICES-001

A set of best practices derived from observing successful, data-driven workflow patterns.

**Rules:**

- `verify-after-write`: After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_blo...

### DEPENDENCY-MANAGEMENT-001

A protocol for ensuring a reliable execution environment through formal dependency management.

**Rules:**

- `dependency-install-on-start`: Upon starting a task, after loading AGENTS.md, the agent MUST install all required Python packages l...

### NON-COMPLIANCE-PROTOCOL-001

A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.

**Rules:**

- `non-compliance-definition`: Defines non-compliance as a violation of any rule, convention, or procedure in AGENTS.md or its sour...
- `non-compliance-direct-editing`: Prohibits the direct editing of build artifacts like AGENTS.md or README.md. Changes must be made to...
- `non-compliance-test-procedure`: Requires adherence to all documented testing procedures before submitting changes....
- ... and 2 more rules

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

## Notes

*This AGENTS.md file is a build artifact. Do not edit directly.*
*Make changes to source files in `protocols/` directory and regenerate.*

## Build Instructions

To regenerate this file, run:
```bash
python3 tooling/builder.py --target agents-md
```
