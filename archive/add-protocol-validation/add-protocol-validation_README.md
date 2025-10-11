# Project Chimera: An Agent Self-Improvement Protocol

## Overview

This repository is a controlled environment for the self-experimentation and autonomous operation of the AI agent Jules. The primary objective is to develop, execute, and refine a robust, auditable, and self-enforcing protocol for performing complex software engineering tasks. The system is designed around a core principle: **the protocol is the code.**

## Core Architecture: The Integrated FSM Workflow

The agent's operation is governed by a unified workflow that integrates an interactive execution engine with a formal validation toolchain.

1.  **Execution Engine (`tooling/master_control.py`):** A Finite State Machine (FSM) that orchestrates the agent's actions. It is the heart of the system, driving the agent through the formal phases of a task: Orientation, Planning, Execution, and Post-Mortem.
2.  **Validation & Management Toolchain (`tooling/fdc_cli.py`):** A command-line interface that provides formal validation of plans and automated management of the task lifecycle. It enforces a strict, command-based structure for all plans.

These two components work together to ensure every task is executed in a controlled, predictable, and verifiable manner.

## The Unified Workflow

All tasks are initiated via `run.py` and follow this strict, automated protocol:

1.  **Orientation:** The FSM begins by running an automated orientation sequence to gather context about the repository and environment.
2.  **Planning:** The agent (Jules) analyzes the task and generates a formal, command-based plan in a `plan.txt` file.
3.  **Validation:** The `master_control.py` FSM calls the `fdc_cli.py validate` tool to formally verify the plan against the repository's protocol (`tooling/fdc_fsm.json`). Invalid plans are rejected, preventing execution.
4.  **Execution:** Upon successful validation, the FSM proceeds to execute the plan step-by-step. The FSM pauses at each step, waiting for a signal from the agent (`step_complete.txt`) before continuing. This allows the agent to perform the action and confirm its completion.
5.  **Post-Mortem:** Once all steps are complete, the FSM automatically calls `fdc_cli.py close` to generate a unique, timestamped post-mortem report in the `postmortems/` directory, formally closing the task.

## Key Components

-   **`AGENTS.md`**: The master protocol document (v3.0) that defines the high-level states and principles governing the agent's behavior.
-   **`run.py`**: The single entry point for initiating any new task, which starts the `MasterControlGraph`.
-   **`tooling/master_control.py`**: The interactive FSM that executes the task workflow.
-   **`tooling/fdc_cli.py`**: The CLI tool for validating plans and managing the task lifecycle.
-   **`tooling/fsm.json`**: The FSM definition for the *execution* engine (`master_control.py`).
-   **`tooling/fdc_fsm.json`**: The FSM definition for the *validation* engine (`fdc_cli.py`).
-   **`knowledge_core/`**: The agent's internal, auto-generated knowledge base, including dependency graphs and code symbols.
-   **`logs/activity.log.jsonl`**: A structured, machine-readable log of all agent actions, conforming to `LOGGING_SCHEMA.md`.
-   **`postmortems/`**: A directory containing all historical, uniquely-named post-mortem reports generated at the end of each task.