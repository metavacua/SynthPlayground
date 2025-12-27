# AGENTS.md

**Directory:** `/protocols/core/protocols`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Default protocol set for unmapped directories

## Protocols

This AGENTS.md file contains 8 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Default protocol set for unmapped directories
directory: /protocols/core/protocols
generatedAt: '2025-12-27T01:58:32.666090Z'
protocols:
- description: Defines the identity and versioning of the Advanced Orientation and
    Research Protocol (AORP).
  protocol_id: aorp-header
  rules:
  - description: The governing protocol set is identified as the Advanced Orientation
      and Research Protocol (AORP).
    enforcement: Protocol is identified by its name in documentation and compiled
      artifacts.
    rule_id: aorp-identity
  - description: The official protocol version is tracked in the VERSION file in the
      repository root, following Semantic Versioning (SemVer).
    enforcement: Build or validation scripts should verify the presence and format
      of the VERSION file.
    rule_id: aorp-versioning
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
  - tooling/master_control.py
  - tooling/fdc_cli.py
  description: Defines the Context-Free Development Cycle (CFDC), a hierarchical planning
    and execution model.
  protocol_id: cfdc-protocol-001
  rules:
  - description: Plans may execute other plans as sub-routines using the 'call_plan
      <path_to_plan>' directive. This enables a modular, hierarchical workflow.
    enforcement: The plan validator must be able to parse this directive and recursively
      validate sub-plans. The execution engine must implement a plan execution stack
      to manage the context of nested calls.
    rule_id: hierarchical-planning-via-call-plan
  - description: To ensure decidability, the plan execution stack must not exceed
      a system-wide constant, MAX_RECURSION_DEPTH. This prevents infinite recursion
      and guarantees all processes will terminate.
    enforcement: The execution engine must check the stack depth before every 'call_plan'
      execution and terminate with a fatal error if the limit would be exceeded.
    rule_id: max-recursion-depth
  version: 1.0.0
- associated_tools:
  - tooling/fdc_cli.py
  - tooling/fdc_fsm.json
  description: Ensures all development processes are formally decidable and computationally
    tractable.
  protocol_id: decidability-constraints-001
  rules:
  - description: The agent's planning and execution language is, by design, not Turing-complete.
      This is a fundamental constraint to guarantee that all processes will terminate.
    enforcement: Enforced by the design of the plan runner and validated by the `lint`
      command in the FDC toolchain.
    rule_id: non-turing-completeness
  - description: The agent MUST NOT generate plans that involve recursion or self-invocation.
      A plan cannot trigger another FDC or a sub-plan, with the sole exception of
      the 'Deep Research Cycle'.
    enforcement: The `lint` command in `tooling/fdc_cli.py` scans plans for disallowed
      recursive calls.
    rule_id: bounded-recursion
  - description: All plans must be valid strings in the language defined by the tooling/fdc_fsm.json
      Finite State Machine.
    enforcement: The `lint` command in `tooling/fdc_cli.py` validates the plan against
      the FSM definition.
    rule_id: fsm-adherence
  version: 1.0.0
- associated_tools:
  - tooling/fdc_cli.py
  - tooling/fdc_fsm.json
  - knowledge_core/symbols.json
  - knowledge_core/dependency_graph.json
  - LOGGING_SCHEMA.md
  - set_plan
  - message_user
  description: Defines the Finite Development Cycle (FDC), a formally defined process
    for executing a single, coherent task.
  protocol_id: fdc-protocol-001
  rules:
  - description: The AORP cascade is the mandatory entry point to every FDC.
    enforcement: Enforced by the `start` command in `tooling/fdc_cli.py`.
    rule_id: fdc-entry-point
  - description: The FDC is a Finite State Machine (FSM) formally defined in `tooling/fdc_fsm.json`.
      Plans must be valid strings in the language defined by this FSM.
    enforcement: Validated by the `lint` command in `tooling/fdc_cli.py`.
    rule_id: fdc-state-transitions
  - description: 'Phase 1 (Deconstruction & Contextualization): The agent must ingest
      the task, query historical logs, identify entities using the symbol map, and
      analyze impact using the dependency graph.'
    enforcement: Procedural step guided by the agent's core logic, using artifacts
      in `logs/` and `knowledge_core/`.
    rule_id: phase1-deconstruction
  - description: 'Phase 2 (Planning & Self-Correction): The agent must generate a
      granular plan, lint it using the FDC toolchain, cite evidence for its steps,
      and perform a critical review.'
    enforcement: The `lint` command in `tooling/fdc_cli.py` is a mandatory pre-flight
      check.
    rule_id: phase2-planning
  - description: 'Phase 3 (Execution & Structured Logging): The agent must execute
      the validated plan and log every action according to the `LOGGING_SCHEMA.md`.'
    enforcement: Logging is performed by the agent's action execution wrapper.
    rule_id: phase3-execution
  - description: 'Phase 4 (Pre-Submission Post-Mortem): The agent must formally close
      the task using the `close` command and complete the generated post-mortem report.'
    enforcement: The `close` command in `tooling/fdc_cli.py` initiates this phase.
    rule_id: phase4-post-mortem
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

### AORP-HEADER

Defines the identity and versioning of the Advanced Orientation and Research Protocol (AORP).

**Rules:**

- `aorp-identity`: The governing protocol set is identified as the Advanced Orientation and Research Protocol (AORP)....
- `aorp-versioning`: The official protocol version is tracked in the VERSION file in the repository root, following Seman...

### BEST-PRACTICES-001

A set of best practices derived from observing successful, data-driven workflow patterns.

**Rules:**

- `verify-after-write`: After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_blo...

### CFDC-PROTOCOL-001

Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.

**Rules:**

- `hierarchical-planning-via-call-plan`: Plans may execute other plans as sub-routines using the 'call_plan <path_to_plan>' directive. This e...
- `max-recursion-depth`: To ensure decidability, the plan execution stack must not exceed a system-wide constant, MAX_RECURSI...

### DECIDABILITY-CONSTRAINTS-001

Ensures all development processes are formally decidable and computationally tractable.

**Rules:**

- `non-turing-completeness`: The agent's planning and execution language is, by design, not Turing-complete. This is a fundamenta...
- `bounded-recursion`: The agent MUST NOT generate plans that involve recursion or self-invocation. A plan cannot trigger a...
- `fsm-adherence`: All plans must be valid strings in the language defined by the tooling/fdc_fsm.json Finite State Mac...

### FDC-PROTOCOL-001

Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.

**Rules:**

- `fdc-entry-point`: The AORP cascade is the mandatory entry point to every FDC....
- `fdc-state-transitions`: The FDC is a Finite State Machine (FSM) formally defined in `tooling/fdc_fsm.json`. Plans must be va...
- `phase1-deconstruction`: Phase 1 (Deconstruction & Contextualization): The agent must ingest the task, query historical logs,...
- ... and 3 more rules

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
