# Protocol: Pre-Commit Verification

This protocol establishes the mandatory sequence of verification steps that must be performed before any code is submitted. Its purpose is to ensure that all changes meet a baseline level of quality, correctness, and review, preventing regressions and maintaining repository health.

## Rule: Mandatory Pre-Commit Checks

Before finalizing and submitting any work, the agent **must** execute the `pre_commit_instructions` tool. This tool acts as a procedural gateway, providing the specific, up-to-date checklist of actions required for validation. This typically includes:

1.  **Running all automated tests** to verify correctness.
2.  **Requesting a formal code review** to get critical feedback.
3.  **Recording key learnings** to contribute to the agent's long-term memory.

Adherence to this protocol is not optional. It is a fundamental step in the development lifecycle that safeguards the integrity of the codebase.
