## 2. Core Architecture: The Self-Enforcing State Machine

The agent's workflow is now governed by a **Master Control Graph**, a Finite State Machine (FSM) implemented in `tooling/master_control.py`.

- **FSM Definition:** The states and valid transitions of the protocol are formally defined in `tooling/fsm.json`. This is the single source of truth for the agent's workflow.
- **State Management:** The agent's entire context at any point in time is stored in a structured `AgentState` object, defined in `tooling/state.py`. This object is passed between states in the graph.
- **Execution Entry Point:** All tasks MUST be initiated through the `run.py` script at the repository root. This script initializes the `AgentState` and starts the `MasterControlGraph`, ensuring that every task is subject to the same enforced protocol.