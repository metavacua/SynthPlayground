# Agent Protocols

_This document is auto-generated from protocol source files. Do not edit it directly._

## Protocol: best-practices-001
_A set of best practices derived from observing successful, data-driven workflow patterns._

### Rules
- **verify-after-write**: After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_block`, `replace_with_git_merge_diff`), the agent MUST use a subsequent read-only tool (`read_file`, `list_files`, `grep`) to verify that the action was executed successfully and had the intended effect. A plan step should only be marked as complete after this verification.
  - *Enforcement: This is a core operational discipline. Future tooling, such as a trace validator, could enforce this by analyzing the execution log against this protocol.*

### Associated Tools
- `create_file_with_block`
- `overwrite_file_with_block`
- `replace_with_git_merge_diff`
- `delete_file`
- `read_file`
- `list_files`
- `grep`

---

## Protocol: meta-protocol-001
_A meta-protocol governing the agent's awareness and maintenance of its own core protocol files._

### Rules
- **agents-md-self-awareness**: The AGENTS.md file is a build artifact generated from source files in the 'protocols/' directory. Before relying on AGENTS.md, the agent should ensure it is up-to-date by running 'make AGENTS.md'. This ensures the agent is operating with the latest set of protocols.
  - *Enforcement: The agent should incorporate this check into its standard operating procedure, particularly at the beginning of a task or when unexpected behavior occurs.*

### Associated Tools
- `run_in_bash_session`

---

## Protocol: non-compliance-protocol-001
_A protocol that defines non-compliance with AGENTS.md and specifies corrective actions._

### Rules
- **non-compliance-definition**: Defines non-compliance as a violation of any rule, convention, or procedure in AGENTS.md or its source protocols.
  - *Enforcement: This is a definitional rule. Enforcement is achieved through the agent's adherence to the specific non-compliance rules that follow.*
- **non-compliance-direct-editing**: Prohibits the direct editing of build artifacts like AGENTS.md or README.md. Changes must be made to source files, followed by a rebuild.
  - *Enforcement: Agent must revert direct edits and modify source files, then run the appropriate build command.*
- **non-compliance-test-procedure**: Requires adherence to all documented testing procedures before submitting changes.
  - *Enforcement: Agent must halt execution and run the required tests, debugging any failures before proceeding.*
- **non-compliance-architectural-deviation**: Forbids changes that contradict documented architectural patterns or coding conventions.
  - *Enforcement: Agent must revert non-compliant changes and re-implement them according to standards.*
- **non-compliance-self-awareness-failure**: Requires the agent to maintain an up-to-date understanding of protocols by recompiling AGENTS.md when necessary.
  - *Enforcement: Agent should run 'make AGENTS.md' to refresh its protocol knowledge and re-evaluate its plan.*

---

## Protocol: pre-commit-protocol-001
_Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission._

### Rules
- **pre-commit-instructions-mandate**: Before submitting changes, the agent MUST execute the `pre_commit_instructions` tool to receive the required sequence of validation steps (e.g., running tests, requesting code review).
  - *Enforcement: The agent's core logic should invoke this tool as the entry point to the pre-submission phase.*

### Associated Tools
- `pre_commit_instructions`
- `code_linter`

---

## Protocol: reset-all-prohibition-001
_A high-priority protocol that unconditionally forbids the use of the `reset_all` tool._

### Rules
- **no-reset-all**: The `reset_all` tool is strictly forbidden under all circumstances. It is a legacy tool that has been superseded by more granular and safer methods of workspace management. Its use is considered a critical failure.
  - *Enforcement: This rule is enforced by the `master_control.py` orchestrator, which will immediately terminate the workflow with an error if an attempt is made to call this tool.*

### Associated Tools
- `reset_all`

---
