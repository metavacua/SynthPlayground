# Subject: Jules Agent Protocol v4.0

## 1. Objective
To define a robust, interactive, resource-bounded, and self-enforcing protocol for all agent operations. This protocol is implemented as a state machine in code that is driven by an external control loop, ensuring that the agent is an active participant in a stable and auditable workflow.

## 2. Core Architecture: The Interactive State Machine

The agent's workflow is governed by a **Master Control Graph**, an FSM implemented in `tooling/master_control.py`. This architecture is designed to be interactive and safe.

### 2.1. Core Principles

- **Externalized Control Loop:** The FSM is advanced one step at a time by an external process (the agent's core execution loop). The `MasterControlGraph` exposes a `step(state)` method, which executes the logic for the current state and returns the updated state. This makes the process interactive and allows the agent to perform actions between FSM transitions.
- **Resource Bounding:** The protocol treats stability as a primary design goal. The `AgentState` tracks resource consumption (e.g., tool calls, tokens), and the `MasterControlGraph` is configured with safety limits. If a limit is about to be exceeded, the graph preemptively halts and transitions to an `ERROR` state.
- **Stateful Context:** The agent's entire context is stored in a structured `AgentState` object (`tooling/state.py`), which includes the current FSM state. This object is passed to and from the `step` method, making the graph itself stateless between calls.

### 2.2. FSM Definition
The states and valid transitions of the protocol are formally defined in `tooling/fsm.json`. This is the single source of truth for the agent's workflow, programmatically enforced by the `MasterControlGraph`.

## 3. The Finite Development Cycle (FDC) as an Interactive FSM

The FDC is implemented as a sequence of states in the Master Control Graph. An external loop drives the agent through these states by repeatedly calling the `step` method.

### State: `START`
- **Action:** The initial state. The first call to `step` transitions the agent to the `ORIENTING` state.

### State: `ORIENTING`
- **Action:** The `do_orientation` node is executed. This node programmatically performs the mandatory L1, L2, and L3 orientation steps.
- **Outcome:** On success, the state transitions to `PLANNING`.

### State: `PLANNING`
- **Action:** The `do_planning` node is executed. This node is responsible for ensuring a valid plan is set in the `AgentState`. For deep research (L4), this involves calling the `plan_deep_research` tool.
- **Outcome:** On success, the state transitions to `EXECUTING`.

### State: `EXECUTING`
- **Action:** The `do_execution` node is executed. This node iteratively executes one step of the agent's plan per call.
- **Outcome:** The FSM loops in this state until all plan steps are complete, then transitions to `POST_MORTEM`.

### State: `POST_MORTEM`
- **Action:** The `do_post_mortem` node is executed. This node ensures a final report is generated.
- **Outcome:** On success, the state transitions to `DONE`.

### State: `DONE` / `ERROR`
- **Action:** The terminal states. The workflow is complete. The final `AgentState` object provides a complete, auditable log.

## 4. Core Tooling
The Master Control Graph orchestrates a suite of tools to perform its functions:
- **`tooling/master_control.py`:** Implements the `step`-wise, resource-bounded FSM.
- **`tooling/research.py`:** Contains the `execute_research_protocol` function for all information gathering.
- **`tooling/research_planner.py`:** Contains the `plan_deep_research` function for L4 tasks.

This interactive, FSM-based architecture ensures that the protocol is not just a document, but the running code that governs my every action, making my development process transparent, robust, and reliable.