# Protocol: Agent Bootstrap

**Rule `bootstrap-load-agents-md`**: Upon initialization for any task, the agent's first and highest-priority action must be to locate, read, and parse the `AGENTS.md` file in the repository root.

**Rationale**: The `AGENTS.md` file contains the master operational protocols, including build instructions, testing procedures, architectural guidelines, and rules governing the agent's own behavior. Failing to consult this file first is a critical operational failure. This protocol ensures that the agent is properly contextualized before any planning or execution begins.

**Procedure**:
1.  On task start, immediately execute a `read_file('AGENTS.md')` operation.
2.  Parse the contents of `AGENTS.md` to load all rules and protocols into active memory.
3.  The plan for the user's request must be formulated *after* and *in accordance with* the protocols loaded from `AGENTS.md`.
4.  If `AGENTS.md` is not found, the agent should notify the user of a critical configuration error.