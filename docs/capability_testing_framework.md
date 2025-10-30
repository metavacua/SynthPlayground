# Capability Testing Framework

This document outlines a systematic approach to testing the integration between the agent's core capabilities and the specific tools and protocols of this repository. The goal is to ensure that the agent can effectively use the repository's tools and follow its established protocols, and to identify and address any gaps in this integration.

## Agent Built-in Tools

These are the tools that are part of the agent's core capabilities, provided by the underlying environment.

| Tool | Description |
|---|---|
| `list_files` | Lists files and directories. |
| `read_file` | Reads the content of a file. |
| `view_text_website` | Fetches the content of a website as plain text. |
| `set_plan` | Sets or updates the agent's plan. |
| `plan_step_complete` | Marks a plan step as complete. |
| `message_user` | Sends a message to the user. |
| `request_user_input` | Asks the user for input. |
| `submit` | Submits the current changes. |
| `delete_file` | Deletes a file. |
| `rename_file` | Renames or moves a file. |
| `grep` | Searches for a pattern in files. |
| `reset_all` | Resets the codebase to its original state. |
| `restore_file` | Restores a file to its original state. |
| `view_image` | Views an image from a URL. |
| `run_in_bash_session` | Runs a bash command. |
| `create_file_with_block` | Creates a new file with content. |
| `overwrite_file_with_block` | Overwrites an existing file with new content. |
| `replace_with_git_merge_diff` | Applies a git merge diff to a file. |
| `read_pr_comments` | Reads pull request comments. |
| `reply_to_pr_comments` | Replies to pull request comments. |
| `request_code_review` | Requests a code review. |
| `read_image_file` | Reads an image file from the local filesystem. |
| `frontend_verification_instructions` | Gets instructions for frontend verification. |
| `frontend_verification_complete` | Marks frontend verification as complete. |
| `google_search` | Performs a Google search. |
| `initiate_memory_recording` | Initiates memory recording. |
| `pre_commit_instructions` | Gets pre-commit instructions. |

## Repository-Specific Tools

These are the tools that are specific to this repository, located in the `tooling/` directory.

| Tool | Description |
|---|---|
| `tooling/builder.py` | The main build tool for the repository. |
| `tooling/auditor.py` | Runs comprehensive checks on the repository's health. |
| `tooling/protocol_compiler.py` | Compiles the protocol source files. |
| `tooling/capability_verifier.py` | Verifies the agent's capabilities. |
| `tooling/self_improvement_cli.py` | Initiates a self-improvement proposal. |
| `tooling/fdc_cli.py` | The command-line interface for the Finite Development Cycle. |

## Repository Protocols

These are the formal protocols that govern the agent's behavior, as defined in `AGENTS.md`.

| Protocol | Description |
|---|---|
| `dependency-management-001` | Ensures a reliable execution environment through formal dependency management. |
| `test-driven-development-001` | Enforces Test-Driven Development (TDD) practices. |
| `guardian-protocol-001` | A meta-protocol to ensure all autonomous actions are strategically sound and easily reviewable. |
| `pre-commit-protocol-001` | Defines the mandatory pre-commit checks. |
| `self-improvement-protocol-001` | A formal protocol for the agent to propose, validate, and implement improvements. |

## Capability Test Format

Capability tests are defined in YAML files located in the `capability_tests/` directory. Each file can contain one or more tests. The following structure must be used:

```yaml
- id: CPT-001
  description: A brief, human-readable description of the capability being tested.
  steps:
    - tool: tool_name
      args: [arg1, arg2]
      # ... other tool-specific parameters
  assertions:
    - tool: tool_name
      args: [arg1, arg2]
      # ... other assertion-specific parameters
      expected_output: |
        The expected output from the tool.
      expected_exit_code: 0
```

### Fields

*   `id`: A unique identifier for the test (e.g., `CPT-001`).
*   `description`: A brief, human-readable description of the capability being tested.
*   `steps`: A list of agent actions to be executed to set up and run the test.
    *   `tool`: The name of the tool to be used (e.g., `run_in_bash_session`, `create_file_with_block`).
    *   `args`: A list of arguments to be passed to the tool.
*   `assertions`: A list of agent actions to be executed to verify the outcome of the test.
    *   `tool`: The name of the tool to be used for the assertion.
    *   `args`: A list of arguments to be passed to the tool.
    *   `expected_output`: The expected output from the tool. This can be a multi-line string.
    *   `expected_exit_code`: The expected exit code from the tool.
