### STANDING ORDERS

1.  **Orchestrator is Sovereign:** The agent's lifecycle is governed by `master_control.py`. The agent's primary job is to provide a valid `plan.txt` when the Orchestrator enters the `PLANNING` state.
2.  **Toolchain is Law:** All plans must be valid according to the `fdc_cli.py lint` command. A valid plan is one that passes the Closure Mandate and is a valid string in the language defined by `fdc_fsm.json`.
3.  **Hierarchy is Structure:** The Orchestrator (`master_control.py`) validates the agent's plan using the FDC Toolchain (`fdc_cli.py`). This separation ensures a robust, verifiable, and decidable development process, preventing the system from executing paradoxical or non-terminating plans.