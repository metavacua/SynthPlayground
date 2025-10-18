# Protocol: Agent Shell Entry Point

This protocol establishes the `agent_shell.py` script as the sole, official entry point for initiating any and all agent tasks.

## The Problem: Inconsistent Initialization

Prior to this protocol, there was no formally mandated entry point for the agent. This could lead to tasks being initiated through different scripts, potentially bypassing critical setup procedures like FSM initialization, logger configuration, and state management. This inconsistency makes the agent's behavior less predictable and harder to debug.

## The Solution: A Single, Enforced Entry Point

This protocol mandates the use of `tooling/agent_shell.py` for all task initiations.

**Rule `shell-is-primary-entry-point`**: All agent tasks must be initiated through the `agent_shell.py` script.

This ensures that every task begins within a controlled, programmatic environment where:
1.  The MasterControlGraph FSM is correctly instantiated and run.
2.  The centralized logger is initialized for comprehensive, structured logging.
3.  The agent's lifecycle is managed programmatically, not through fragile file-based signals.

By enforcing a single entry point, this protocol enhances the reliability, auditability, and robustness of the entire agent system.