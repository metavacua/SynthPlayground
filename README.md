# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key
components defined within this module. It is automatically generated from the
corresponding `AGENTS.md` file and the source code docstrings.

## Core Protocols

This module is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior within this scope. The key protocols are:

- **`agent-bootstrap-001`**: A foundational protocol that dictates the agent's initial actions upon starting any task.
- **`dependency-management-001`**: A protocol for ensuring a reliable execution environment through formal dependency management.
- **`agent-shell-001`**: A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.
- **`toolchain-review-on-schema-change-001`**: A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.
- **`agent-interaction-001`**: A protocol governing the agent's core interaction and planning tools.
- **`plan-registry-audit-001`**: A protocol for using the plan registry auditor tool to ensure the integrity of the plan registry.
- **`refactor-001`**: A protocol for using the refactoring tool.
- **`speculative-execution-001`**: A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods.

## Key Components

- **`tooling/__init__.py`**:

  > _No docstring found._

- **`tooling/agent_shell.py`**:

  > The new, interactive, API-driven entry point for the agent.\n  > \n  > This script replaces the old file-based signaling system with a direct,\n  > programmatic interface to the MasterControlGraph FSM. It is responsible for:\n  > 1.  Initializing the agent's state and a centralized logger.\n  > 2.  Instantiating and running the MasterControlGraph.\n  > 3.  Driving the FSM by calling its methods and passing data and the logger.\n  > 4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans\n  >     and respond to requests for action.

- **`tooling/background_researcher.py`**:

  > This script performs a simulated research task in the background.\n  > It takes a task ID as a command-line argument and writes its findings\n  > to a temporary file that the main agent can poll.

- **`tooling/builder.py`**:

  > _No docstring found._

- **`tooling/code_suggester.py`**:

  > Handles the generation and application of autonomous code change suggestions.\n  > \n  > This tool is a key component of the advanced self-correction loop. It is\n  > designed to be invoked by the self-correction orchestrator when a lesson\n  > contains a 'propose-code-change' action.\n  > \n  > For its initial implementation, this tool acts as a structured executor. It\n  > takes a lesson where the 'details' field contains a fully-formed git-style\n  > merge diff and applies it to the target file. It does this by generating a\n  > temporary, single-step plan file and signaling its location for the master\n  > controller to execute.\n  > \n  > This establishes the fundamental workflow for autonomous code modification,\n  > decoupling the suggestion logic from the execution logic. Future iterations\n  > can enhance this tool with more sophisticated code generation capabilities\n  > (e.g., using an LLM to generate the diff from a natural language description)\n  > without altering the core orchestration process.

- **`tooling/context_awareness_scanner.py`**:

  > _No docstring found._

- **`tooling/dependency_graph_generator.py`**:

  > Scans the repository for dependency files and generates a unified dependency graph.\n  > \n  > This script is a crucial component of the agent's environmental awareness,\n  > providing a clear map of the software supply chain. It recursively searches the\n  > entire repository for common dependency management files, specifically:\n  > - `package.json` (for JavaScript/Node.js projects)\n  > - `requirements.txt` (for Python projects)\n  > \n  > It parses these files to identify two key types of relationships:\n  > 1.  **Internal Dependencies:** Links between different projects within this repository.\n  > 2.  **External Dependencies:** Links to third-party libraries and packages.\n  > \n  > The final output is a JSON file, `knowledge_core/dependency_graph.json`, which\n  > represents these relationships as a graph structure with nodes (projects and\n  > dependencies) and edges (the dependency links). This artifact is a primary\n  > input for the agent's orientation and planning phases, allowing it to reason\n  > about the potential impact of its changes.

- **`tooling/doc_generator.py`**:

  > Generates detailed system documentation from Python source files.\n  > \n  > This script scans specified directories for Python files, parses their\n  > Abstract Syntax Trees (ASTs), and extracts documentation for the module,\n  > classes, and functions. The output is a structured Markdown file.\n  > \n  > This is a key component of the project's self-documentation capabilities,\n  > powering the `SYSTEM_DOCUMENTATION.md` artifact in the `knowledge_core`.\n  > \n  > The script is configured via top-level constants:\n  > - `SCAN_DIRECTORIES`: A list of directories to search for .py files.\n  > - `OUTPUT_FILE`: The path where the final Markdown file will be written.\n  > - `DOC_TITLE`: The main title for the generated documentation file.\n  > \n  > It uses Python's `ast` module to reliably parse source files without\n  > importing them, which avoids issues with dependencies or script side-effects.

- **`tooling/document_scanner.py`**:

  > _No docstring found._

- **`tooling/environmental_probe.py`**:

  > Performs a series of checks to assess the capabilities of the execution environment.\n  > \n  > This script is a critical diagnostic tool run at the beginning of a task to\n  > ensure the agent understands its operational sandbox. It verifies fundamental\n  > capabilities required for most software development tasks:\n  > \n  > 1.  **Filesystem I/O:** Confirms that the agent can create, write to, read from,\n  >     and delete files. It also provides a basic latency measurement for these\n  >     operations.\n  > 2.  **Network Connectivity:** Checks for external network access by attempting to\n  >     connect to a highly-available public endpoint (google.com). This is crucial\n  >     for tasks requiring `git` operations, package downloads, or API calls.\n  > 3.  **Environment Variables:** Verifies that standard environment variables are\n  >     accessible, which is a prerequisite for many command-line tools.\n  > \n  > The script generates a human-readable report summarizing the results of these\n  > probes, allowing the agent to quickly identify any environmental constraints\n  > that might impact its ability to complete a task.

- **`tooling/fdc_cli.py`**:

  > _Error parsing file: invalid syntax. Perhaps you forgot a comma? (fdc_cli.py, line 178)_

- **`tooling/generate_docs.py`**:

  > This script generates comprehensive Markdown documentation for the agent's\n  > architecture, including the FSM, the agent shell, and the master control script.

- **`tooling/hierarchical_compiler.py`**:

  > _No docstring found._

- **`tooling/knowledge_compiler.py`**:

  > Extracts structured lessons from post-mortem reports and compiles them into a\n  > centralized, long-term knowledge base.\n  > \n  > This script is a core component of the agent's self-improvement feedback loop.\n  > After a task is completed, a post-mortem report is generated that includes a\n  > section for "Corrective Actions & Lessons Learned." This script automates the\n  > process of parsing that section to extract key insights.\n  > \n  > It identifies pairs of "Lesson" and "Action" statements and transforms them\n  > into a standardized, machine-readable format. These formatted entries are then\n  > appended to the `knowledge_core/lessons.jsonl` file, which serves as the\n  > agent's persistent memory of what has worked, what has failed, and what can be\n  > improved in future tasks.\n  > \n  > The script is executed via the command line, taking the path to a completed\n  > post-mortem file as its primary argument.

- **`tooling/knowledge_integrator.py`**:

  > Enriches the local knowledge graph with data from external sources like DBPedia.\n  > \n  > This script loads the RDF graph generated from the project's protocols,\n  > identifies key concepts (like tools and rules), queries the DBPedia SPARQL\n  > endpoint to find related information, and merges the external data into a new,\n  > enriched knowledge graph.

- **`tooling/log_failure.py`**:

  > _No docstring found._

- **`tooling/master_control.py`**:

  > The master orchestrator for the agent's lifecycle, implementing the Context-Free Development Cycle (CFDC).\n  > \n  > This script, master_control.py, is the heart of the agent's operational loop.\n  > It implements the CFDC, a hierarchical planning and execution model based on a\n  > Pushdown Automaton. This allows the agent to execute complex tasks by calling\n  > plans as sub-routines.\n  > \n  > Core Responsibilities:\n  > - **Hierarchical Plan Execution:** Manages a plan execution stack to enable\n  >   plans to call other plans via the `call_plan` directive. This allows for\n  >   modular, reusable, and complex task decomposition. A maximum recursion depth\n  >   is enforced to guarantee decidability.\n  > - **Plan Validation:** Contains the in-memory plan validator. Before execution,\n  >   it parses a plan and simulates its execution against a Finite State Machine\n  >   (FSM) to ensure it complies with the agent's operational protocols.\n  > - **"Registry-First" Plan Resolution:** When resolving a `call_plan` directive,\n  >   it first attempts to look up the plan by its logical name in the\n  >   `knowledge_core/plan_registry.json`. If not found, it falls back to treating\n  >   the argument as a direct file path.\n  > - **FSM-Governed Lifecycle:** The entire workflow, from orientation to\n  >   finalization, is governed by a strict FSM definition (e.g., `tooling/fsm.json`)\n  >   to ensure predictable and auditable behavior.\n  > \n  > This module is designed as a library to be controlled by an external shell\n  > (e.g., `agent_shell.py`), making its interaction purely programmatic.

- **`tooling/master_control_cli.py`**:

  > The official command-line interface for the agent's master control loop.\n  > \n  > This script is now a lightweight wrapper that passes control to the new,\n  > API-driven `agent_shell.py`. It preserves the command-line interface while\n  > decoupling the entry point from the FSM implementation.

- **`tooling/pages_generator.py`**:

  > Generates a single HTML file for GitHub Pages from the repository's metalanguage.\n  > \n  > This script combines the human-readable `README.md` and the machine-readable\n  > `AGENTS.md` into a single, navigable HTML document. It uses the `markdown`\n  > library to convert the Markdown content to HTML and to automatically generate\n  > a Table of Contents.\n  > \n  > The final output is a semantic HTML5 document, `index.html`, which serves as\n  > the main page for the project's GitHub Pages site.

- **`tooling/plan_manager.py`**:

  > Provides a command-line interface for managing the agent's Plan Registry.\n  > \n  > This script is the administrative tool for the Plan Registry, a key component\n  > of the Context-Free Development Cycle (CFDC) that enables hierarchical and\n  > modular planning. The registry, located at `knowledge_core/plan_registry.json`,\n  > maps human-readable, logical names to the file paths of specific plans. This\n  > decouples the `call_plan` directive from hardcoded file paths, making plans\n  > more reusable and the system more robust.\n  > \n  > This CLI provides three essential functions:\n  > - **register**: Associates a new logical name with a plan file path, adding it\n  >   to the central registry.\n  > - **deregister**: Removes an existing logical name and its associated path from\n  >   the registry.\n  > - **list**: Displays all current name-to-path mappings in the registry.\n  > \n  > By providing a simple, standardized interface for managing this library of\n  > reusable plans, this tool improves the agent's ability to compose complex\n  > workflows from smaller, validated sub-plans.

- **`tooling/plan_parser.py`**:

  > Parses a plan file into a structured list of commands.\n  > \n  > This module provides the `parse_plan` function and the `Command` dataclass,\n  > which are central to the agent's ability to understand and execute plans.\n  > The parser correctly handles multi-line arguments and ignores comments,\n  > allowing for robust and readable plan files.

- **`tooling/plan_registry_auditor.py`**:

  > _No docstring found._

- **`tooling/protocol_auditor.py`**:

  > Audits the agent's behavior against its governing protocols and generates a report.\n  > \n  > This script performs a comprehensive analysis to ensure the agent's actions,\n  > as recorded in the activity log, align with the defined protocols in AGENTS.md.\n  > It serves as a critical feedback mechanism for maintaining operational integrity.\n  > The final output is a detailed `audit_report.md` file.\n  > \n  > The auditor performs three main checks:\n  > 1.  **`AGENTS.md` Source Check:** Verifies if the `AGENTS.md` build artifact is\n  >     potentially stale by comparing its modification time against the source\n  >     protocol files in the `protocols/` directory.\n  > 2.  **Protocol Completeness:** It cross-references the tools used in the log\n  >     (`logs/activity.log.jsonl`) against the tools defined in `AGENTS.md` to find:\n  >     - Tools used but not associated with any formal protocol.\n  >     - Tools defined in protocols but never used in the log.\n  > 3.  **Tool Centrality:** It conducts a frequency analysis of tool usage to\n  >     identify which tools are most critical to the agent's workflow.\n  > \n  > The script parses all embedded JSON protocol blocks within `AGENTS.md` and reads\n  > from the standard `logs/activity.log.jsonl` log file, providing a reliable and\n  > accurate audit.

- **`tooling/protocol_compiler.py`**:

  > Compiles source protocol files into unified, human-readable and machine-readable artifacts.\n  > \n  > This script is the engine behind the "protocol as code" principle. It discovers,\n  > validates, and assembles protocol definitions from a source directory (e.g., `protocols/`)\n  > into high-level documents like `AGENTS.md`.\n  > \n  > Key Functions:\n  > - **Discovery:** Scans a directory for source files, including `.protocol.json`\n  >   (machine-readable rules) and `.protocol.md` (human-readable context).\n  > - **Validation:** Uses a JSON schema (`protocol.schema.json`) to validate every\n  >   `.protocol.json` file, ensuring all protocol definitions are syntactically\n  >   correct and adhere to the established structure.\n  > - **Compilation:** Combines the human-readable markdown and the machine-readable\n  >   JSON into a single, cohesive Markdown file, embedding the JSON in code blocks.\n  > - **Documentation Injection:** Can inject other generated documents, like the\n  >   `SYSTEM_DOCUMENTATION.md`, into the final output at specified locations.\n  > - **Knowledge Graph Generation:** Optionally, it can process the validated JSON\n  >   protocols and serialize them into an RDF knowledge graph (in Turtle format),\n  >   creating a machine-queryable version of the agent's governing rules.\n  > \n  > This process ensures that `AGENTS.md` and other protocol documents are not edited\n  > manually but are instead generated from a validated, single source of truth,\n  > making the agent's protocols robust, verifiable, and maintainable.

- **`tooling/protocol_updater.py`**:

  > A command-line tool for programmatically updating protocol source files.\n  > \n  > This script provides the mechanism for the agent to perform self-correction\n  > by modifying its own governing protocols based on structured, actionable\n  > lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)\n  > workflow.\n  > \n  > The tool operates on the .protocol.json files located in the `protocols/`\n  > directory, performing targeted updates based on command-line arguments.

- **`tooling/readme_generator.py`**:

  > _No docstring found._

- **`tooling/refactor.py`**:

  > _No docstring found._

- **`tooling/reorientation_manager.py`**:

  > Re-orientation Manager\n  > \n  > This script is the core of the automated re-orientation process. It is\n  > designed to be triggered by the build system whenever the agent's core\n  > protocols (`AGENTS.md`) are re-compiled.\n  > \n  > The manager performs the following key functions:\n  > 1.  **Diff Analysis:** It compares the old version of AGENTS.md with the new\n  >     version to identify new protocols, tools, or other key concepts that have\n  >     been introduced.\n  > 2.  **Temporal Orientation (Shallow Research):** For each new concept, it\n  >     invokes the `temporal_orienter.py` tool to fetch a high-level summary from\n  >     an external knowledge base like DBpedia. This ensures the agent has a\n  >     baseline understanding of new terms.\n  > 3.  **Knowledge Storage:** The summaries from the temporal orientation are\n  >     stored in a structured JSON file (`knowledge_core/temporal_orientations.json`),\n  >     creating a persistent, queryable knowledge artifact.\n  > 4.  **Deep Research Trigger:** It analyzes the nature of the changes. If a\n  >     change is deemed significant (e.g., the addition of a new core\n  >     architectural protocol), it programmatically triggers a formal L4 Deep\n  >     Research Cycle by creating a `deep_research_required.json` file.\n  > \n  > This automated workflow ensures that the agent never operates with an outdated\n  > understanding of its own protocols. It closes the loop between protocol\n  > modification and the agent's self-awareness, making the system more robust,\n  > adaptive, and reliable.

- **`tooling/research.py`**:

  > This module contains the logic for executing research tasks based on a set of\n  > constraints. It acts as a dispatcher, calling the appropriate tool (e.g.,\n  > read_file, google_search) based on the specified target and scope.

- **`tooling/research_planner.py`**:

  > This module is responsible for generating a formal, FSM-compliant research plan\n  > for a given topic. The output is a string that can be executed by the agent's\n  > master controller.

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