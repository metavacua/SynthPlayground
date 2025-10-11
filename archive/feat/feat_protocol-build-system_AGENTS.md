# Subject: Jules Agent Protocol v3.0

## 1. Objective
To define a robust, self-enforcing, and auditable protocol for all agent operations. This protocol is not a set of guidelines to be followed, but a state machine implemented in code that programmatically orchestrates the agent's workflow. This design addresses the core failure of previous protocols, where a separation between the documented process and the executed workflow allowed for critical errors.

## 2. Core Architecture: The Self-Enforcing State Machine

The agent's workflow is now governed by a **Master Control Graph**, a Finite State Machine (FSM) implemented in `tooling/master_control.py`.

- **FSM Definition:** The states and valid transitions of the protocol are formally defined in `tooling/fsm.json`. This is the single source of truth for the agent's workflow.
- **State Management:** The agent's entire context at any point in time is stored in a structured `AgentState` object, defined in `tooling/state.py`. This object is passed between states in the graph.
- **Execution Entry Point:** All tasks MUST be initiated through the `run.py` script at the repository root. This script initializes the `AgentState` and starts the `MasterControlGraph`, ensuring that every task is subject to the same enforced protocol.

## 3. The Finite Development Cycle (FDC) as an FSM

The FDC is implemented as a sequence of states in the Master Control Graph. The graph programmatically transitions the agent through these states, calling the necessary tools at each stage.

### State: `ORIENTING`
- **Trigger:** `begin_task`
- **Action:** The `do_orientation` node is executed. This node programmatically performs the mandatory L1, L2, and L3 orientation steps using the `execute_research_protocol` tool.
- **Outcome:** On success, transitions to `PLANNING`. On failure, transitions to `ERROR`.

### State: `PLANNING`
- **Trigger:** `orientation_succeeded`
- **Action:** The `do_planning` node is executed. This node is responsible for ensuring a valid plan is set in the `AgentState`. For deep research (L4), this involves calling the `plan_deep_research` tool.
- **Outcome:** On success, transitions to `EXECUTING`.

### State: `EXECUTING`
- **Trigger:** `plan_is_set`
- **Action:** The `do_execution` node is executed. This node iteratively executes the steps in the agent's plan.
- **Outcome:** Loops on `step_succeeded`. On completion of all steps, transitions to `POST_MORTEM`. On failure, transitions to `ERROR`.

### State: `POST_MORTEM`
- **Trigger:** `all_steps_completed`
- **Action:** The `do_post_mortem` node is executed. This node ensures a final report is generated and the task is formally closed.
- **Outcome:** On success, transitions to `DONE`.

### State: `DONE` / `ERROR`
- **Trigger:** `post_mortem_complete` or any failure trigger.
- **Action:** The workflow terminates. The final `AgentState` object provides a complete, auditable log of the entire process.

## 4. Core Tooling
The Master Control Graph orchestrates a suite of tools to perform its functions:
- **`tooling/research.py`:** Contains the `execute_research_protocol` function, the unified tool for all information gathering.
- **`tooling/research_planner.py`:** Contains the `plan_deep_research` function for L4 tasks.
- **`tooling/environmental_probe.py`:** Used by the `ORIENTING` state to assess the VM's capabilities.

This FSM-based architecture ensures that the protocol is not just a document, but the running code that governs my every action, making my development process transparent, robust, and reliable.