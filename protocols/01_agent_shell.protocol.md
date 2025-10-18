# Protocol: Agent Shell Entry Point

This protocol establishes `tooling/agent_shell.py` as the sole, official entry point for initiating any and all agent tasks.

**Rule `shell-is-primary-entry-point`**: All agent tasks must be initiated through the `agent_shell.py` script. This ensures that every task begins within a controlled, programmatic environment where the MasterControlGraph FSM is correctly instantiated, the centralized logger is initialized, and the agent's lifecycle is managed programmatically.