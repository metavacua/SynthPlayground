# AGENTS.md

**Directory:** `/protocols/external_apis`
**Generated:** 2025-12-27 01:58:32 UTC

## Description

External API protocols - API integration and management

## Protocols

This AGENTS.md file contains 6 operational protocols for this directory.

```yaml
'@context': protocols/protocol.context.jsonld
'@type': AgentContext
description: External API protocols - API integration and management
directory: /protocols/external_apis
generatedAt: '2025-12-27T01:58:32.690326Z'
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
- associated_artifacts:
  - knowledge_core/external_api_registry.json
  associated_tools:
  - tooling/external_api_client.py
  description: A protocol for standardized interaction with external agent APIs.
  protocol_id: external-api-integration-001
  rules:
  - description: A central registry of all approved external agent APIs MUST be maintained
      at 'knowledge_core/external_api_registry.json'.
    enforcement: The agent's core logic MUST consult this registry before making any
      calls to an external agent API.
    rule_id: external-api-registry
    tags:
    - external_apis
  - description: API keys for external services MUST be managed securely via environment
      variables.
    enforcement: The agent's external API client will be designed to read API keys
      from environment variables.
    rule_id: secure-api-key-management
    tags:
    - external_apis
  - description: A standardized client for interacting with external agent APIs MUST
      be implemented in 'tooling/external_api_client.py'.
    enforcement: All interactions with external agent APIs MUST be routed through
      this standardized client.
    rule_id: standardized-interaction-client
    tags:
    - external_apis
  version: 1.0.0
- associated_tools:
  - google_search
  - view_text_website
  description: A protocol for integrating with the Google Gemini API.
  protocol_id: gemini-api-integration-001
  rules:
  - description: The agent is authorized to use the Gemini API for advanced tasks.
    enforcement: The agent's core logic will be updated to include a 'Gemini API'
      tool.
    rule_id: gemini-api-access
    tags:
    - gemini
  - description: The agent must handle the Gemini API key securely.
    enforcement: The agent will access the Gemini API key via a secure, environment-variable-based
      mechanism.
    rule_id: gemini-api-key-security
    tags:
    - gemini
  - description: The agent must adhere to a strict sub-protocol when using the Gemini
      API's 'Computer Use' feature.
    enforcement: The 'Gemini API' tool will include a dedicated 'computer_use' module
      that implements these safeguards.
    rule_id: gemini-computer-use-protocol
    tags:
    - gemini
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

### EXTERNAL-API-INTEGRATION-001

A protocol for standardized interaction with external agent APIs.

**Rules:**

- `external-api-registry`: A central registry of all approved external agent APIs MUST be maintained at 'knowledge_core/externa...
- `secure-api-key-management`: API keys for external services MUST be managed securely via environment variables....
- `standardized-interaction-client`: A standardized client for interacting with external agent APIs MUST be implemented in 'tooling/exter...

### GEMINI-API-INTEGRATION-001

A protocol for integrating with the Google Gemini API.

**Rules:**

- `gemini-api-access`: The agent is authorized to use the Gemini API for advanced tasks....
- `gemini-api-key-security`: The agent must handle the Gemini API key securely....
- `gemini-computer-use-protocol`: The agent must adhere to a strict sub-protocol when using the Gemini API's 'Computer Use' feature....

### META-PROTOCOL-001

A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.

**Rules:**

- `agents-md-self-awareness`: The AGENTS.md file is a build artifact generated from source files in the 'protocols/' directory. Be...

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
