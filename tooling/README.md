# Tooling Documentation

This directory contains the core tooling for the agent's operation. The agent's lifecycle is managed by a Finite State Machine (FSM) defined in `fsm.json` and orchestrated by `master_control.py`.

Below is a description of each tool and its purpose.

---

### Core Components

These are the central scripts that manage the agent's lifecycle.

*   **`master_control_cli.py`**: The command-line entry point for running the agent.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/master_control_cli.py "Your task description here"`
    *   **Arguments**:
        *   `task`: (Required) A string describing the high-level task for the agent.

*   **`agent_shell.py`**: The main application loop that drives the FSM. It initializes the agent state, contains the core "agent logic" (e.g., LLM calls to generate plans), and interacts with the `MasterControlGraph`.
    *   **Type**: Library (invoked by `master_control_cli.py`)

*   **`master_control.py`**: Implements the agent's core Finite State Machine (FSM). It defines the states (`ORIENTING`, `PLANNING`, `EXECUTING`, etc.) and the transitions between them, ensuring the agent follows a strict protocol. It is a library controlled by `agent_shell.py`.
    *   **Type**: Library

### Tooling Scripts

*   **`builder.py`**: A unified build script that reads `build_config.json` to execute various compilation and documentation generation tasks.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/builder.py --target <target_name>`
    *   **Arguments**:
        *   `--target` / `-t`: (Required) The build target to execute. Can be `all` to run all targets.
        *   `--list-targets`: Lists all available build targets.
    *   **Available Targets**: `docs`, `security`, `agents`, `readme`, `audit`.

*   **`code_suggester.py`**: Generates a temporary, single-step plan file to apply a code change using a `git merge` style diff. This is used by the self-correction mechanism.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/code_suggester.py --filepath <path> --diff <diff_content>`
    *   **Arguments**:
        *   `--filepath`: (Required) The path to the file to be modified.
        *   `--diff`: (Required) The git-style merge diff content to apply.

*   **`context_awareness_scanner.py`**: Scans a Python file to determine its contextual awareness within the repository. It identifies defined symbols (functions/classes), imported libraries, and finds where the defined symbols are used in the codebase. It outputs a JSON report.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/context_awareness_scanner.py <file_to_scan.py> --search-path <path>`
    *   **Arguments**:
        *   `filepath`: (Required) The path to the Python file to scan.
        *   `--search-path`: (Optional) The root directory to search for references. Defaults to the current directory.

*   **`dependency_graph_generator.py`**: Scans the entire repository for `package.json` and `requirements.txt` files to build a unified dependency graph. The graph shows relationships between internal projects and external libraries. It saves the output to `knowledge_core/dependency_graph.json`.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/dependency_graph_generator.py`
    *   **Arguments**: None.

*   **`doc_generator.py`**: Generates system documentation by scanning directories for Python files, parsing their docstrings, and creating a structured Markdown file.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/doc_generator.py --source-dir <dir1> --source-dir <dir2> --output-file <path>`
    *   **Arguments**:
        *   `--source-dir`: (Required, repeatable) A directory to scan for `.py` files.
        *   `--output-file`: (Required) The path to the output Markdown file.

*   **`environmental_probe.py`**: A diagnostic script that assesses the capabilities of the execution environment. It checks filesystem I/O, network connectivity, and access to environment variables, then prints a summary report.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/environmental_probe.py`
    *   **Arguments**: None.

*   **`hierarchical_compiler.py`**: A powerful build script that orchestrates the compilation of `AGENTS.md` and `README.md` files across the repository. It operates hierarchically, compiling child modules before parent modules and injecting summaries. It also generates a centralized RDF knowledge graph (`protocols.ttl`) from all `*.protocol.json` files.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/hierarchical_compiler.py`
    *   **Arguments**: None.

*   **`knowledge_compiler.py`**: Extracts structured lessons from post-mortem reports (`.md` files) and compiles them into the `knowledge_core/lessons.jsonl` file. This is a key part of the agent's self-improvement loop.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/knowledge_compiler.py <path_to_postmortem.md>`
    *   **Arguments**:
        *   `postmortem_path`: (Required) Path to the post-mortem markdown file.

*   **`knowledge_integrator.py`**: A library for enriching the project's local knowledge graph with data from external sources like DBPedia. It identifies key concepts in the local graph, queries for them, and merges the results.
    *   **Type**: Library
    *   **Usage**: `run_knowledge_integration(input_graph_path, output_graph_path)`

*   **`log_failure.py`**: A simple script to log a pre-defined catastrophic failure event to the main activity log. This is likely used for testing the logging and monitoring systems.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/log_failure.py`
    *   **Arguments**: None.

*   **`pages_generator.py`**: Combines the root `README.md` and `AGENTS.md` files into a single, styled `index.html` file, suitable for publishing to GitHub Pages.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/pages_generator.py`
    *   **Arguments**: None.

*   **`plan_manager.py`**: A command-line tool for managing the Plan Registry (`knowledge_core/plan_registry.json`), which maps logical names to plan file paths.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/plan_manager.py <command> [args]`
    *   **Commands**:
        *   `list`: Displays all registered plans.
        *   `register <name> <path>`: Registers a new plan.
        *   `deregister <name>`: Removes a plan from the registry.

*   **`plan_parser.py`**: A library for parsing plan files into a structured list of `Command` objects. It correctly handles multi-line arguments and comments.
    *   **Type**: Library
    *   **Usage**: `parse_plan(plan_content)`

*   **`protocol_auditor.py`**: Audits the agent's behavior (from `logs/activity.log.jsonl`) against its defined protocols (in `AGENTS.md` files) and generates a detailed `audit_report.md`.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/protocol_auditor.py`
    *   **Arguments**: None.

*   **`protocol_compiler.py`**: Compiles protocol source files (`.protocol.json`, `.protocol.md`) into a unified `AGENTS.md` file. It validates protocols against a schema and can also generate an RDF knowledge graph.
    *   **Type**: Executable & Library
    *   **Usage**: `python3 tooling/protocol_compiler.py [options]`
    *   **Arguments**:
        *   `--source-dir`: Directory containing protocol source files.
        *   `--output-file`: Path for the output Markdown file.
        *   `--schema-file`: Path to the JSON schema for validation.
        *   `--knowledge-graph-file`: (Optional) Generate a Turtle knowledge graph file.
        *   `--autodoc-file`: Path to a system documentation file to inject.

*   **`protocol_updater.py`**: A command-line tool to programmatically update protocol source files (`.protocol.json`), allowing the agent to perform self-correction.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/protocol_updater.py <command> [options]`
    *   **Commands**:
        *   `add-tool`: Adds a tool to a protocol's `associated_tools` list.
        *   `update-rule`: Updates the description of a specific rule.
    *   **Options**:
        *   `--protocol-id`: (Required) The ID of the protocol to modify.
        *   `--tool-name`: (For `add-tool`) The name of the tool to add.
        *   `--rule-id`: (For `update-rule`) The ID of the rule to update.
        *   `--description`: (For `update-rule`) The new rule description.

*   **`readme_generator.py`**: Generates a human-readable `README.md` for a module by summarizing its `AGENTS.md` file and the docstrings of its key components.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/readme_generator.py --source-file <AGENTS.md> --output-file <README.md>`
    *   **Arguments**:
        *   `--source-file`: (Required) Path to the source `AGENTS.md` file.
        *   `--output-file`: (Required) Path for the output `README.md` file.

*   **`refactor.py`**: A simple refactoring tool that finds a symbol's definition and all its references, then generates a plan file to rename the symbol everywhere it's used.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/refactor.py --filepath <path> --old-name <old> --new-name <new>`
    *   **Arguments**:
        *   `--filepath`: (Required) The path to the file where the symbol is defined.
        *   `--old-name`: (Required) The current name of the symbol.
        *   `--new-name`: (Required) The new name for the symbol.
        *   `--search-path`: (Optional) The root directory to search for references.

*   **`reorientation_manager.py`**: Manages the automated re-orientation process. It compares old and new `AGENTS.md` files to find new concepts, runs temporal orientation (shallow research) on them, and may trigger a deep research cycle for significant changes.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/reorientation_manager.py --old-agents-file <old.md> --new-agents-file <new.md>`
    *   **Arguments**:
        *   `--old-agents-file`: (Required) Path to the `AGENTS.md` file before a build.
        *   `--new-agents-file`: (Required) Path to the `AGENTS.md` file after a build.

*   **`research.py`**: A library providing a unified, constraint-based interface for all research and data-gathering operations (e.g., reading files, searching the web). It is a core component of the agent's orientation protocol.
    *   **Type**: Library
    *   **Usage**: `execute_research_protocol(constraints)`

*   **`research_planner.py`**: A library for generating a structured, FSM-compliant executable plan for deep research tasks.
    *   **Type**: Library
    *   **Usage**: `plan_deep_research(topic)`

*   **`self_correction_orchestrator.py`**: The engine for the self-correction feedback loop. It reads actionable lessons from `knowledge_core/lessons.jsonl` and uses other tools (`protocol_updater.py`, `code_suggester.py`) to apply them, then triggers a rebuild of `AGENTS.md`.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/self_correction_orchestrator.py`
    *   **Arguments**: None.

*   **`self_improvement_cli.py`**: A command-line tool that analyzes agent activity logs (`logs/activity.log.jsonl`) to identify opportunities for self-improvement, such as planning inefficiencies or protocol violations.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/self_improvement_cli.py [--log-file <path>]`
    *   **Arguments**:
        *   `--log-file`: (Optional) Path to the activity log file.

*   **`standard_agents_compiler.py`**: Generates a simplified, standard-compliant `AGENTS.standard.md` file for external tools by parsing key commands (install, test, lint, format) from the project's `Makefile`.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/standard_agents_compiler.py`
    *   **Arguments**: None.

*   **`state.py`**: A library that defines the core data structures (`AgentState`, `PlanContext`) for managing the agent's state throughout its lifecycle. This is fundamental to the FSM's operation.
    *   **Type**: Library
    *   **Usage**: Imported by other tools (`master_control.py`, `agent_shell.py`, etc.).

*   **`symbol_map_generator.py`**: Generates a code symbol map (`knowledge_core/symbols.json`) for the repository. It uses the `ctags` command if available for multi-language support, otherwise falls back to Python's `ast` module for Python-only analysis.
    *   **Type**: Executable
    *   **Usage**: `python3 tooling/symbol_map_generator.py`
    *   **Arguments**: None.

---

### Data and Configuration Files

*   **`fsm.json`**: The primary Finite State Machine (FSM) definition for the main agent lifecycle. It is used by `master_control.py` to orchestrate the agent's flow through states like `ORIENTING`, `PLANNING`, `EXECUTING`, and `FINALIZING`.

*   **`fdc_fsm.json`**: A more granular FSM definition for the Context-Free Development Cycle (CFDC). This likely governs the sub-states within the main `EXECUTING` phase.

*   **`research_fsm.json`**: A specialized FSM definition for the deep research workflow, guiding the agent through `GATHERING`, `SYNTHESIZING`, and `REPORTING` states.

*   **`*.txt` files**: These appear to be older, backup, or alternative versions of the Python scripts. They are not actively used by the current tooling.