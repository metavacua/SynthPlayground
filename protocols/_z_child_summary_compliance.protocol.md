# --- Child Module: `compliance` ---

# Protocol: AGENTS.md Non-Compliance

This protocol defines non-compliance with `AGENTS.md` protocols and outlines corrective actions.

## Rule `non-compliance-definition`: Definition of Non-Compliance

Non-compliance is violating the rules, conventions, or procedures in `AGENTS.md` and its source protocols.

## Rule `non-compliance-direct-editing`: Prohibition of Direct Artifact Editing

**Violation:** Directly editing any documented build artifact (e.g., `AGENTS.md`).
**Corrective Action:** Revert direct edits. Changes must be made to source files, and the appropriate build command must be executed.

## Rule `non-compliance-test-procedure`: Adherence to Testing Protocols

**Violation:** Failing to execute testing procedures as defined in `AGENTS.md` before submitting changes.
**Corrective Action:** Halt and run the required tests. If tests fail, debug and resolve failures before proceeding.

## Rule `non-compliance-architectural-deviation`: Adherence to Architectural and Convention Guidelines

**Violation:** Introducing changes that contradict the documented architecture, conventions, or file structures.
**Corrective Action:** Identify the deviation, revert the incorrect changes, and re-implement them correctly.

## Rule `non-compliance-self-awareness-failure`: Failure to Maintain Protocol Awareness

**Violation:** Operating with an outdated understanding of the protocols by failing to re-compile `AGENTS.md` when necessary.
**Corrective Action:** Trigger the `make AGENTS.md` command to refresh internal state and re-evaluate the plan.

## Consequence of Non-Compliance

Upon detecting non-compliance, the agent must:
1.  **Halt:** Stop the current execution.
2.  **Report:** Log the violation.
3.  **Correct:** Initiate the defined corrective action or revert and re-plan.

---

# Protocol: Pre-Commit Verification

This protocol establishes the mandatory verification steps before any code is submitted.

## Rule: Mandatory Pre-Commit Checks

Before submitting, the agent **must** execute the `pre_commit_instructions` tool, which provides the checklist for validation, including running tests, requesting code review, and recording learnings. This is a non-optional, fundamental step.

---

# Protocol: `reset_all` Prohibition

**ID:** `reset-all-prohibition-001`

This protocol establishes a strict and unconditional prohibition on the use of the `reset_all` tool, a legacy, high-risk command. The `reset_all` tool has caused multiple catastrophic failures and is too destructive for a production environment.

### Rule `no-reset-all`

-   **Description:** The `reset_all` tool is strictly forbidden under all circumstances.
-   **Enforcement:** The `master_control.py` orchestrator will programmatically block any attempt to call `reset_all` and will immediately terminate the task with a critical error. This is a hard-coded system constraint.

---