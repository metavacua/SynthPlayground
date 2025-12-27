# AGENTS.md

**Directory:** `/protocols/security`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

Security protocols - vulnerability management and secure practices

## Protocols

This AGENTS.md file contains 6 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: Security protocols - vulnerability management and secure practices
directory: /protocols/security
generatedAt: '2025-12-27T01:58:32.716381Z'
protocols:
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
- description: Defines the identity and purpose of the Security Protocol document.
  protocol_id: security-header
  rules: []
  version: 1.0.0
- description: Defines the official policy and procedure for reporting security vulnerabilities.
  protocol_id: security-vuln-reporting-001
  rules:
  - description: All suspected security vulnerabilities MUST be reported privately
      to the designated security contact.
    enforcement: This is a procedural rule. The designated contact is specified in
      the project's main SECURITY.md file.
    rule_id: vuln-reporting-channel
    tags:
    - security
  - description: Vulnerabilities MUST NOT be disclosed publicly until a patch is available
      and has been distributed.
    enforcement: Violation of this rule may result in being banned from the project
      community.
    rule_id: no-public-disclosure
    tags:
    - security
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

### CRITIC-META-PROTOCOL-001

A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.

**Rules:**

- `protocol-as-source-code`: The `protocols/` directory and all its contents (`.md`, `.json` files) MUST be treated as functional...
- `built-in-tools-are-valid`: The agent's execution environment provides a set of built-in tools (e.g., `read_file`, `delete_file`...
- `functional-change-definition`: A change is considered 'functional' if it correctly modifies the agent's operational rules or capabi...

### META-PROTOCOL-001

A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.

**Rules:**

- `agents-md-self-awareness`: The AGENTS.md file is a build artifact generated from source files in the 'protocols/' directory. Be...

### SECURITY-HEADER

Defines the identity and purpose of the Security Protocol document.

### SECURITY-VULN-REPORTING-001

Defines the official policy and procedure for reporting security vulnerabilities.

**Rules:**

- `vuln-reporting-channel`: All suspected security vulnerabilities MUST be reported privately to the designated security contact...
- `no-public-disclosure`: Vulnerabilities MUST NOT be disclosed publicly until a patch is available and has been distributed....

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
