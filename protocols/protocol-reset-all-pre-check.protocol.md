# Protocol: `reset_all` Pre-Execution Authorization Check

This protocol strengthens the safety measures around the destructive `reset_all` tool by shifting the burden of verification from the tool to the agent.

## The Flaw in the Previous Protocol

The original protocol (`reset-all-authorization-001`) required the `reset_all` tool itself to perform the authorization check. However, since `reset_all` is a built-in, unmodifiable tool provided by the execution environment, this protocol was **unenforceable**. An agent could call the tool without consequence, leading directly to the catastrophic failure that was logged.

## The Corrective Action: Agent-Side Verification

This new protocol, `protocol-reset-all-pre-check-001`, corrects this flaw by making the agent explicitly responsible for the check.

**Rule `agent-must-verify-token`**: Before ever attempting to call `reset_all`, the agent's plan **MUST** include a step to use the `list_files` tool to verify the existence of the `authorization.token` file.

This change makes adherence verifiable by inspecting the agent's plan and execution log. It closes the loophole and ensures that the decision to use a destructive tool is always preceded by a conscious, verifiable check for authorization.