# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key components defined within this module. It is automatically generated.

## Core Protocols

- **`dependency-management-001`**: A protocol for ensuring a reliable execution environment through formal dependency management.
- **`agent-shell-001`**: A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.
- **`toolchain-review-on-schema-change-001`**: A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.
- **`unified-auditor-001`**: A protocol for the unified repository auditing tool, which combines multiple health and compliance checks into a single interface.
- **`aura-execution-001`**: A protocol for executing Aura scripts, enabling a more expressive and powerful planning and automation language for the agent.
- **`capability-verification-001`**: A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.
- **`csdc-001`**: A protocol for the Context-Sensitive Development Cycle (CSDC), which introduces development models based on logical constraints.
- **`unified-doc-builder-001`**: A protocol for the unified documentation builder, which generates various documentation artifacts from the repository's sources of truth.
- **`hdl-proving-001`**: A protocol for interacting with the Hypersequent-calculus-based logic engine, allowing the agent to perform formal logical proofs.
- **`agent-interaction-001`**: A protocol governing the agent's core interaction and planning tools.
- **`security-header`**: Defines the identity and purpose of the Security Protocol document.
- **`security-vuln-reporting-001`**: Defines the official policy and procedure for reporting security vulnerabilities.
- **`speculative-execution-001`**: A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods.

## Key Components

- **`tooling/__init__.py`**:

  > This module contains the various tools and utilities that support the agent's
  > development, testing, and operational workflows.
  >
  > The tools in this package are the building blocks of the agent's capabilities,
  > ranging from code analysis and refactoring to protocol compilation and
  > self-correction. Each script is designed to be a self-contained unit of
  > functionality that can be invoked either from the command line or programmatically
  > by the agent's master control system.
  >
  > This __init__.py file marks the 'tooling' directory as a Python package,
  > allowing for the organized import of its various modules.

- **`tooling/agent_shell.py`**:

  > The new, interactive, API-driven entry point for the agent.
  >
  > This script replaces the old file-based signaling system with a direct,
  > programmatic interface to the MasterControlGraph FSM. It is responsible for:
  > 1.  Initializing the agent's state and a centralized logger.
  > 2.  Instantiating and running the MasterControlGraph.
  > 3.  Driving the FSM by calling its methods and passing data and the logger.
  > 4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans
  >     and respond to requests for action.

- **`tooling/auditor.py`**:

  > A unified auditing tool for maintaining repository health and compliance.
  >
  > This script combines the functionality of several disparate auditing tools into a
  > single, comprehensive command-line interface. It serves as the central tool for
  > validating the key components of the agent's architecture, including protocols,
  > plans, and documentation.
  >
  > The auditor can perform the following checks:
  > 1.  **Protocol Audit (`protocol`):**
  >     - Checks if `AGENTS.md` artifacts are stale compared to their source files.
  >     - Verifies protocol completeness by comparing tools used in logs against
  >       tools defined in protocols.
  >     - Analyzes tool usage frequency (centrality).
  > 2.  **Plan Registry Audit (`plans`):**
  >     - Scans `knowledge_core/plan_registry.json` for "dead links" where the
  >       target plan file does not exist.
  > 3.  **Documentation Audit (`docs`):**
  >     - Scans the generated `SYSTEM_DOCUMENTATION.md` to find Python modules
  >       that are missing module-level docstrings.
  >
  > The tool is designed to be run from the command line and can execute specific
  > audits or all of them, generating a consolidated `audit_report.md` file.

- **`tooling/aura_executor.py`**:

  > This script serves as the command-line executor for `.aura` files.
  >
  > It bridges the gap between the high-level Aura scripting language and the
  > agent's underlying Python-based toolset. The executor is responsible for:
  > 1.  Parsing the `.aura` source code using the lexer and parser from the
  >     `aura_lang` package.
  > 2.  Setting up an execution environment for the interpreter.
  > 3.  Injecting a "tool-calling" capability into the Aura environment, which
  >     allows Aura scripts to dynamically invoke registered Python tools
  >     (e.g., `hdl_prover`, `environmental_probe`).
  > 4.  Executing the parsed program and printing the final result.
  >
  > This makes it a key component for enabling more expressive and complex
  > automation scripts for the agent.

- **`tooling/builder.py`**:

  > A unified, configuration-driven build script for the project.
  >
  > This script serves as the central entry point for all build-related tasks, such
  > as generating documentation, compiling protocols, and running code quality checks.
  > It replaces a traditional Makefile's direct command execution with a more
  > structured, maintainable, and introspectable approach.
  >
  > The core logic is driven by a `build_config.json` file, which defines a series
  > of "targets." Each target specifies:
  > - The `type` of target: "compiler" or "command".
  > - For "compiler" types: `compiler` script, `output`, `sources`, and `options`.
  > - For "command" types: the `command` to execute.
  >
  > The configuration also defines "build_groups", which are ordered collections of
  > targets (e.g., "all", "quality").
  >
  > This centralized builder provides several advantages:
  > - **Single Source of Truth:** The `build_config.json` file is the definitive
  >   source for all build logic.
  > - **Consistency:** Ensures all build tasks are executed in a uniform way.
  > - **Extensibility:** New build targets can be added by simply updating the
  >   configuration file.
  > - **Discoverability:** The script can list all available targets and groups.

- **`tooling/capability_verifier.py`**:

  > A tool to verify that the agent can monotonically improve its capabilities.
  >
  > This script is designed to provide a formal, automated test for the agent's
  > self-correction and learning mechanisms. It ensures that when the agent learns
  > a new capability, it does so without losing (regressing) any of its existing
  > capabilities. This is a critical safeguard for ensuring robust and reliable
  > agent evolution.
  >
  > The tool works by orchestrating a four-step process:
  > 1.  **Confirm Initial Failure:** It runs a specific test file that is known to
  >     fail, verifying that the agent currently lacks the target capability.
  > 2.  **Invoke Self-Correction:** It simulates the discovery of a new "lesson" and
  >     triggers the `self_correction_orchestrator.py` script, which is responsible
  >     for integrating new knowledge and skills.
  > 3.  **Confirm Final Success:** It runs the same test file again, confirming that
  >     the agent has successfully learned the new capability and the test now passes.
  > 4.  **Check for Regressions:** It runs the full, existing test suite to ensure
  >     that the process of learning the new skill has not inadvertently broken any
  >     previously functional capabilities.
  >
  > This provides a closed-loop verification of monotonic improvement, which is a
  > cornerstone of the agent's design philosophy.

- **`tooling/code_suggester.py`**:

  > Handles the generation and application of autonomous code change suggestions.
  >
  > This tool is a key component of the advanced self-correction loop. It is
  > designed to be invoked by the self-correction orchestrator when a lesson
  > contains a 'propose-code-change' action.
  >
  > For its initial implementation, this tool acts as a structured executor. It
  > takes a lesson where the 'details' field contains a fully-formed git-style
  > merge diff and applies it to the target file. It does this by generating a
  > temporary, single-step plan file and signaling its location for the master
  > controller to execute.
  >
  > This establishes the fundamental workflow for autonomous code modification,
  > decoupling the suggestion logic from the execution logic. Future iterations
  > can enhance this tool with more sophisticated code generation capabilities
  > (e.g., using an LLM to generate the diff from a natural language description)
  > without altering the core orchestration process.

- **`tooling/context_awareness_scanner.py`**:

  > A tool for performing static analysis on a Python file to understand its context.
  >
  > This script provides a "contextual awareness" scan of a specified Python file
  > to help an agent (or a human) understand its role, dependencies, and connections
  > within a larger codebase. This is crucial for planning complex changes or
  > refactoring efforts, as it provides a snapshot of the potential impact of
  > modifying a file.
  >
  > The scanner performs three main functions:
  > 1.  **Symbol Definition Analysis:** It uses Python's Abstract Syntax Tree (AST)
  >     module to parse the target file and identify all the functions and classes
  >     that are defined within it.
  > 2.  **Import Analysis:** It also uses the AST to find all modules and symbols
  >     that the target file imports, revealing its dependencies on other parts of
  >     the codebase or external libraries.
  > 3.  **Reference Finding:** It performs a repository-wide search to find all other
  >     files that reference the symbols defined in the target file. This helps to
  >     understand how the file is used by the rest of the system.
  >
  > The final output is a detailed JSON report containing all of this information,
  > which can be used as a foundational artifact for automated planning or human review.

- **`tooling/dependency_graph_generator.py`**:

  > Scans the repository for dependency files and generates a unified dependency graph.
  >
  > This script is a crucial component of the agent's environmental awareness,
  > providing a clear map of the software supply chain. It recursively searches the
  > entire repository for common dependency management files, specifically:
  > - `package.json` (for JavaScript/Node.js projects)
  > - `requirements.txt` (for Python projects)
  >
  > It parses these files to identify two key types of relationships:
  > 1.  **Internal Dependencies:** Links between different projects within this repository.
  > 2.  **External Dependencies:** Links to third-party libraries and packages.
  >
  > The final output is a JSON file, `knowledge_core/dependency_graph.json`, which
  > represents these relationships as a graph structure with nodes (projects and
  > dependencies) and edges (the dependency links). This artifact is a primary
  > input for the agent's orientation and planning phases, allowing it to reason
  > about the potential impact of its changes.

- **`tooling/doc_builder.py`**:

  > A unified documentation builder for the project.
  > ...

- **`tooling/document_scanner.py`**:

  > A tool for scanning the repository for human-readable documents and extracting their text content.
  >
  > This script is a crucial component of the agent's initial information-gathering
  > and orientation phase. It allows the agent to ingest knowledge from unstructured
  > or semi-structured documents that are not part of the formal codebase, but which
  > may contain critical context, requirements, or specifications.
  >
  > The scanner searches a given directory for files with common document extensions:
  > - `.pdf`: Uses the `pypdf` library to extract text from PDF files.
  > - `.md`: Reads Markdown files.
  > - `.txt`: Reads plain text files.
  >
  > The output is a dictionary where the keys are the file paths of the discovered
  > documents and the values are their extracted text content. This data can then
  > be used by the agent to inform its planning and execution process. This tool
  > is essential for bridging the gap between human-written documentation and the
  > agent's operational awareness.

- **`tooling/environmental_probe.py`**:

  > Performs a series of checks to assess the capabilities of the execution environment.
  >
  > This script is a critical diagnostic tool run at the beginning of a task to
  > ensure the agent understands its operational sandbox. It verifies fundamental
  > capabilities required for most software development tasks:
  >
  > 1.  **Filesystem I/O:** Confirms that the agent can create, write to, read from,
  >     and delete files. It also provides a basic latency measurement for these
  >     operations.
  > 2.  **Network Connectivity:** Checks for external network access by attempting to
  >     connect to a highly-available public endpoint (google.com). This is crucial
  >     for tasks requiring `git` operations, package downloads, or API calls.
  > 3.  **Environment Variables:** Verifies that standard environment variables are
  >     accessible, which is a prerequisite for many command-line tools.
  >
  > The script generates a human-readable report summarizing the results of these
  > probes, allowing the agent to quickly identify any environmental constraints
  > that might impact its ability to complete a task.

- **`tooling/filesystem_lister.py`**:

  > _No module-level docstring found._

- **`tooling/hdl_prover.py`**:

  > A command-line tool for proving sequents in Intuitionistic Linear Logic.
  >
  > This script provides a basic interface to a simple logic prover. It takes a
  > sequent as a command-line argument, parses it into a logical structure, and
  > then attempts to prove it using a rudimentary proof search algorithm.
  >
  > The primary purpose of this tool is to allow the agent to perform formal
  > reasoning and verification tasks by checking the validity of logical entailments.
  > For example, it can be used to verify that a certain conclusion follows from a
  > set of premises according to the rules of linear logic.
  >
  > The current implementation uses a very basic parser and proof algorithm,
  > serving as a placeholder and demonstration for a more sophisticated, underlying
  > logic engine.

- **`tooling/hierarchical_compiler.py`**:

  > A hierarchical build system for compiling nested protocol modules.
  >
  > This script orchestrates the compilation of `AGENTS.md` and `README.md` files
  > across a repository with a nested or hierarchical module structure. It is a key
  > component of the system's ability to manage complexity by allowing protocols to
  > be defined in a modular, distributed way while still being presented as a unified,
  > coherent whole at each level of the hierarchy.
  >
  > The compiler operates in two main passes:
  >
  > **Pass 1: Documentation Compilation (Bottom-Up)**
  > 1.  **Discovery:** It finds all `protocols` directories in the repository, which
  >     signify the root of a documentation module.
  > 2.  **Bottom-Up Traversal:** It processes these directories from the most deeply
  >     nested ones upwards. This ensures that child modules are always built before
  >     their parents.
  > 3.  **Child Summary Injection:** For each compiled child module, it generates a
  >     summary of its protocols and injects this summary into the parent's
  >     `protocols` directory as a temporary file.
  > 4.  **Parent Compilation:** When the parent module is compiled, the standard
  >     `protocol_compiler.py` automatically includes the injected child summaries,
  >     creating a single `AGENTS.md` file that contains both the parent's native
  >     protocols and the full protocols of all its direct children.
  > 5.  **README Generation:** After each `AGENTS.md` is compiled, the corresponding
  >     `README.md` is generated.
  >
  > **Pass 2: Centralized Knowledge Graph Compilation**
  > 1.  After all documentation is built, it performs a full repository scan to find
  >     every `*.protocol.json` file.
  > 2.  It parses all of these files and compiles them into a single, centralized
  >     RDF knowledge graph (`protocols.ttl`). This provides a unified,
  >     machine-readable view of every protocol defined anywhere in the system.
  >
  > This hierarchical approach allows for both localized, context-specific protocol
  > definitions and a holistic, system-wide understanding of the agent's governing rules.

- **`tooling/knowledge_compiler.py`**:

  > Extracts structured lessons from post-mortem reports and compiles them into a
  > centralized, long-term knowledge base.
  >
  > This script is a core component of the agent's self-improvement feedback loop.
  > After a task is completed, a post-mortem report is generated that includes a
  > section for "Corrective Actions & Lessons Learned." This script automates the
  > process of parsing that section to extract key insights.
  >
  > It identifies pairs of "Lesson" and "Action" statements and transforms them
  > into a standardized, machine-readable format. These formatted entries are then
  > appended to the `knowledge_core/lessons.jsonl` file, which serves as the
  > agent's persistent memory of what has worked, what has failed, and what can be
  > improved in future tasks.
  >
  > The script is executed via the command line, taking the path to a completed
  > post-mortem file as its primary argument.

- **`tooling/knowledge_integrator.py`**:

  > Enriches the local knowledge graph with data from external sources like DBPedia.
  >
  > This script loads the RDF graph generated from the project's protocols,
  > identifies key concepts (like tools and rules), queries the DBPedia SPARQL
  > endpoint to find related information, and merges the external data into a new,
  > enriched knowledge graph.

- **`tooling/log_failure.py`**:

  > A dedicated script to log a catastrophic failure event to the main activity log.
  >
  > This tool is designed to be invoked in the rare case of a severe, unrecoverable
  > error that violates a core protocol. Its primary purpose is to ensure that such
  > a critical event is formally and structurally documented in the standard agent
  > activity log (`logs/activity.log.jsonl`), even if the main agent loop has
  > crashed or been terminated.
  >
  > The script is pre-configured to log a `SYSTEM_FAILURE` event, specifically
  > attributing it to the "Unauthorized use of the `reset_all` tool." This creates a
  > permanent, machine-readable record of the failure, which is essential for
  > post-mortem analysis, debugging, and the development of future safeguards.
  >
  > By using the standard `Logger` class, it ensures that the failure log entry
  > conforms to the established `LOGGING_SCHEMA.md`, making it processable by
  > auditing and analysis tools.

- **`tooling/master_control.py`**:

  > The master orchestrator for the agent's lifecycle, implementing the Context-Free Development Cycle (CFDC).
  >
  > This script, master_control.py, is the heart of the agent's operational loop.
  > It implements the CFDC, a hierarchical planning and execution model based on a
  > Pushdown Automaton. This allows the agent to execute complex tasks by calling
  > plans as sub-routines.
  >
  > Core Responsibilities:
  > - **Hierarchical Plan Execution:** Manages a plan execution stack to enable
  >   plans to call other plans via the `call_plan` directive. This allows for
  >   modular, reusable, and complex task decomposition. A maximum recursion depth
  >   is enforced to guarantee decidability.
  > - **Plan Validation:** Contains the in-memory plan validator. Before execution,
  >   it parses a plan and simulates its execution against a Finite State Machine
  >   (FSM) to ensure it complies with the agent's operational protocols.
  > - **"Registry-First" Plan Resolution:** When resolving a `call_plan` directive,
  >   it first attempts to look up the plan by its logical name in the
  >   `knowledge_core/plan_registry.json`. If not found, it falls back to treating
  >   the argument as a direct file path.
  > - **FSM-Governed Lifecycle:** The entire workflow, from orientation to
  >   finalization, is governed by a strict FSM definition (e.g., `tooling/fsm.json`)
  >   to ensure predictable and auditable behavior.
  >
  > This module is designed as a library to be controlled by an external shell
  > (e.g., `agent_shell.py`), making its interaction purely programmatic.

- **`tooling/plan_manager.py`**:

  > Provides a command-line interface for managing the agent's Plan Registry.
  >
  > This script is the administrative tool for the Plan Registry, a key component
  > of the Context-Free Development Cycle (CFDC) that enables hierarchical and
  > modular planning. The registry, located at `knowledge_core/plan_registry.json`,
  > maps human-readable, logical names to the file paths of specific plans. This
  > decouples the `call_plan` directive from hardcoded file paths, making plans
  > more reusable and the system more robust.
  >
  > This CLI provides three essential functions:
  > - **register**: Associates a new logical name with a plan file path, adding it
  >   to the central registry.
  > - **deregister**: Removes an existing logical name and its associated path from
  >   the registry.
  > - **list**: Displays all current name-to-path mappings in the registry.
  >
  > By providing a simple, standardized interface for managing this library of
  > reusable plans, this tool improves the agent's ability to compose complex
  > workflows from smaller, validated sub-plans.

- **`tooling/plan_parser.py`**:

  > Parses a plan file into a structured list of commands.
  >
  > This module provides the `parse_plan` function and the `Command` dataclass,
  > which are central to the agent's ability to understand and execute plans.
  > The parser correctly handles multi-line arguments and ignores comments,
  > allowing for robust and readable plan files.

- **`tooling/protocol_compiler.py`**:

  > Compiles source protocol files into unified, human-readable and machine-readable artifacts.
  >
  > This script is the engine behind the "protocol as code" principle. It discovers,
  > validates, and assembles protocol definitions from a source directory (e.g., `protocols/`)
  > into high-level documents like `AGENTS.md`.
  >
  > Key Functions:
  > - **Discovery:** Scans a directory for source files, including `.protocol.json`
  >   (machine-readable rules) and `.protocol.md` (human-readable context).
  > - **Validation:** Uses a JSON schema (`protocol.schema.json`) to validate every
  >   `.protocol.json` file, ensuring all protocol definitions are syntactically
  >   correct and adhere to the established structure.
  > - **Compilation:** Combines the human-readable markdown and the machine-readable
  >   JSON into a single, cohesive Markdown file, embedding the JSON in code blocks.
  > - **Documentation Injection:** Can inject other generated documents, like the
  >   `SYSTEM_DOCUMENTATION.md`, into the final output at specified locations.
  > - **Knowledge Graph Generation:** Optionally, it can process the validated JSON
  >   protocols and serialize them into an RDF knowledge graph (in Turtle format),
  >   creating a machine-queryable version of the agent's governing rules.
  >
  > This process ensures that `AGENTS.md` and other protocol documents are not edited
  > manually but are instead generated from a validated, single source of truth,
  > making the agent's protocols robust, verifiable, and maintainable.

- **`tooling/protocol_updater.py`**:

  > A command-line tool for programmatically updating protocol source files.
  >
  > This script provides the mechanism for the agent to perform self-correction
  > by modifying its own governing protocols based on structured, actionable
  > lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)
  > workflow.
  >
  > The tool operates on the .protocol.json files located in the `protocols/`
  > directory, performing targeted updates based on command-line arguments.

- **`tooling/refactor.py`**:

  > A tool for performing automated symbol renaming in Python code.
  >
  > This script provides a command-line interface to find a specific symbol
  > (a function or a class) in a given Python file and rename it, along with all of
  > its textual references throughout the entire repository. This provides a safe
  > and automated way to perform a common refactoring task, reducing the risk of
  > manual errors.
  >
  > The tool operates in three main stages:
  > 1.  **Definition Finding:** It uses Python's Abstract Syntax Tree (AST) module
  >     to parse the source file and precisely locate the definition of the target
  >     symbol. This ensures that the tool is targeting the correct code construct.
  > 2.  **Reference Finding:** It performs a text-based search across the specified
  >     search path (defaulting to the entire repository) to find all files that
  >     mention the symbol's old name.
  > 3.  **Plan Generation:** Instead of modifying files directly, it generates a
  >     refactoring "plan." This plan is a sequence of `replace_with_git_merge_diff`
  >     commands, one for each file that needs to be changed. The path to this
  >     generated plan file is printed to standard output.
  >
  > This plan-based approach allows the agent's master controller to execute the
  > refactoring in a controlled, verifiable, and atomic way, consistent with its
  > standard operational procedures.

- **`tooling/reorientation_manager.py`**:

  > Re-orientation Manager
  >
  > This script is the core of the automated re-orientation process. It is
  > designed to be triggered by the build system whenever the agent's core
  > protocols (`AGENTS.md`) are re-compiled.
  >
  > The manager performs the following key functions:
  > 1.  **Diff Analysis:** It compares the old version of AGENTS.md with the new
  >     version to identify new protocols, tools, or other key concepts that have
  >     been introduced.
  > 2.  **Temporal Orientation (Shallow Research):** For each new concept, it
  >     invokes the `temporal_orienter.py` tool to fetch a high-level summary from
  >     an external knowledge base like DBpedia. This ensures the agent has a
  >     baseline understanding of new terms.
  > 3.  **Knowledge Storage:** The summaries from the temporal orientation are
  >     stored in a structured JSON file (`knowledge_core/temporal_orientations.json`),
  >     creating a persistent, queryable knowledge artifact.
  > 4.  **Deep Research Trigger:** It analyzes the nature of the changes. If a
  >     change is deemed significant (e.g., the addition of a new core
  >     architectural protocol), it programmatically triggers a formal L4 Deep
  >     Research Cycle by creating a `deep_research_required.json` file.
  >
  > This automated workflow ensures that the agent never operates with an outdated
  > understanding of its own protocols. It closes the loop between protocol
  > modification and the agent's self-awareness, making the system more robust,
  > adaptive, and reliable.

- **`tooling/research.py`**:

  > This module contains the logic for executing research tasks based on a set of
  > constraints. It acts as a dispatcher, calling the appropriate tool (e.g.,
  > read_file, google_search) based on the specified target and scope.

- **`tooling/research_planner.py`**:

  > This module is responsible for generating a formal, FSM-compliant research plan
  > for a given topic. The output is a string that can be executed by the agent's
  > master controller.

- **`tooling/self_correction_orchestrator.py`**:

  > Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.
  >
  > This script is the engine of the automated feedback loop. It reads structured,
  > actionable lessons from `knowledge_core/lessons.jsonl` and uses the
  > `protocol_updater.py` tool to apply them to the source protocol files.

- **`tooling/self_improvement_cli.py`**:

  > Analyzes agent activity logs to identify opportunities for self-improvement.
  >
  > This script is a command-line tool that serves as a key part of the agent's
  > meta-cognitive loop. It parses the structured activity log
  > (`logs/activity.log.jsonl`) to identify patterns that may indicate
  > inefficiencies or errors in the agent's workflow.
  >
  > The primary analysis currently implemented is:
  > - **Planning Efficiency Analysis:** It scans the logs for tasks that required
  >   multiple `set_plan` actions. A high number of plan revisions for a single
  >   task can suggest that the initial planning phase was insufficient, the task
  >   was poorly understood, or the agent struggled to adapt to unforeseen
  >   challenges.
  >
  > By flagging these tasks, the script provides a starting point for a deeper
  > post-mortem analysis, helping the agent (or its developers) to understand the
  > root causes of the planning churn and to develop strategies for more effective
  > upfront planning in the future.
  >
  > The tool is designed to be extensible, with future analyses (such as error
  > rate tracking or tool usage anti-patterns) to be added as the system evolves.

- **`tooling/state.py`**:

  > Defines the core data structures for managing the agent's state.
  >
  > This module provides the `AgentState` and `PlanContext` dataclasses, which are
  > fundamental to the operation of the Context-Free Development Cycle (CFDC). These
  > structures allow the `master_control.py` orchestrator to maintain a complete,
  > snapshot-able representation of the agent's progress through a task.
  >
  > - `AgentState`: The primary container for all information related to the current
  >   task, including the plan execution stack, message history, and error states.
  > - `PlanContext`: A specific structure that holds the state of a single plan
  >   file, including its content and the current execution step. This is the
  >   element that gets pushed onto the `plan_stack` in `AgentState`.
  >
  > Together, these classes enable the hierarchical, stack-based planning and
  > execution that is the hallmark of the CFDC.

- **`tooling/symbol_map_generator.py`**:

  > Generates a code symbol map for the repository to aid in contextual understanding.
  >
  > This script creates a `symbols.json` file in the `knowledge_core` directory,
  > which acts as a high-level index of the codebase. This map contains information
  > about key programming constructs like classes and functions, including their
  > name, location (file path and line number), and language.
  >
  > The script employs a two-tiered approach for symbol generation:
  > 1.  **Universal Ctags (Preferred):** It first checks for the presence of the
  >     `ctags` command-line tool. If available, it uses `ctags` to perform a
  >     comprehensive, multi-language scan of the repository. This is the most
  >     robust and accurate method.
  > 2.  **AST Fallback (Python-only):** If `ctags` is not found, the script falls
  >     back to using Python's built-in Abstract Syntax Tree (`ast`) module. This
  >     method parses all `.py` files and extracts symbol information for Python
  >     code. While less comprehensive than `ctags`, it ensures that a baseline
  >     symbol map is always available.
  >
  > The resulting `symbols.json` artifact is a critical input for the agent's
  > orientation and planning phases, allowing it to quickly locate relevant code
  > and understand the structure of the repository without having to read every file.