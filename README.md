# Project Chimera: An Agent Self-Improvement Protocol

## Overview

This repository is a controlled environment for the self-experimentation and autonomous operation of the AI agent Jules. The primary objective is to develop, execute, and refine a robust, auditable, and self-enforcing protocol for performing complex software engineering tasks. The system is designed around a core principle: **the protocol is the code.**

The project automatically generates this README, its system documentation, and its core operational protocols (`AGENTS.md`) from source. This ensures that the documentation and the codebase are always in sync.

## Core Architecture: The Integrated FSM Workflow

The agent's operation is governed by a unified workflow that integrates an interactive execution engine with a formal validation toolchain.

1.  **Execution Engine (`tooling/master_control.py`):** A Finite State Machine (FSM) that orchestrates the agent's actions. It is the heart of the system, driving the agent through the formal phases of a task.
2.  **Validation & Management Toolchain (`tooling/fdc_cli.py`):** A command-line interface that provides formal validation of plans and automated management of the task lifecycle.

These two components work together to ensure every task is executed in a controlled, predictable, and verifiable manner.

## Core Protocols

This project is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior. The key protocols are:

- **`aorp-header`**: Defines the identity and versioning of the Advanced Orientation and Research Protocol (AORP).
- **`agent-bootstrap-001`**: A foundational protocol that dictates the agent's initial actions upon starting any task.
- **`core-directive-001`**: The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).
- **`decidability-constraints-001`**: Ensures all development processes are formally decidable and computationally tractable.
- **`orientation-cascade-001`**: Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.
- **`fdc-protocol-001`**: Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.
- **`standing-orders-001`**: A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.
- **`best-practices-001`**: A set of best practices derived from observing successful, data-driven workflow patterns.
- **`meta-protocol-001`**: A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.
- **`cfdc-protocol-001`**: Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.
- **`self-correction-protocol-001`**: Defines the automated, closed-loop workflow for protocol self-correction.
- **`non-compliance-protocol-001`**: A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.
- **`pre-commit-protocol-001`**: Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission.
- **`reset-all-authorization-001`**: Requires explicit user authorization via a token file for the use of the destructive `reset_all` tool.
- **`research-protocol-001`**: A protocol for conducting systematic research using the integrated research toolchain.
- **`reset-all-prohibition-001`**: A high-priority protocol that unconditionally forbids the use of the `reset_all` tool.
- **`critic-meta-protocol-001`**: A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.
- **`critic-reset-prohibition-001`**: A specific, high-priority protocol that forbids the Code Review Critic agent from using the 'reset_all' tool.
- **`deep-research-cycle-001`**: A standardized, callable plan for conducting in-depth research on a complex topic.
- **`protocol-reset-all-pre-check-001`**: A protocol that mandates a pre-execution check for the `reset_all` tool to prevent unauthorized use.
- **`research-fdc-001`**: Defines the formal Finite Development Cycle (FDC) for conducting deep research.

## Key Components

- **`tooling/master_control.py`**:

  > The master orchestrator for the agent's lifecycle, governed by a Finite State Machine.\n  > \n  > This script, `master_control.py`, is the heart of the agent's operational loop.\n  > It implements a strict, protocol-driven workflow defined in a JSON file\n  > (typically `tooling/fsm.json`). The `MasterControlGraph` class reads this FSM\n  > definition and steps through the prescribed states, ensuring that the agent\n  > cannot deviate from the established protocol.\n  > \n  > The key responsibilities of this orchestrator include:\n  > - **State Enforcement:** Guiding the agent through the formal states of a task:\n  >   ORIENTING, PLANNING, EXECUTING, FINALIZING, and finally AWAITING_SUBMISSION.\n  > - **Plan Validation:** Before execution, it invokes the `fdc_cli.py` tool to\n  >   formally validate the agent-generated `plan.txt`, preventing the execution of\n  >   invalid or unsafe plans.\n  > - **Hierarchical Execution (CFDC):** It manages the plan execution stack, which\n  >   is the core mechanism of the Context-Free Development Cycle (CFDC). This\n  >   allows plans to call other plans as sub-routines via the `call_plan`\n  >   directive.\n  > - **Recursion Safety:** It enforces a `MAX_RECURSION_DEPTH` on the plan stack to\n  >   guarantee that the execution process is always decidable and will terminate.\n  > - **Lifecycle Management:** It orchestrates the entire lifecycle, from initial\n  >   orientation and environmental probing to the final post-mortem analysis and\n  >   compilation of lessons learned.\n  > \n  > The FSM operates by waiting for specific signals—typically the presence of\n  > files like `plan.txt` or `step_complete.txt`—before transitioning to the next\n  > state. This creates a robust, interactive loop where the orchestrator directs\n  > the high-level state, and the agent is responsible for completing the work\n  > required to advance that state.

- **`tooling/fdc_cli.py`**:

  > Provides the command-line interface for the Finite Development Cycle (FDC).\n  > \n  > This script is a core component of the agent's protocol, offering tools to ensure\n  > that all development work is structured, verifiable, and safe. It is used by both\n  > the agent to signal progress and the `master_control.py` orchestrator to\n  > validate the agent's plans before execution.\n  > \n  > The CLI provides several key commands:\n  > - `close`: Logs the formal end of a task, signaling to the orchestrator that\n  >   execution is complete.\n  > - `validate`: Performs a deep validation of a plan file against the FDC's Finite\n  >   State Machine (FSM) definition. It checks for both syntactic correctness (Is\n  >   the sequence of operations valid?) and semantic correctness (Does the plan try\n  >   to use a file before creating it?).\n  > - `analyze`: Reads a plan and provides a high-level analysis of its\n  >   characteristics, such as its computational complexity and whether it is a\n  >   read-only or read-write plan.\n  > - `lint`: A comprehensive "linter" that runs a full suite of checks on a plan\n  >   file, including `validate`, `analyze`, and checks for disallowed recursion.

- **`tooling/protocol_compiler.py`**:

  > Compiles source protocol files into unified, human-readable and machine-readable artifacts.\n  > \n  > This script is the engine behind the "protocol as code" principle. It discovers,\n  > validates, and assembles protocol definitions from a source directory (e.g., `protocols/`)\n  > into high-level documents like `AGENTS.md`.\n  > \n  > Key Functions:\n  > - **Discovery:** Scans a directory for source files, including `.protocol.json`\n  >   (machine-readable rules) and `.protocol.md` (human-readable context).\n  > - **Validation:** Uses a JSON schema (`protocol.schema.json`) to validate every\n  >   `.protocol.json` file, ensuring all protocol definitions are syntactically\n  >   correct and adhere to the established structure.\n  > - **Compilation:** Combines the human-readable markdown and the machine-readable\n  >   JSON into a single, cohesive Markdown file, embedding the JSON in code blocks.\n  > - **Documentation Injection:** Can inject other generated documents, like the\n  >   `SYSTEM_DOCUMENTATION.md`, into the final output at specified locations.\n  > - **Knowledge Graph Generation:** Optionally, it can process the validated JSON\n  >   protocols and serialize them into an RDF knowledge graph (in Turtle format),\n  >   creating a machine-queryable version of the agent's governing rules.\n  > \n  > This process ensures that `AGENTS.md` and other protocol documents are not edited\n  > manually but are instead generated from a validated, single source of truth,\n  > making the agent's protocols robust, verifiable, and maintainable.

- **`tooling/doc_generator.py`**:

  > Generates detailed system documentation from Python source files.\n  > \n  > This script scans specified directories for Python files, parses their\n  > Abstract Syntax Trees (ASTs), and extracts documentation for the module,\n  > classes, and functions. The output is a structured Markdown file.\n  > \n  > This is a key component of the project's self-documentation capabilities,\n  > powering the `SYSTEM_DOCUMENTATION.md` artifact in the `knowledge_core`.\n  > \n  > The script is configured via top-level constants:\n  > - `SCAN_DIRECTORIES`: A list of directories to search for .py files.\n  > - `OUTPUT_FILE`: The path where the final Markdown file will be written.\n  > - `DOC_TITLE`: The main title for the generated documentation file.\n  > \n  > It uses Python's `ast` module to reliably parse source files without\n  > importing them, which avoids issues with dependencies or script side-effects.

- **`tooling/protocol_auditor.py`**:

  > Audits the agent's behavior against its governing protocols and generates a report.\n  > \n  > This script performs a comprehensive analysis to ensure the agent's actions,\n  > as recorded in the activity log, align with the defined protocols in AGENTS.md.\n  > It serves as a critical feedback mechanism for maintaining operational integrity.\n  > The final output is a detailed `audit_report.md` file.\n  > \n  > The auditor performs three main checks:\n  > 1.  **`AGENTS.md` Source Check:** Verifies if the `AGENTS.md` build artifact is\n  >     potentially stale by comparing its modification time against the source\n  >     protocol files in the `protocols/` directory.\n  > 2.  **Protocol Completeness:** It cross-references the tools used in the log\n  >     (`logs/activity.log.jsonl`) against the tools defined in `AGENTS.md` to find:\n  >     - Tools used but not associated with any formal protocol.\n  >     - Tools defined in protocols but never used in the log.\n  > 3.  **Tool Centrality:** It conducts a frequency analysis of tool usage to\n  >     identify which tools are most critical to the agent's workflow.\n  > \n  > The script parses all embedded JSON protocol blocks within `AGENTS.md` and reads\n  > from the standard `logs/activity.log.jsonl` log file, providing a reliable and\n  > accurate audit.

- **`tooling/self_improvement_cli.py`**:

  > Analyzes agent activity logs to identify opportunities for self-improvement.\n  > \n  > This script is a command-line tool that serves as a key part of the agent's\n  > meta-cognitive loop. It parses the structured activity log\n  > (`logs/activity.log.jsonl`) to identify patterns that may indicate\n  > inefficiencies or errors in the agent's workflow.\n  > \n  > The primary analysis currently implemented is:\n  > - **Planning Efficiency Analysis:** It scans the logs for tasks that required\n  >   multiple `set_plan` actions. A high number of plan revisions for a single\n  >   task can suggest that the initial planning phase was insufficient, the task\n  >   was poorly understood, or the agent struggled to adapt to unforeseen\n  >   challenges.\n  > \n  > By flagging these tasks, the script provides a starting point for a deeper\n  > post-mortem analysis, helping the agent (or its developers) to understand the\n  > root causes of the planning churn and to develop strategies for more effective\n  > upfront planning in the future.\n  > \n  > The tool is designed to be extensible, with future analyses (such as error\n  > rate tracking or tool usage anti-patterns) to be added as the system evolves.

## Build System & Usage

This project uses a `Makefile` to automate common development tasks.

-   `make build`: The main command. Generates all documentation (`README.md`, `SYSTEM_DOCUMENTATION.md`) and compiles all protocols (`AGENTS.md`, `SECURITY.md`).
-   `make test`: Runs the complete unit test suite.
-   `make format`: Formats all Python code using `black`.
-   `make lint`: Lints all Python code using `flake8`.
-   `make clean`: Removes all generated artifacts.