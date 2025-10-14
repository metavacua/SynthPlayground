# Agent Architecture Documentation

This document provides a detailed overview of the agent's architecture, including the Finite State Machine (FSM) that governs its behavior.

## Finite State Machine (FSM)

The agent's lifecycle is managed by a strict FSM. Below are the defined states and the transitions between them.

### States

- **START**: No description available.
- **ORIENTING**: No description available.
- **PLANNING**: Validates a given plan, parses it, and initializes the plan stack.
- **RESEARCHING**: Launches the background research process.
- **AWAITING_RESULT**: Checks for the result of the background research process.
- **EXECUTING**: No description available.
- **FINALIZING**: Handles the finalization of the task with agent-provided analysis.
- **AWAITING_SUBMISSION**: No description available.
- **ERROR**: No description available.

### Transitions

| Source State      | Trigger             | Destination State |
|-------------------|---------------------|-------------------|
| START             | begin_task          | ORIENTING         |
| ORIENTING         | orientation_succeeded | PLANNING          |
| ORIENTING         | orientation_failed  | ERROR             |
| PLANNING          | plan_op             | EXECUTING         |
| PLANNING          | planning_failed     | ERROR             |
| PLANNING          | research_requested  | RESEARCHING       |
| RESEARCHING       | research_started    | AWAITING_RESULT   |
| RESEARCHING       | research_failed     | ERROR             |
| AWAITING_RESULT   | wait                | AWAITING_RESULT   |
| AWAITING_RESULT   | result_ready        | PLANNING          |
| AWAITING_RESULT   | result_failed       | ERROR             |
| EXECUTING         | step_op             | EXECUTING         |
| EXECUTING         | all_steps_completed | FINALIZING        |
| EXECUTING         | execution_failed    | ERROR             |
| FINALIZING        | finalization_succeeded | AWAITING_SUBMISSION |
| FINALIZING        | finalization_failed | ERROR             |
| ERROR             | reorient            | ORIENTING         |

## Agent Shell (`tooling/agent_shell.py`)

The `agent_shell.py` script is the primary entry point for all agent tasks. It is responsible for initializing the agent's state, running the MasterControlGraph, and driving the FSM through its lifecycle.
