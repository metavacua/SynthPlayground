# AGENTS.md

**Directory:** `/tooling/chomsky`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Default protocol set for unmapped directories

## Protocols

This AGENTS.md file contains 8 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Default protocol set for unmapped directories
directory: /tooling/chomsky
generatedAt: '2025-12-27T01:58:32.756019Z'
protocols:
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

### BEST-PRACTICES-001

A set of best practices derived from observing successful, data-driven workflow patterns.

**Rules:**

- `verify-after-write`: After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_blo...

### CAPABILITY-VERIFICATION-001

A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.

**Rules:**

- `verify-capability-acquisition`: The `capability_verifier.py` tool should be used to test the agent's ability to acquire a new capabi...

### FILE-INDEXING-001

A protocol for maintaining an up-to-date file index to accelerate tool performance.

**Rules:**

- `update-index-before-submit`: Before submitting any changes that alter the file structure (create, delete, rename), the agent MUST...

### META-MUTATION-001

A protocol that empowers the agent to modify its own core tooling, enabling a recursive self-improvement cycle.

**Rules:**

- `authorize-tooling-modification`: The agent is authorized to use the 'modify_tooling' action within the self_correction_orchestrator.p...

### NON-COMPLIANCE-PROTOCOL-001

A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.

**Rules:**

- `non-compliance-definition`: Defines non-compliance as a violation of any rule, convention, or procedure in AGENTS.md or its sour...
- `non-compliance-direct-editing`: Prohibits the direct editing of build artifacts like AGENTS.md or README.md. Changes must be made to...
- `non-compliance-test-procedure`: Requires adherence to all documented testing procedures before submitting changes....
- ... and 2 more rules

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
