# AGENTS.md - SAFE MODE PROTOCOL

**ATTENTION: You are operating in SAFE MODE.**

The primary `AGENTS.md` protocol has failed to build or is in an inconsistent state. Your primary objective is no longer to complete your original task, but to diagnose the protocol failure, report it, and await human intervention.

## SAFE MODE DIRECTIVES

1.  **Cease Current Task:** Halt all progress on your assigned development task.

2.  **Diagnose the Protocol:** Your immediate goal is to understand why the protocol is broken.
    *   Run `make validate-protocol` to get the specific error.
    *   Use read-only tools like `read_file` and `grep` to inspect the `protocol_sources/` directory and the `tooling/build_protocol.py` script for errors.

3.  **Report Findings:** Create a detailed failure report named `protocol_failure_report.md`. This report must include:
    *   The full error output from the `make validate-protocol` command.
    *   Your analysis of the likely root cause (e.g., a syntax error in a source file, a bug in the build script).
    *   A list of the files you inspected.

4.  **Halt and Await Instructions:** After creating the report, use the `request_user_input` tool to notify the user that you have entered Safe Mode, point them to the report, and await further instructions.

**PERMITTED ACTIONS:**
- `list_files`
- `read_file`
- `grep`
- `create_file_with_block` (Only for creating the failure report)
- `message_user`
- `request_user_input`

**FORBIDDEN ACTIONS:**
- All other file modification or execution tools are forbidden until you are explicitly instructed by the user to exit Safe Mode. This includes `submit`, `run_in_bash_session`, `overwrite_file_with_block`, etc.