# Protocol: `reset_all` Prohibition

**ID:** `reset-all-prohibition-001`

## 1. Description

This protocol establishes a strict and unconditional prohibition on the use of the `reset_all` tool. This tool is considered a legacy, high-risk command that is no longer permitted in any workflow.

## 2. Rationale

The `reset_all` tool has been the cause of multiple catastrophic failures, leading to the complete loss of work and the inability to complete tasks. Its behavior is too destructive and unpredictable for a production environment. More granular and safer tools are available for workspace management. This protocol serves as a hard-coded safeguard to prevent any future use of this tool.

## 3. Rules

### Rule `no-reset-all`

-   **Description:** The `reset_all` tool is strictly forbidden under all circumstances.
-   **Enforcement:** The `master_control.py` orchestrator will programmatically block any attempt to call `reset_all` and will immediately terminate the task with a critical error. This is not a rule for the agent to interpret, but a hard-coded system constraint.