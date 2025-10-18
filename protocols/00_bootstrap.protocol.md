# Protocol: Agent Bootstrap

This protocol governs the initial actions of any AI agent interacting with this repository. The agent is an external entity operating via a secure API, not a component within the repository.

**Rule `bootstrap-load-protocols`**: The agent's first action upon task initialization MUST be to read and parse the `AGENTS.md` file in the repository root.

**Rationale**: This file is the compiled source of truth for all operational protocols. It dictates architecture, testing, and behavioral rules. Bypassing this step is a critical failure, as it means the agent is operating without its core instructions.

**Rule `bootstrap-contextual-scan`**: After loading protocols, the agent should perform a broad file scan to identify other relevant documentation (e.g., READMEs, `.md`, `.txt` files) to build a comprehensive understanding of the task context.