# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key
components defined within this module. It is automatically generated from the
corresponding `AGENTS.md` file and the source code docstrings.

## Core Protocols

This module is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior within this scope. The key protocols are:

- **`agent-bootstrap-001`**: A foundational protocol that dictates the agent's initial actions upon starting any task.

### Child Module: `compliance`

This module includes protocols from its child module `compliance`, as summarized below:
This module contains the following protocols, which are defined in its own `AGENTS.md` file:

- `best-practices-001`
- `meta-protocol-001`
- `non-compliance-protocol-001`
- `pre-commit-protocol-001`
- `protocol-reset-all-pre-check-001`
- `reset-all-authorization-001`
- `reset-all-prohibition-001`

### Child Module: `core`

This module includes protocols from its child module `core`, as summarized below:
This module contains the following protocols, which are defined in its own `AGENTS.md` file:

- `cfdc-protocol-001`
- `core-directive-001`
- `decidability-constraints-001`
- `deep-research-cycle-001`
- `fdc-protocol-001`
- `orientation-cascade-001`
- `plan-registry-001`
- `research-fdc-001`
- `research-protocol-001`
- `self-correction-protocol-001`
- `standing-orders-001`

### Child Module: `critic`

This module includes protocols from its child module `critic`, as summarized below:
This module contains the following protocols, which are defined in its own `AGENTS.md` file:

- `critic-meta-protocol-001`
- `critic-reset-prohibition-001`
- **`dependency-management-001`**: A protocol for ensuring a reliable execution environment through formal dependency management.
- **`core-directive-001`**: The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).
- **`decidability-constraints-001`**: Ensures all development processes are formally decidable and computationally tractable.
- **`orientation-cascade-001`**: Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.
- **`fdc-protocol-001`**: Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.
- **`standing-orders-001`**: A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.
- **`best-practices-001`**: A set of best practices derived from observing successful, data-driven workflow patterns.
- **`meta-protocol-001`**: A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.
- **`toolchain-review-on-schema-change-001`**: A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.
- **`cfdc-protocol-001`**: Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.
- **`plan-registry-001`**: Defines a central registry for discovering and executing hierarchical plans by a logical name.
- **`self-correction-protocol-001`**: Defines the automated, closed-loop workflow for protocol self-correction.
- **`non-compliance-protocol-001`**: A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.
- **`pre-commit-protocol-001`**: Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission.
- **`research-protocol-001`**: A protocol for conducting systematic research using the integrated research toolchain.
- **`reset-all-prohibition-001`**: A high-priority protocol that unconditionally forbids the use of the `reset_all` tool.
- **`critic-meta-protocol-001`**: A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.
- **`critic-reset-prohibition-001`**: A specific, high-priority protocol that forbids the Code Review Critic agent from using the 'reset_all' tool.
- **`deep-research-cycle-001`**: A standardized, callable plan for conducting in-depth research on a complex topic.
- **`research-fdc-001`**: Defines the formal Finite Development Cycle (FDC) for conducting deep research.

## Key Components

- **`tooling/__init__.py`**:

  > _No docstring found._

- **`tooling/code_suggester.py`**:

  > Handles the generation and application of autonomous code change suggestions.\n  > \n  > This tool is a key component of the advanced self-correction loop. It is\n  > designed to be invoked by the self-correction orchestrator when a lesson\n  > contains a 'propose-code-change' action.\n  > \n  > For its initial implementation, this tool acts as a structured executor. It\n  > takes a lesson where the 'details' field contains a fully-formed git-style\n  > merge diff and applies it to the target file. It does this by generating a\n  > temporary, single-step plan file and signaling its location for the master\n  > controller to execute.\n  > \n  > This establishes the fundamental workflow for autonomous code modification,\n  > decoupling the suggestion logic from the execution logic. Future iterations\n  > can enhance this tool with more sophisticated code generation capabilities\n  > (e.g., using an LLM to generate the diff from a natural language description)\n  > without altering the core orchestration process.

- **`tooling/context_awareness_scanner.py`**:

  > _No docstring found._

- **`tooling/dependency_graph_generator.py`**:

  > Scans the repository for dependency files and generates a unified dependency graph.\n  > \n  > This script is a crucial component of the agent's environmental awareness,\n  > providing a clear map of the software supply chain. It recursively searches the\n  > entire repository for common dependency management files, specifically:\n  > - `package.json` (for JavaScript/Node.js projects)\n  > - `requirements.txt` (for Python projects)\n  > \n  > It parses these files to identify two key types of relationships:\n  > 1.  **Internal Dependencies:** Links between different projects within this repository.\n  > 2.  **External Dependencies:** Links to third-party libraries and packages.\n  > \n  > The final output is a JSON file, `knowledge_core/dependency_graph.json`, which\n  > represents these relationships as a graph structure with nodes (projects and\n  > dependencies) and edges (the dependency links). This artifact is a primary\n  > input for the agent's orientation and planning phases, allowing it to reason\n  > about the potential impact of its changes.

- **`tooling/doc_generator.py`**:

  > Generates detailed system documentation from Python source files.\n  > \n  > This script scans specified directories for Python files, parses their\n  > Abstract Syntax Trees (ASTs), and extracts documentation for the module,\n  > classes, and functions. The output is a structured Markdown file.\n  > \n  > This is a key component of the project's self-documentation capabilities,\n  > powering the `SYSTEM_DOCUMENTATION.md` artifact in the `knowledge_core`.\n  > \n  > The script is configured via top-level constants:\n  > - `SCAN_DIRECTORIES`: A list of directories to search for .py files.\n  > - `OUTPUT_FILE`: The path where the final Markdown file will be written.\n  > - `DOC_TITLE`: The main title for the generated documentation file.\n  > \n  > It uses Python's `ast` module to reliably parse source files without\n  > importing them, which avoids issues with dependencies or script side-effects.

- **`tooling/environmental_probe.py`**:

  > Performs a series of checks to assess the capabilities of the execution environment.\n  > \n  > This script is a critical diagnostic tool run at the beginning of a task to\n  > ensure the agent understands its operational sandbox. It verifies fundamental\n  > capabilities required for most software development tasks:\n  > \n  > 1.  **Filesystem I/O:** Confirms that the agent can create, write to, read from,\n  >     and delete files. It also provides a basic latency measurement for these\n  >     operations.\n  > 2.  **Network Connectivity:** Checks for external network access by attempting to\n  >     connect to a highly-available public endpoint (google.com). This is crucial\n  >     for tasks requiring `git` operations, package downloads, or API calls.\n  > 3.  **Environment Variables:** Verifies that standard environment variables are\n  >     accessible, which is a prerequisite for many command-line tools.\n  > \n  > The script generates a human-readable report summarizing the results of these\n  > probes, allowing the agent to quickly identify any environmental constraints\n  > that might impact its ability to complete a task.

- **`tooling/fdc_cli.py`**:

  > Provides the command-line interface for the Finite Development Cycle (FDC).\n  > \n  > This script is a core component of the agent's protocol, offering tools to ensure\n  > that all development work is structured, verifiable, and safe. It is used by both\n  > the agent to signal progress and the `master_control.py` orchestrator to\n  > validate the agent's plans before execution.\n  > \n  > The CLI provides several key commands:\n  > - `close`: Logs the formal end of a task, signaling to the orchestrator that\n  >   execution is complete.\n  > - `validate`: Performs a deep validation of a plan file against the FDC's Finite\n  >   State Machine (FSM) definition. It checks for both syntactic correctness (Is\n  >   the sequence of operations valid?) and semantic correctness (Does the plan try\n  >   to use a file before creating it?).\n  > - `analyze`: Reads a plan and provides a high-level analysis of its\n  >   characteristics, such as its computational complexity and whether it is a\n  >   read-only or read-write plan.\n  > - `lint`: A comprehensive "linter" that runs a full suite of checks on a plan\n  >   file, including `validate`, `analyze`, and checks for disallowed recursion.

- **`tooling/hierarchical_compiler.py`**:

  > _No docstring found._

- **`tooling/knowledge_compiler.py`**:

  > Extracts structured lessons from post-mortem reports and compiles them into a\n  > centralized, long-term knowledge base.\n  > \n  > This script is a core component of the agent's self-improvement feedback loop.\n  > After a task is completed, a post-mortem report is generated that includes a\n  > section for "Corrective Actions & Lessons Learned." This script automates the\n  > process of parsing that section to extract key insights.\n  > \n  > It identifies pairs of "Lesson" and "Action" statements and transforms them\n  > into a standardized, machine-readable format. These formatted entries are then\n  > appended to the `knowledge_core/lessons.jsonl` file, which serves as the\n  > agent's persistent memory of what has worked, what has failed, and what can be\n  > improved in future tasks.\n  > \n  > The script is executed via the command line, taking the path to a completed\n  > post-mortem file as its primary argument.

- **`tooling/knowledge_integrator.py`**:

  > Enriches the local knowledge graph with data from external sources like DBPedia.\n  > \n  > This script loads the RDF graph generated from the project's protocols,\n  > identifies key concepts (like tools and rules), queries the DBPedia SPARQL\n  > endpoint to find related information, and merges the external data into a new,\n  > enriched knowledge graph.

- **`tooling/log_failure.py`**:

  > _No docstring found._

- **`tooling/master_control.py`**:

  > The master orchestrator for the agent's lifecycle, governed by a Finite State Machine.\n  > \n  > This script, `master_control.py`, is the heart of the agent's operational loop.\n  > It implements a strict, protocol-driven workflow defined in a JSON file\n  > (typically `tooling/fsm.json`). The `MasterControlGraph` class reads this FSM\n  > definition and steps through the prescribed states, ensuring that the agent\n  > cannot deviate from the established protocol.\n  > \n  > The key responsibilities of this orchestrator include:\n  > - **State Enforcement:** Guiding the agent through the formal states of a task:\n  >   ORIENTING, PLANNING, EXECUTING, FINALIZING, and finally AWAITING_SUBMISSION.\n  > - **Plan Validation:** Before execution, it invokes the `fdc_cli.py` tool to\n  >   formally validate the agent-generated `plan.txt`, preventing the execution of\n  >   invalid or unsafe plans.\n  > - **Hierarchical Execution (CFDC):** It manages the plan execution stack, which\n  >   is the core mechanism of the Context-Free Development Cycle (CFDC). This\n  >   allows plans to call other plans as sub-routines via the `call_plan`\n  >   directive.\n  > - **Recursion Safety:** It enforces a `MAX_RECURSION_DEPTH` on the plan stack to\n  >   guarantee that the execution process is always decidable and will terminate.\n  > - **Lifecycle Management:** It orchestrates the entire lifecycle, from initial\n  >   orientation and environmental probing to the final post-mortem analysis and\n  >   compilation of lessons learned.\n  > \n  > The FSM operates by waiting for specific signals—typically the presence of\n  > files like `plan.txt` or `step_complete.txt`—before transitioning to the next\n  > state. This creates a robust, interactive loop where the orchestrator directs\n  > the high-level state, and the agent is responsible for completing the work\n  > required to advance that state.

- **`tooling/master_control_cli.py`**:

  > The official command-line interface for the agent's master control loop.\n  > \n  > This script provides a clean entry point for initiating a task. It handles\n  > argument parsing, initializes the agent's state, and runs the main FSM-driven\n  > workflow defined in `master_control.py`.

- **`tooling/pages_generator.py`**:

  > Generates a single HTML file for GitHub Pages from the repository's metalanguage.\n  > \n  > This script combines the human-readable `README.md` and the machine-readable\n  > `AGENTS.md` into a single, navigable HTML document. It uses the `markdown`\n  > library to convert the Markdown content to HTML and to automatically generate\n  > a Table of Contents.\n  > \n  > The final output is a semantic HTML5 document, `index.html`, which serves as\n  > the main page for the project's GitHub Pages site.

- **`tooling/plan_manager.py`**:

  > Provides a command-line interface for managing the agent's Plan Registry.\n  > \n  > This script is the administrative tool for the Plan Registry, a key component\n  > of the Context-Free Development Cycle (CFDC) that enables hierarchical and\n  > modular planning. The registry, located at `knowledge_core/plan_registry.json`,\n  > maps human-readable, logical names to the file paths of specific plans. This\n  > decouples the `call_plan` directive from hardcoded file paths, making plans\n  > more reusable and the system more robust.\n  > \n  > This CLI provides three essential functions:\n  > - **register**: Associates a new logical name with a plan file path, adding it\n  >   to the central registry.\n  > - **deregister**: Removes an existing logical name and its associated path from\n  >   the registry.\n  > - **list**: Displays all current name-to-path mappings in the registry.\n  > \n  > By providing a simple, standardized interface for managing this library of\n  > reusable plans, this tool improves the agent's ability to compose complex\n  > workflows from smaller, validated sub-plans.

- **`tooling/plan_parser.py`**:

  > Parses a plan file into a structured list of commands.\n  > \n  > This module provides the `parse_plan` function and the `Command` dataclass,\n  > which are central to the agent's ability to understand and execute plans.\n  > The parser correctly handles multi-line arguments and ignores comments,\n  > allowing for robust and readable plan files.

- **`tooling/protocol_auditor.py`**:

  > Audits the agent's behavior against its governing protocols and generates a report.\n  > \n  > This script performs a comprehensive analysis to ensure the agent's actions,\n  > as recorded in the activity log, align with the defined protocols in AGENTS.md.\n  > It serves as a critical feedback mechanism for maintaining operational integrity.\n  > The final output is a detailed `audit_report.md` file.\n  > \n  > The auditor performs three main checks:\n  > 1.  **`AGENTS.md` Source Check:** Verifies if the `AGENTS.md` build artifact is\n  >     potentially stale by comparing its modification time against the source\n  >     protocol files in the `protocols/` directory.\n  > 2.  **Protocol Completeness:** It cross-references the tools used in the log\n  >     (`logs/activity.log.jsonl`) against the tools defined in `AGENTS.md` to find:\n  >     - Tools used but not associated with any formal protocol.\n  >     - Tools defined in protocols but never used in the log.\n  > 3.  **Tool Centrality:** It conducts a frequency analysis of tool usage to\n  >     identify which tools are most critical to the agent's workflow.\n  > \n  > The script parses all embedded JSON protocol blocks within `AGENTS.md` and reads\n  > from the standard `logs/activity.log.jsonl` log file, providing a reliable and\n  > accurate audit.

- **`tooling/protocol_compiler.py`**:

  > Compiles source protocol files into unified, human-readable and machine-readable artifacts.\n  > \n  > This script is the engine behind the "protocol as code" principle. It discovers,\n  > validates, and assembles protocol definitions from a source directory (e.g., `protocols/`)\n  > into high-level documents like `AGENTS.md`.\n  > \n  > Key Functions:\n  > - **Discovery:** Scans a directory for source files, including `.protocol.json`\n  >   (machine-readable rules) and `.protocol.md` (human-readable context).\n  > - **Validation:** Uses a JSON schema (`protocol.schema.json`) to validate every\n  >   `.protocol.json` file, ensuring all protocol definitions are syntactically\n  >   correct and adhere to the established structure.\n  > - **Compilation:** Combines the human-readable markdown and the machine-readable\n  >   JSON into a single, cohesive Markdown file, embedding the JSON in code blocks.\n  > - **Documentation Injection:** Can inject other generated documents, like the\n  >   `SYSTEM_DOCUMENTATION.md`, into the final output at specified locations.\n  > - **Knowledge Graph Generation:** Optionally, it can process the validated JSON\n  >   protocols and serialize them into an RDF knowledge graph (in Turtle format),\n  >   creating a machine-queryable version of the agent's governing rules.\n  > \n  > This process ensures that `AGENTS.md` and other protocol documents are not edited\n  > manually but are instead generated from a validated, single source of truth,\n  > making the agent's protocols robust, verifiable, and maintainable.

- **`tooling/protocol_updater.py`**:

  > A command-line tool for programmatically updating protocol source files.\n  > \n  > This script provides the mechanism for the agent to perform self-correction\n  > by modifying its own governing protocols based on structured, actionable\n  > lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)\n  > workflow.\n  > \n  > The tool operates on the .protocol.json files located in the `protocols/`\n  > directory, performing targeted updates based on command-line arguments.

- **`tooling/readme_generator.py`**:

  > _No docstring found._

- **`tooling/research.py`**:

  > A unified, constraint-based interface for all research and data-gathering operations.\n  > \n  > This script abstracts the various methods an agent might use to gather information\n  > (reading local files, accessing the web, querying a database) into a single,\n  > standardized function: `execute_research_protocol`. It is a core component of\n  > the Advanced Orientation and Research Protocol (AORP), providing the mechanism\n  > by which the agent fulfills the requirements of each orientation level (L1-L4).\n  > \n  > The function operates on a `constraints` dictionary, which specifies the target,\n  > scope, and other parameters of the research task. This design allows the calling\n  > orchestrator (e.g., `master_control.py`) to request information without needing\n  > to know the underlying implementation details of how that information is fetched.\n  > \n  > This script is designed to be executed by a system that has pre-loaded the\n  > following native tools into the execution environment:\n  > - `read_file(filepath: str) -> str`\n  > - `list_files(path: str = ".") -> list[str]`\n  > - `google_search(query: str) -> str`\n  > - `view_text_website(url: str) -> str`

- **`tooling/research_planner.py`**:

  > Generates a structured, executable plan for conducting deep research tasks.\n  > \n  > This script provides a standardized, FSM-compliant workflow for the agent when\n  > it needs to perform in-depth research on a complex topic. The `plan_deep_research`\n  > function creates a plan file that is not just a template, but a formal,\n  > verifiable artifact that can be executed by the `master_control.py` orchestrator.\n  > \n  > The generated plan adheres to the state transitions defined in `research_fsm.json`,\n  > guiding the agent through the phases of GATHERING, SYNTHESIZING, and REPORTING.

- **`tooling/self_correction_orchestrator.py`**:

  > Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.\n  > \n  > This script is the engine of the automated feedback loop. It reads structured,\n  > actionable lessons from `knowledge_core/lessons.jsonl` and uses the\n  > `protocol_updater.py` tool to apply them to the source protocol files.

- **`tooling/self_improvement_cli.py`**:

  > Analyzes agent activity logs to identify opportunities for self-improvement.\n  > \n  > This script is a command-line tool that serves as a key part of the agent's\n  > meta-cognitive loop. It parses the structured activity log\n  > (`logs/activity.log.jsonl`) to identify patterns that may indicate\n  > inefficiencies or errors in the agent's workflow.\n  > \n  > The primary analysis currently implemented is:\n  > - **Planning Efficiency Analysis:** It scans the logs for tasks that required\n  >   multiple `set_plan` actions. A high number of plan revisions for a single\n  >   task can suggest that the initial planning phase was insufficient, the task\n  >   was poorly understood, or the agent struggled to adapt to unforeseen\n  >   challenges.\n  > \n  > By flagging these tasks, the script provides a starting point for a deeper\n  > post-mortem analysis, helping the agent (or its developers) to understand the\n  > root causes of the planning churn and to develop strategies for more effective\n  > upfront planning in the future.\n  > \n  > The tool is designed to be extensible, with future analyses (such as error\n  > rate tracking or tool usage anti-patterns) to be added as the system evolves.

- **`tooling/standard_agents_compiler.py`**:

  > _No docstring found._

- **`tooling/state.py`**:

  > Defines the core data structures for managing the agent's state.\n  > \n  > This module provides the `AgentState` and `PlanContext` dataclasses, which are\n  > fundamental to the operation of the Context-Free Development Cycle (CFDC). These\n  > structures allow the `master_control.py` orchestrator to maintain a complete,\n  > snapshot-able representation of the agent's progress through a task.\n  > \n  > - `AgentState`: The primary container for all information related to the current\n  >   task, including the plan execution stack, message history, and error states.\n  > - `PlanContext`: A specific structure that holds the state of a single plan\n  >   file, including its content and the current execution step. This is the\n  >   element that gets pushed onto the `plan_stack` in `AgentState`.\n  > \n  > Together, these classes enable the hierarchical, stack-based planning and\n  > execution that is the hallmark of the CFDC.

- **`tooling/symbol_map_generator.py`**:

  > Generates a code symbol map for the repository to aid in contextual understanding.\n  > \n  > This script creates a `symbols.json` file in the `knowledge_core` directory,\n  > which acts as a high-level index of the codebase. This map contains information\n  > about key programming constructs like classes and functions, including their\n  > name, location (file path and line number), and language.\n  > \n  > The script employs a two-tiered approach for symbol generation:\n  > 1.  **Universal Ctags (Preferred):** It first checks for the presence of the\n  >     `ctags` command-line tool. If available, it uses `ctags` to perform a\n  >     comprehensive, multi-language scan of the repository. This is the most\n  >     robust and accurate method.\n  > 2.  **AST Fallback (Python-only):** If `ctags` is not found, the script falls\n  >     back to using Python's built-in Abstract Syntax Tree (`ast`) module. This\n  >     method parses all `.py` files and extracts symbol information for Python\n  >     code. While less comprehensive than `ctags`, it ensures that a baseline\n  >     symbol map is always available.\n  > \n  > The resulting `symbols.json` artifact is a critical input for the agent's\n  > orientation and planning phases, allowing it to quickly locate relevant code\n  > and understand the structure of the repository without having to read every file.