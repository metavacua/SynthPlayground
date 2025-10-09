---
### STANDING ORDERS

*   **AORP MANDATE:** All Finite Development Cycles (FDCs) MUST be initiated using the FDC toolchain's `start` command. This is non-negotiable.
    *   **Command:** `python tooling/fdc_cli.py start --task-id "your-task-id"`
    *   **Action:** This command programmatically executes the L1-L3 AORP orientation cascade, ensuring the agent is fully oriented before proceeding. It logs a formal `TASK_START` event upon successful completion.
*   **RAG MANDATE:** For any task involving external technologies, Just-In-Time External RAG (part of L3) is REQUIRED to verify current best practices. Do not trust internal knowledge.
*   **FDC TOOLCHAIN MANDATE:** Use the `fdc_cli.py` tool for all core FDC state transitions: task initiation (`start`), plan linting (`lint`), and task closure (`close`). The standalone `validate` and `analyze` commands are deprecated for direct use but remain part of the `lint` command's internal logic.