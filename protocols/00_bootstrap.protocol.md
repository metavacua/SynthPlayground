# Protocol: Agent Bootstrap

**Rule `bootstrap-load-agents-md`**: On task start, the agent must read and parse `AGENTS.md` from the repository root before formulating a plan. This is the first and highest-priority action.

**Rule `bootstrap-scan-for-documents`**: After processing `AGENTS.md`, the agent should perform a scan of the repository for document files that could contain relevant information. The agent will incorporate the summarized information into its understanding of the project and use it to inform the planning process.