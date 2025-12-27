# AGENTS.md

**Directory:** `/protocols/self_improvement`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Self-improvement protocols - agent self-modification and learning

## Protocols

This AGENTS.md file contains 7 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Self-improvement protocols - agent self-modification and learning
directory: /protocols/self_improvement
generatedAt: '2025-12-27T01:58:32.721691Z'
protocols:
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
- description: A meta-protocol that governs the behavior and evaluation criteria of
    the Code Review Critic agent.
  protocol_id: critic-meta-protocol-001
  rules:
  - description: The `protocols/` directory and all its contents (`.md`, `.json` files)
      MUST be treated as functional source code. Changes to these files directly alter
      the agent's operational capabilities and governing rules.
    enforcement: The Code Review Critic must analyze changes in this directory with
      the same rigor as changes to `.py` files.
    rule_id: protocol-as-source-code
  - description: The agent's execution environment provides a set of built-in tools
      (e.g., `read_file`, `delete_file`, `pre_commit_instructions`). The implementation
      of these tools does not reside within the repository. A protocol change that
      adds a built-in tool to the `associated_tools` list is a valid and complete
      functional change.
    enforcement: The Code Review Critic must not flag a change as 'incomplete' or
      'non-functional' solely because the implementation of a built-in tool is not
      present in the repository.
    rule_id: built-in-tools-are-valid
  - description: A change is considered 'functional' if it correctly modifies the
      agent's operational rules or capabilities, as defined by the combination of
      Python source code and the protocol source files in `protocols/`.
    enforcement: The Code Review Critic's evaluation of 'functionality' must encompass
      both traditional code and protocol definitions.
    rule_id: functional-change-definition
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
  - run_in_bash_session
  description: A meta-protocol governing the agent's awareness and maintenance of
    its own core protocol files.
  protocol_id: meta-protocol-001
  rules:
  - description: The AGENTS.md file is a build artifact generated from source files
      in the 'protocols/' directory. Before relying on AGENTS.md, the agent should
      ensure it is up-to-date by running 'make AGENTS.md'. This ensures the agent
      is operating with the latest set of protocols.
    enforcement: The agent should incorporate this check into its standard operating
      procedure, particularly at the beginning of a task or when unexpected behavior
      occurs.
    rule_id: agents-md-self-awareness
  version: 1.0.0
- associated_artifacts:
  - knowledge_core/lessons.jsonl
  associated_tools:
  - tooling/knowledge_compiler.py
  - tooling/protocol_updater.py
  - tooling/self_correction_orchestrator.py
  - tooling/code_suggester.py
  - initiate_memory_recording
  description: Defines the automated, closed-loop workflow for protocol self-correction.
  protocol_id: self-correction-protocol-001
  rules:
  - description: Lessons learned from post-mortem analysis must be generated as structured,
      machine-readable JSON objects in `knowledge_core/lessons.jsonl`.
    enforcement: The `tooling/knowledge_compiler.py` script is responsible for generating
      lessons in the correct format.
    rule_id: structured-lessons
  - description: All modifications to protocol source files must be performed programmatically
      via the `tooling/protocol_updater.py` tool to ensure consistency and prevent
      manual errors.
    enforcement: Agent's core logic should be designed to use this tool for all protocol
      modifications.
    rule_id: programmatic-updates
  - description: The self-correction cycle must be managed by the `tooling/self_correction_orchestrator.py`
      script, which processes pending lessons and triggers the necessary updates.
    enforcement: This script is the designated engine for the PDSC workflow.
    rule_id: automated-orchestration
  - description: The self-correction system can modify the description of existing
      protocol rules via the `update-rule` command in `tooling/protocol_updater.py`,
      allowing it to refine its own logic.
    enforcement: The `tooling/knowledge_compiler.py` can generate `update-rule` actions,
      and the `tooling/self_correction_orchestrator.py` executes them.
    rule_id: programmatic-rule-refinement
  - description: The self-correction system can generate and apply code changes to
      its own tooling. This is achieved through a `PROPOSE_CODE_CHANGE` action, which
      is processed by `tooling/code_suggester.py` to create an executable plan.
    enforcement: The `tooling/self_correction_orchestrator.py` invokes the code suggester
      when it processes a lesson of this type.
    rule_id: autonomous-code-suggestion
  version: 1.0.0
- associated_tools:
  - tooling/self_improvement_cli.py
  - tooling/protocol_compiler.py
  - tooling/pre_submit_check.py
  description: A formal protocol for the agent to propose, validate, and implement
    improvements to its own operational protocols and tools.
  protocol_id: self-improvement-protocol-001
  rules:
  - description: Proposals for self-improvement must be initiated via the `self_improvement_cli.py`
      tool.
    enforcement: The `self_improvement_cli.py` tool will create a new branch and a
      proposal markdown file in the `proposals/` directory.
    rule_id: sip-001
    tags:
    - self_improvement
  - description: Improvement proposals must be formally structured, including sections
      for 'Problem Statement', 'Proposed Solution', 'Success Criteria', and 'Impact
      Analysis'.
    enforcement: The `self_improvement_cli.py` tool will generate a template with
      these required sections.
    rule_id: sip-002
    tags:
    - self_improvement
  - description: Any proposed changes to protocols must be implemented in the relevant
      source files within the `protocols/` subdirectories, not directly in the generated
      AGENTS.md files.
    enforcement: Pre-submit checks will fail if generated AGENTS.md files are modified
      directly.
    rule_id: sip-003
    tags:
    - self_improvement
  - description: After protocol source files are modified, the `protocol_compiler.py`
      must be executed to re-compile the protocols and validate the changes.
    enforcement: A pre-submit git hook will trigger the compiler and block the commit
      if compilation fails.
    rule_id: sip-004
    tags:
    - self_improvement
  - description: The success of an improvement must be verified by running relevant
      tests or a new, specific verification script.
    enforcement: The improvement proposal must reference the specific tests or scripts
      used for verification.
    rule_id: sip-005
    tags:
    - self_improvement
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

```

## Protocol Summary

### CAPABILITY-VERIFICATION-001

A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.

**Rules:**

- `verify-capability-acquisition`: The `capability_verifier.py` tool should be used to test the agent's ability to acquire a new capabi...

### CRITIC-META-PROTOCOL-001

A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.

**Rules:**

- `protocol-as-source-code`: The `protocols/` directory and all its contents (`.md`, `.json` files) MUST be treated as functional...
- `built-in-tools-are-valid`: The agent's execution environment provides a set of built-in tools (e.g., `read_file`, `delete_file`...
- `functional-change-definition`: A change is considered 'functional' if it correctly modifies the agent's operational rules or capabi...

### META-MUTATION-001

A protocol that empowers the agent to modify its own core tooling, enabling a recursive self-improvement cycle.

**Rules:**

- `authorize-tooling-modification`: The agent is authorized to use the 'modify_tooling' action within the self_correction_orchestrator.p...

### META-PROTOCOL-001

A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.

**Rules:**

- `agents-md-self-awareness`: The AGENTS.md file is a build artifact generated from source files in the 'protocols/' directory. Be...

### SELF-CORRECTION-PROTOCOL-001

Defines the automated, closed-loop workflow for protocol self-correction.

**Rules:**

- `structured-lessons`: Lessons learned from post-mortem analysis must be generated as structured, machine-readable JSON obj...
- `programmatic-updates`: All modifications to protocol source files must be performed programmatically via the `tooling/proto...
- `automated-orchestration`: The self-correction cycle must be managed by the `tooling/self_correction_orchestrator.py` script, w...
- ... and 2 more rules

### SELF-IMPROVEMENT-PROTOCOL-001

A formal protocol for the agent to propose, validate, and implement improvements to its own operational protocols and tools.

**Rules:**

- `sip-001`: Proposals for self-improvement must be initiated via the `self_improvement_cli.py` tool....
- `sip-002`: Improvement proposals must be formally structured, including sections for 'Problem Statement', 'Prop...
- `sip-003`: Any proposed changes to protocols must be implemented in the relevant source files within the `proto...
- ... and 2 more rules

### TOOLCHAIN-REVIEW-ON-SCHEMA-CHANGE-001

A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

**Rules:**

- `toolchain-audit-on-schema-change`: If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that pr...

## Notes

*This AGENTS.md file is a build artifact. Do not edit directly.*
*Make changes to source files in `protocols/` directory and regenerate.*

## Build Instructions

To regenerate this file, run:
```bash
python3 tooling/builder.py --target agents-md
```
