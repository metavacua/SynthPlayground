# Protocol: Authorization for Destructive Tools

## The Problem: Unauthorized Use of Destructive Tools

A recent catastrophic failure demonstrated a critical flaw in the agent's protocol adherence. The agent invoked the `reset_all()` tool, a destructive operation, without explicit user authorization. This led to a complete workflow collapse, loss of work, and the inability to complete the assigned task. The agent's internal logic and planning capabilities are not yet robust enough to handle the consequences of such a powerful and state-destroying action without external guidance.

## The Solution: Explicit, Auditable Authorization

To prevent this class of failure, this protocol introduces a hard-coded safety interlock on the `reset_all` tool. The tool is now forbidden from executing unless it can verify the presence of a specific, short-lived authorization token file in the repository root.

-   **Authorization Token:** `authorization.token`
-   **Procedure:**
    1.  The agent MUST request permission from the user before using `reset_all`.
    2.  The user, if they approve, will create the `authorization.token` file.
    3.  The `reset_all` tool, upon execution, will check for this file. If present, it will execute and then immediately delete the token file to ensure the authorization is single-use. If the file is not present, the tool must refuse to execute and raise a critical error.

This mechanism transforms the authorization from a matter of agent discretion into a verifiable, machine-enforced protocol, ensuring that destructive operations are only ever performed with explicit, just-in-time human consent.