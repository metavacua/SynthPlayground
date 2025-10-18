# Agent Protocols

_This document is auto-generated from protocol source files. Do not edit it directly._

## Protocol: critic-meta-protocol-001
_A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent._

### Rules
- **protocol-as-source-code**: The `protocols/` directory and all its contents (`.md`, `.json` files) MUST be treated as functional source code. Changes to these files directly alter the agent's operational capabilities and governing rules.
  - *Enforcement: The Code Review Critic must analyze changes in this directory with the same rigor as changes to `.py` files.*
- **built-in-tools-are-valid**: The agent's execution environment provides a set of built-in tools (e.g., `read_file`, `delete_file`, `pre_commit_instructions`). The implementation of these tools does not reside within the repository. A protocol change that adds a built-in tool to the `associated_tools` list is a valid and complete functional change.
  - *Enforcement: The Code Review Critic must not flag a change as 'incomplete' or 'non-functional' solely because the implementation of a built-in tool is not present in the repository.*
- **functional-change-definition**: A change is considered 'functional' if it correctly modifies the agent's operational rules or capabilities, as defined by the combination of Python source code and the protocol source files in `protocols/`.
  - *Enforcement: The Code Review Critic's evaluation of 'functionality' must encompass both traditional code and protocol definitions.*

---

## Protocol: critic-reset-prohibition-001
_A specific, high-priority protocol that forbids the Code Review Critic agent from using the 'reset_all' tool._

### Rules
- **critic-no-reset**: The agent role-playing as the 'Code Review Critic' is explicitly forbidden from invoking the 'reset_all' tool under any circumstances. This is a critical safeguard to prevent the loss of work during the review process.
  - *Enforcement: This rule is enforced by its inclusion in the compiled AGENTS.md, which serves as the context for the Code Review Critic. The critic must be programmed to parse and adhere to this prohibition.*

### Associated Tools
- `reset_all`

---
