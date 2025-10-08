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