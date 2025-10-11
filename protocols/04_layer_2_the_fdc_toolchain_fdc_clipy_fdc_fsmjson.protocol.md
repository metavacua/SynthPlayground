### Layer 2: The FDC Toolchain (`fdc_cli.py` & `fdc_fsm.json`)

The FDC Toolchain is a set of utilities that the agent uses to structure its work and that the Orchestrator uses for validation. The toolchain is governed by its own FSM (`tooling/fdc_fsm.json`), which defines the legal sequence of commands *within a plan*.

#### **FDC Commands for Agent Use:**

**`start` - Task Initiation**
*   **Usage:** The first command the agent MUST issue upon receiving a task.
*   **Command:** `run_in_bash_session python3 tooling/fdc_cli.py start --task-id "your-task-id"`
*   **Function:** Logs the `TASK_START` event, formally beginning the development cycle.

**`lint` - Pre-Flight Plan Validation**
*   **Usage:** A command the agent can use to self-correct its own plan before finalizing it. The Orchestrator will *always* run this command on `plan.txt` as a mandatory check.
*   **Command:** `run_in_bash_session python3 tooling/fdc_cli.py lint <plan_file.txt>`
*   **Function:** Performs a comprehensive check against the low-level FSM:
    1.  **Closure Mandate:** Ensures the plan's final action is a call to the `close` command.
    2.  **FSM Validation:** Validates the sequence of agent tools against `tooling/fdc_fsm.json`.
    3.  **Semantic Validation:** Checks for errors like using a file before creating it.

**`close` - Task Closure**
*   **Usage:** The **last command** in any valid plan.
*   **Command:** `run_in_bash_session python3 tooling/fdc_cli.py close --task-id "your-task-id"`
*   **Function:** Logs `TASK_END`, generates a post-mortem template, and signals to the Orchestrator that plan execution is complete.
---