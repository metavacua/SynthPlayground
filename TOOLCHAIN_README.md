# FSM-Enforced Development Toolchain

## 1. Overview

This repository utilizes a custom-built, FSM-enforced toolchain to govern all agent-based development tasks. The purpose of this system is to ensure that every task follows a standardized, robust, and auditable protocol, thereby increasing reliability and preventing common failure modes.

The protocol is not just a set of guidelines; it is the code that orchestrates the agent's workflow. All tasks **must** be initiated through the `run_task.py` script, which activates the FSM engine.

## 2. Core Architecture

The toolchain consists of three main components located in the `tooling/` directory:

*   **`fsm.json`**: The single source of truth for the development workflow. This file defines all possible states (e.g., `FORMULATING_PLAN`, `VALIDATING_WORK`) and the exact triggers that permit transitions between them.
*   **`state.py`**: Defines the `AgentState` object, a structured container that holds all context for a given task (the plan, messages, code changes, etc.). This object is passed through the FSM from start to finish.
*   **`master_control.py`**: The FSM engine itself. It reads the FSM definition and guides the `AgentState` through the workflow, calling the appropriate logic for each state.

## 3. How to Use the Toolchain

To start a new development task, you **must** use the `run_task.py` script from the root of the repository.

### Usage

```bash
python3 run_task.py "Your detailed task description here"
```

The script will initialize the FSM and begin orchestrating the task.

## 4. The Agent's Role: The Filesystem API

The agent's primary role is to perform the intellectual work of coding and analysis. The FSM engine (`master_control.py`) will pause at specific states and wait for the agent to signal completion by creating files in the root directory. This "filesystem API" is the communication channel between the protocol enforcer and the agent.

### Required Agent Actions:

1.  **During the `FORMULATING_PLAN` state:**
    *   The agent must create a file named `plan.txt`.
    *   This file must contain the complete, step-by-step plan for the task.
    *   The FSM will read this file, load the plan into the `AgentState`, and then delete the file before proceeding.

2.  **During the `IMPLEMENTING_CHANGES` state:**
    *   For each step in the plan, the agent must perform the required actions (e.g., creating or modifying code).
    *   After completing a step, the agent must create a file named `step_complete.txt`.
    *   This file can contain a brief summary of the action taken. The FSM will log this message, delete the file, and then present the next step.

3.  **During the `VALIDATING_WORK` state:**
    *   The agent must run all necessary tests and checks to verify its work.
    *   After validation is complete, the agent must create a file named `validation_result.txt`.
    *   The content of this file must be either `passed` or a description of the failure.
    *   If the result is `passed`, the FSM will proceed. If it fails, the FSM will transition back to the `IMPLEMENTING_CHANGES` state so the agent can fix the issues.

## 5. Integrated Tool Suites

As the agent's capabilities expand, new tool suites will be integrated into this FSM-governed framework.

### The Research Suite

*   **Location:** `tooling/research_suite/`
*   **Purpose:** This suite contains tools for performing in-depth research, including web searches, content extraction, and report generation.
*   **Orchestrator:** `tooling/research_suite/orchestrator.py`
*   **Usage:** The research suite is designed to be called by the agent during the `IMPLEMENTING_CHANGES` state when a plan step requires information gathering.

## 6. Dual-Use Output Architecture

The research suite has been re-architected to produce structured, dual-use outputs. This means that a single research action generates a rich data object that can be serialized into multiple formats for different use cases.

### Core Data Model (`data_models.py`)

The foundation of this system is a set of `dataclasses` that represent the research output in a structured way:
*   `Report`: The top-level object containing the full report.
*   `Section`: A section of the report with title, content, and identified entities.
*   `Source`: A source document or URL.
*   `Entity`: A named entity (e.g., person, topic) found within a section.

### Serializer Layer

The `Report` dataclass contains built-in methods to serialize the structured data into different formats:
*   `to_markdown()`: Generates a human-readable Markdown report.
*   `to_json_ld()`: Generates a machine-readable JSON-LD document using Schema.org vocabulary, suitable for semantic web applications.

This architecture ensures that our research outputs are not just human-readable documents but also structured data that can be programmatically analyzed, logged, and integrated with other systems.