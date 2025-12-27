# AGENTS.md

**Directory:** `/protocols/chc/bootstrap`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Default protocol set for unmapped directories

## Protocols

This AGENTS.md file contains 2 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Default protocol set for unmapped directories
directory: /protocols/chc/bootstrap
generatedAt: '2025-12-27T01:58:32.628197Z'
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

```

## Protocol Summary

### BEST-PRACTICES-001

A set of best practices derived from observing successful, data-driven workflow patterns.

**Rules:**

- `verify-after-write`: After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_blo...

### NON-COMPLIANCE-PROTOCOL-001

A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.

**Rules:**

- `non-compliance-definition`: Defines non-compliance as a violation of any rule, convention, or procedure in AGENTS.md or its sour...
- `non-compliance-direct-editing`: Prohibits the direct editing of build artifacts like AGENTS.md or README.md. Changes must be made to...
- `non-compliance-test-procedure`: Requires adherence to all documented testing procedures before submitting changes....
- ... and 2 more rules

## Notes

*This AGENTS.md file is a build artifact. Do not edit directly.*
*Make changes to source files in `protocols/` directory and regenerate.*

## Build Instructions

To regenerate this file, run:
```bash
python3 tooling/builder.py --target agents-md
```
