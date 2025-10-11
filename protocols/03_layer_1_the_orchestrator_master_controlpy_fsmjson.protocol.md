### Layer 1: The Orchestrator (`master_control.py` & `fsm.json`)

The Orchestrator is the master Finite State Machine (FSM) that guides the agent through its entire lifecycle, from orientation to submission. It is not directly controlled by the agent's plan but rather directs the agent's state based on the successful completion of each phase.

**Key States (defined in `tooling/fsm.json`):**
*   `ORIENTING`: The initial state where the agent gathers context.
*   `PLANNING`: The state where the Orchestrator waits for the agent to produce a `plan.txt`.
*   `EXECUTING`: The state where the Orchestrator oversees the step-by-step execution of the validated plan.
*   `POST_MORTEM`: The state for finalizing the task and recording learnings.
*   `AWAITING_SUBMISSION`: The final state before the code is submitted.

**The Orchestrator's Critical Role in Planning:**
During the `PLANNING` state, the Orchestrator's most important job is to validate the agent-generated `plan.txt`. It does this by calling the FDC Toolchain's `lint` command. **A plan that fails this check will halt the entire process, preventing the agent from entering an invalid state.**