# Protocol: Global Tool Prohibitions

This protocol establishes a set of universal, non-negotiable prohibitions on the use of specific high-risk tools. These rules apply to all agents, roles, and operational contexts without exception.

**Rule `prohibit-reset-all`**: The `reset_all` tool is unconditionally and permanently forbidden.

**Rationale**: The `reset_all` tool is a legacy command that has been directly responsible for catastrophic task failures and complete loss of work. Its behavior is too destructive for a production environment. Safer, more granular tools for workspace management are available and must be used instead. This rule is a hard-coded safeguard.

**Enforcement**: The system's core orchestrator (`master_control.py`) programmatically blocks any attempt to call `reset_all` and will immediately terminate the task with a critical failure. This is not a suggestion for agent behavior; it is a system-level constraint.