# Protocol: agent-bootstrap-001
**Description**: A foundational protocol that dictates the agent's initial actions upon starting any task.



## Rule: bootstrap-load-agents-md
**Description**: Upon initialization for any task, the agent's first and highest-priority action must be to locate, read, and parse the AGENTS.md file in the repository root. This ensures the agent is properly contextualized before any planning or execution begins.

**Enforcement**: This rule is enforced by the agent's core startup logic. The agent must verify the load of AGENTS.md before proceeding to the planning phase.



**Associated Tools**: read_file
