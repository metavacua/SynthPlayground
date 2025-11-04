# Autonomous Agent Protocol System

This repository contains a sophisticated, protocol-driven framework for the development and operation of autonomous AI agents. The system is designed to ensure that agent behavior is predictable, verifiable, and aligned with a set of core principles, which are encoded in a series of formal protocols.

## Key Features

- **Protocol-Driven Architecture**: The agent's behavior is governed by a set of formal protocols, which are defined in the `protocols/` directory. These protocols are compiled into a single, machine-readable `AGENTS.md` file, which serves as the agent's primary operational guide.
- **Comprehensive Tooling**: The `tooling/` directory contains a rich set of tools for building, testing, and maintaining the agent and its protocols. This includes a protocol compiler, a documentation builder, a test runner, and a variety of other utilities.
- **Self-Improvement Capabilities**: The agent is designed to be self-improving, with protocols that allow it to modify its own tooling and even its own protocols. This is a core feature of the system, and it is governed by a strict set of safeguards.
- **Formal Verification**: The system is designed to be formally verifiable, with a focus on decidability and computational tractability. This is a key aspect of the project, and it is reflected in the design of the agent's planning and execution language.

## Getting Started

To get started with this project, you will need to have Python 3 installed. You can then install the necessary dependencies by running the following command:

```bash
pip install -r tooling/requirements.txt
```

Once the dependencies are installed, you can build the project by running the following command:

```bash
python3 tooling/builder.py --target all
```

This will compile the protocols, integrate the knowledge sources, and generate the `AGENTS.md` file.

## The Protocol System

The protocol system is the heart of this project. It is designed to ensure that the agent's behavior is predictable, verifiable, and aligned with a set of core principles. The protocols are defined in the `protocols/` directory, and they are compiled into a single, machine-readable `AGENTS.md` file, which serves as the agent's primary operational guide.

The following protocols are currently defined:

- **`00_aorp-header.protocol.yaml`**: Defines the identity and versioning of the Advanced Orientation and Research Protocol (AORP).
- **`00_bootstrap.protocol.yaml`**: A foundational protocol that dictates the agent's initial actions upon starting any task.
- **`00_dependency-management.protocol.yaml`**: A protocol for ensuring a reliable execution environment through formal dependency management.
- **`00_experimental.protocol.yaml`**: An experimental protocol to test dynamic rule-following. It mandates a prologue action before file creation.
- **`00_security_header.protocol.yaml`**: Defines the identity and purpose of the Security Protocol document.
- **`01_agent_shell.protocol.yaml`**: A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.
- **`01_core-directive.protocol.yaml`**: The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).
- **`01_vulnerability_reporting.protocol.yaml`**: Defines the official policy and procedure for reporting security vulnerabilities.
- **`02_decidability-constraints.protocol.yaml`**: Ensures all development processes are formally decidable and computationally tractable.
- **`03_orientation-protocol.protocol.yaml`**: Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.
- **`04_fdc-protocol.protocol.yaml`**: Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.
- **`05_standing-orders.protocol.yaml`**: A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.
- **`06_best-practices.protocol.yaml`**: A set of best practices derived from observing successful, data-driven workflow patterns.
- **`07_meta-protocol.protocol.yaml`**: A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.
- **`08_toolchain_review.protocol.yaml`**: A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.
- **`09_context-free-development-cycle.protocol.yaml`**: Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.
- **`10_plan-registry.protocol.yaml`**: Defines a central registry for discovering and executing hierarchical plans by a logical name.
- **`12_self_correction.protocol.yaml`**: Defines the automated, closed-loop workflow for protocol self-correction.
- **`13_non-compliance.protocol.yaml`**: A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.
- **`14_pre-commit.protocol.yaml`**: Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission.
- **`16_research.protocol.yaml`**: A protocol for conducting systematic research using the integrated research toolchain.
- **`98_reset-all-prohibition.protocol.yaml`**: A high-priority protocol that unconditionally forbids the use of the `reset_all` tool.
- **`CHARTER.protocol.yaml`**: A charter of operational principles for the AI agent.
- **`GIT_WORKFLOW_PROTOCOL.yaml`**: A protocol for git workflow.
- **`auditor.protocol.yaml`**: A protocol for the unified repository auditing tool, which combines multiple health and compliance checks into a single interface.
- **`aura-execution.protocol.yaml`**: A protocol for executing Aura scripts, enabling a more expressive and powerful planning and automation language for the agent.
- **`browser_control.protocol.yaml`**: A protocol for controlling a web browser using the GeminiComputerUse tool.
- **`capability_verifier.protocol.yaml`**: A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.
- **`critic-meta-protocol-001.protocol.yaml`**: A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.
- **`critic-reset-prohibition-001.protocol.yaml`**: A specific, high-priority protocol that forbids the Code Review Critic agent from using the 'reset_all' tool.
- **`csdc.protocol.yaml`**: A protocol for the Context-Sensitive Development Cycle (CSDC), which introduces development models based on logical constraints.
- **`deep_research.protocol.yaml`**: A standardized, callable plan for conducting in-depth research on a complex topic.
- **`doc_builder.protocol.yaml`**: A protocol for the unified documentation builder, which generates various documentation artifacts from the repository's sources of truth.
- **`executable-demo.protocol.yaml`**: A demonstration of a protocol with executable code.
- **`external-api-integration-001.protocol.yaml`**: A protocol for standardized interaction with external agent APIs.
- **`file-indexing.protocol.yaml`**: A protocol for maintaining an up-to-date file index to accelerate tool performance.
- **`gemini-api-integration-001.protocol.yaml`**: A protocol for integrating with the Google Gemini API.
- **`guardian.protocol.yaml`**: A meta-protocol to ensure all autonomous actions, especially self-modification, are strategically sound and easily reviewable by humans.
- **`hdl-proving.protocol.yaml`**: A protocol for interacting with the Hypersequent-calculus-based logic engine, allowing the agent to perform formal logical proofs.
- **`hello_world.protocol.yaml`**: A protocol for greeting the world.
- **`interaction.protocol.yaml`**: A protocol governing the agent's core interaction and planning tools.
- **`meta_mutation.protocol.yaml`**: A protocol that empowers the agent to modify its own core tooling, enabling a recursive self-improvement cycle.
- **`plllu-execution.protocol.yaml`**: A protocol for executing pLLLU scripts, enabling a more expressive and powerful planning and automation language for the agent.
- **`research-cycle.protocol.yaml`**: Defines the formal Finite Development Cycle (FDC) for conducting deep research.
- **`self-improvement.protocol.yaml`**: A formal protocol for the agent to propose, validate, and implement improvements to its own operational protocols and tools.
- **`speculative_execution.protocol.yaml`**: A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods.
- **`test-driven-development.protocol.yaml`**: A protocol to enforce Test-Driven Development (TDD) practices.
- **`testing.protocol.yaml`**: A protocol for ensuring comprehensive testing of all new code.

## The Tooling System

The tooling system is a rich set of tools for building, testing, and maintaining the agent and its protocols. The tools are located in the `tooling/` directory, and they are designed to be used in a variety of contexts, from local development to continuous integration.

The following tools are currently available:

- **`__init__.py`**: This package, named 'Agent Smith', is a toolset designed for metamorphic
testing of the agent's core protocol compilation system.

It works by creating isolated sandbox environments, introducing mutations
(e.g., deleting a protocol file), running the protocol compiler, and verifying
that the resulting `AGENTS.md` artifact reflects the mutation as expected.
This allows for robust testing of the hierarchical compiler's resilience and
correctness.
- **`action_logger.py`**: No docstring found.
- **`agent_logic.py`**: No docstring found.
- **`agent_shell.py`**: The new, interactive, API-driven entry point for the agent.

This script replaces the old file-based signaling system with a direct,
programmatic interface to the MasterControlGraph FSM. It is responsible for:
1.  Initializing the agent's state and a centralized logger.
2.  Instantiating and running the MasterControlGraph.
3.  Driving the FSM by calling its methods and passing data and the logger.
4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans
    and respond to requests for action.
- **`analyze_data.py`**: No docstring found.
- **`analyzer.py`**: A constructive code analyzer for classifying Python code according to the Chomsky hierarchy.

This module provides the core logic for the "constructive" analysis of Python code.
It uses the `ast` module to parse Python code into an Abstract Syntax Tree (AST)
and then traverses the tree to identify key characteristics that determine the
computational complexity of the code.

The primary goal is to identify "witnesses" of decidability (e.g., primitive
recursion, bounded loops) and "counter-witnesses" (e.g., general recursion,
potential non-termination). This analysis provides the foundation for the
decidable refactoring toolchain.
- **`appl_logic.py`**: No docstring found.
- **`appl_runner.py`**: A command-line tool for executing APPL files.

This script provides a simple interface to run APPL files using the main
`run.py` interpreter. It captures and prints the output of the execution,
and provides detailed error reporting if the execution fails.
- **`appl_to_lfi_ill.py`**: A compiler that translates APPL (a simple functional language) to LFI-ILL.

This script takes a Python file containing an APPL AST, and compiles it into
an LFI-ILL AST. The resulting AST is then written to a `.lfi_ill` file.
- **`appl_to_lfi_ill_logic.py`**: No docstring found.
- **`ast_generator.py`**: No docstring found.
- **`auditor.py`**: A unified auditing tool for maintaining repository health and compliance.

This script combines the functionality of several disparate auditing tools into a
single, comprehensive command-line interface. It serves as the central tool for
validating the key components of the agent's architecture, including protocols,
plans, and documentation.

The auditor can perform the following checks:
1.  **Protocol Audit (`protocol`):**
    - Checks if `AGENTS.md` artifacts are stale compared to their source files.
    - Verifies protocol completeness by comparing tools used in logs against
      tools defined in protocols.
    - Analyzes tool usage frequency (centrality).
2.  **Plan Registry Audit (`plans`):**
    - Scans `knowledge_core/plan_registry.json` for "dead links" where the
      target plan file does not exist.
3.  **Documentation Audit (`docs`):**
    - Scans the generated `SYSTEM_DOCUMENTATION.md` to find Python modules
      that are missing module-level docstrings.

The tool is designed to be run from the command line and can execute specific
audits or all of them, generating a consolidated `audit_report.md` file.
- **`auditor_logic.py`**: No docstring found.
- **`aura_executor.py`**: This script serves as the command-line executor for `.aura` files.

It bridges the gap between the high-level Aura scripting language and the
agent's underlying Python-based toolset. The executor is responsible for:
1.  Parsing the `.aura` source code using the lexer and parser from the
    `aura_lang` package.
2.  Setting up an execution environment for the interpreter.
3.  Injecting a "tool-calling" capability into the Aura environment, which
    allows Aura scripts to dynamically invoke registered Python tools
    (e.g., `hdl_prover`, `environmental_probe`).
4.  Executing the parsed program and printing the final result.

This makes it a key component for enabling more expressive and complex
automation scripts for the agent.
- **`aura_logic.py`**: No docstring found.
- **`aura_to_lfi_ill.py`**: A compiler that translates AURA code to LFI-ILL.

This script takes an AURA file, parses it, and compiles it into an LFI-ILL
AST. The resulting AST is then written to a `.lfi_ill` file.
- **`aura_to_lfi_ill_logic.py`**: No docstring found.
- **`autonomous_agent.py`**: No docstring found.
- **`autonomous_agent_logic.py`**: No docstring found.
- **`background_researcher.py`**: This script performs a simulated research task in the background.
It takes a task ID as a command-line argument and writes its findings
to a temporary file that the main agent can poll.
- **`background_researcher_logic.py`**: No docstring found.
- **`bash_runner.py`**: No docstring found.
- **`build_logic.py`**: No docstring found.
- **`build_utils.py`**: No docstring found.
- **`builder.py`**: A unified, configuration-driven build script for the project.

This script serves as the central entry point for all build-related tasks, such
as generating documentation, compiling protocols, and running code quality checks.
It replaces a traditional Makefile's direct command execution with a more
structured, maintainable, and introspectable approach.

The core logic is driven by a `build_config.yaml` file, which defines a series
of "targets." Each target specifies:
- The `type` of target: "compiler" or "command".
- For "compiler" types: `compiler` script, `output`, `sources`, and `options`.
- For "command" types: the `command` to execute.

The configuration also defines "build_groups", which are ordered collections of
targets (e.g., "all", "quality").

This centralized builder provides several advantages:
- **Single Source of Truth:** The `build_config.yaml` file is the definitive
  source for all build logic.
- **Consistency:** Ensures all build tasks are executed in a uniform way.
- **Extensibility:** New build targets can be added by simply updating the
  configuration file.
- **Discoverability:** The script can list all available targets and groups.
- **`capability_verifier.py`**: A tool to verify that the agent can monotonically improve its capabilities.

This script is designed to provide a formal, automated test for the agent's
self-correction and learning mechanisms. It ensures that when the agent learns
a new capability, it does so without losing (regressing) any of its existing
capabilities. This is a critical safeguard for ensuring robust and reliable
agent evolution.

The tool works by orchestrating a four-step process:
1.  **Confirm Initial Failure:** It runs a specific test file that is known to
    fail, verifying that the agent currently lacks the target capability.
2.  **Invoke Self-Correction:** It simulates the discovery of a new "lesson" and
    triggers the `self_correction_orchestrator.py` script, which is responsible
    for integrating new knowledge and skills.
3.  **Confirm Final Success:** It runs the same test file again, confirming that
    the agent has successfully learned the new capability and the test now passes.
4.  **Check for Regressions:** It runs the full, existing test suite to ensure
    that the process of learning the new skill has not inadvertently broken any
    previously functional capabilities.

This provides a closed-loop verification of monotonic improvement, which is a
cornerstone of the agent's design philosophy.
- **`capability_verifier_logic.py`**: No docstring found.
- **`classify_repository.py`**: No docstring found.
- **`cli.py`**: A unified command-line interface for the Chomsky toolchain.

This script provides a single entry point for all the tools related to the
Chomsky hierarchy and decidability. It orchestrates the functionality of the
various components of the toolchain, such as the code analyzer and the
refactoring tools, providing a clear and contextually visible interface for
both human and agentic use.
- **`code_suggester.py`**: Handles the generation and application of autonomous code change suggestions.

This tool is a key component of the advanced self-correction loop. It is
designed to be invoked by the self-correction orchestrator when a lesson
contains a 'propose-code-change' action.

For its initial implementation, this tool acts as a structured executor. It
takes a lesson where the 'details' field contains a fully-formed git-style
merge diff and applies it to the target file. It does this by generating a
temporary, single-step plan file and signaling its location for the master
controller to execute.

This establishes the fundamental workflow for autonomous code modification,
decoupling the suggestion logic from the execution logic. Future iterations
can enhance this tool with more sophisticated code generation capabilities
(e.g., using an LLM to generate the diff from a natural language description)
without altering the core orchestration process.
- **`code_suggester_logic.py`**: No docstring found.
- **`compile_protocols.py`**: No docstring found.
- **`compile_protocols_logic.py`**: No docstring found.
- **`complexity_manager.py`**: A tool for managing the complexity of the codebase by orchestrating various analysis and refactoring tools.
- **`context_awareness_scanner.py`**: A tool for performing static analysis on a Python file to understand its context.

This script provides a "contextual awareness" scan of a specified Python file
to help an agent (or a human) understand its role, dependencies, and connections
within a larger codebase. This is crucial for planning complex changes or
refactoring efforts, as it provides a snapshot of the potential impact of
modifying a file.

The scanner performs three main functions:
1.  **Symbol Definition Analysis:** It uses Python's Abstract Syntax Tree (AST)
    module to parse the target file and identify all the functions and classes
    that are defined within it.
2.  **Import Analysis:** It also uses the AST to find all modules and symbols
    that the target file imports, revealing its dependencies on other parts of
    the codebase or external libraries.
3.  **Reference Finding:** It performs a repository-wide search to find all other
    files that reference the symbols defined in the target file. This helps to
    understand how the file is used by the rest of the system.

The final output is a detailed JSON report containing all of this information,
which can be used as a foundational artifact for automated planning or human review.
- **`context_awareness_scanner_logic.py`**: No docstring found.
- **`context_manager.py`**: A tool for managing the agent's contextual awareness by orchestrating various scanning and analysis tools.
- **`create_file.py`**: No docstring found.
- **`decision_tester.py`**: No docstring found.
- **`dependency_graph_generator.py`**: Scans the repository for dependency files and generates a unified dependency graph.

This script is a crucial component of the agent's environmental awareness,
providing a clear map of the software supply chain. It recursively searches the
entire repository for common dependency management files, specifically:
- `package.json` (for JavaScript/Node.js projects)
- `requirements.txt` (for Python projects)

It parses these files to identify two key types of relationships:
1.  **Internal Dependencies:** Links between different projects within this repository.
2.  **External Dependencies:** Links to third-party libraries and packages.

The final output is a JSON file, `knowledge_core/dependency_graph.json`, which
represents these relationships as a graph structure with nodes (projects and
dependencies) and edges (the dependency links). This artifact is a primary
input for the agent's orientation and planning phases, allowing it to reason
about the potential impact of its changes.
- **`dependency_graph_generator_logic.py`**: No docstring found.
- **`doc_builder.py`**: A unified documentation builder for the project.
...
- **`doc_builder_logic.py`**: No docstring found.
- **`document_scanner.py`**: A tool for scanning the repository for human-readable documents and extracting their text content.

This script is a crucial component of the agent's initial information-gathering
and orientation phase. It allows the agent to ingest knowledge from unstructured
or semi-structured documents that are not part of the formal codebase, but which
may contain critical context, requirements, or specifications.

The scanner searches a given directory for files with common document extensions:
- `.pdf`: Uses the Gemini API to extract text and understand the content of PDF files.
- `.md`: Reads Markdown files.
- `.txt`: Reads plain text files.

The output is a dictionary where the keys are the file paths of the discovered
documents and the values are their extracted text content. This data can then
be used by the agent to inform its planning and execution process. This tool
is essential for bridging the gap between human-written documentation and the
agent's operational awareness.
- **`domain.py`**: No docstring found.
- **`environmental_probe.py`**: Performs a series of checks to assess the capabilities of the execution environment.

This script is a critical diagnostic tool run at the beginning of a task to
ensure the agent understands its operational sandbox. It verifies fundamental
capabilities required for most software development tasks:

1.  **Filesystem I/O:** Confirms that the agent can create, write to, read from,
    and delete files. It also provides a basic latency measurement for these
    operations.
2.  **Network Connectivity:** Checks for external network access by attempting to
    connect to a highly-available public endpoint (google.com). This is crucial
    for tasks requiring `git` operations, package downloads, or API calls.
3.  **Environment Variables:** Verifies that standard environment variables are
    accessible, which is a prerequisite for many command-line tools.

The script generates a human-readable report summarizing the results of these
probes, allowing the agent to quickly identify any environmental constraints
that might impact its ability to complete a task.
- **`external_api_client.py`**: A standardized client for interacting with external agent APIs.
- **`fdc_cli.py`**: This script provides a command-line interface (CLI) for managing the Finite
Development Cycle (FDC).

The FDC is a structured workflow for agent-driven software development. This CLI
is the primary human interface for interacting with that cycle, providing
commands to:
- **start:** Initiates a new development task, triggering the "Advanced
  Orientation and Research Protocol" (AORP) to ensure the agent is fully
  contextualized.
- **close:** Formally concludes a task, creating a post-mortem template for
  analysis and lesson-learning.
- **validate:** Checks a given plan file for both syntactic and semantic
  correctness against the FDC's governing Finite State Machine (FSM). This
  ensures that a plan is executable and will not violate protocol.
- **analyze:** Examines a plan to determine its computational complexity (e.g.,
  Constant, Polynomial, Exponential) and its modality (Read-Only vs.
  Read-Write), providing insight into the plan's potential impact.
- **`fdc_cli_logic.py`**: No docstring found.
- **`fetch_data.py`**: No docstring found.
- **`file_reader.py`**: No docstring found.
- **`filesystem_lister.py`**: A tool for listing files and directories in a repository, with an option to respect .gitignore.
- **`gemini_computer_use.py`**: A tool for controlling a web browser using the Gemini Computer Use API.

This tool allows the agent to perform tasks like data entry, automated testing,
and web research by controlling a web browser. It uses the Gemini Computer Use
API to "see" the screen and "act" by generating UI actions like mouse clicks
and keyboard inputs.
- **`generate_and_test.py`**: A command-line tool for orchestrating the metamorphic testing of the
hierarchical protocol compiler.

This script automates the following workflow:
1.  Creates a clean, isolated sandbox environment.
2.  Copies the necessary protocol source files and the compiler tooling into
    the sandbox.
3.  Installs required Python dependencies within the sandbox.
4.  Applies a specified mutation to the protocol sources (e.g., deleting a file).
5.  Runs the `hierarchical_compiler.py` within the sandbox to generate a
    variant `AGENTS.md` file.
6.  Verifies that the generated artifact correctly reflects the mutation.

This allows for automated, repeatable testing of the compiler's behavior
under various source conditions.
- **`generate_filesystem_rdf.py`**: No docstring found.
- **`goal_generator.py`**: This module provides a simple way to select a plan for the agent.
- **`guardian.py`**: No docstring found.
- **`halting_heuristic_analyzer.py`**: A static analysis tool to estimate the termination risk of a UDC plan.

This script reads a `.udc` plan file, parses its instructions, and uses a
series of heuristics to identify potential infinite loops. It is not a
formal decider (as the halting problem is undecidable), but rather a
practical tool to flag common patterns that lead to non-termination.

The analysis focuses on:
1.  Detecting backward jumps, which are the primary indicator of loops.
2.  Analyzing the exit conditions of these loops (e.g., `JE`, `JNE`).
3.  Checking if the registers involved in the exit conditions are modified
    within the loop body in a way that is likely to lead to termination.

The tool outputs a JSON report detailing the estimated risk level (LOW,
MEDIUM, HIGH) and the specific loops that were identified.
- **`hdl_parser.py`**: No docstring found.
- **`hdl_prover.py`**: A command-line tool for proving sequents in Intuitionistic Linear Logic.

This script provides a basic interface to a simple logic prover. It takes a
sequent as a command-line argument, parses it into a logical structure, and
then attempts to prove it using a rudimentary proof search algorithm.

The primary purpose of this tool is to allow the agent to perform formal
reasoning and verification tasks by checking the validity of logical entailments.
For example, it can be a used to verify that a certain conclusion follows from a
set of premises according to the rules of linear logic.

The current implementation uses a very basic parser and proof algorithm,
serving as a placeholder and demonstration for a more sophisticated, underlying
logic engine.
- **`hello_world.py`**: No docstring found.
- **`interpreter.py`**: No docstring found.
- **`json_to_yaml_ld.py`**: No docstring found.
- **`knowledge_compiler.py`**: Extracts structured lessons from post-mortem reports and compiles them into a
centralized, long-term knowledge base.

This script is a core component of the agent's self-improvement feedback loop.
After a task is completed, a post-mortem report is generated that includes a
section for "Corrective Actions & Lessons Learned." This script automates the
process of parsing that section to extract key insights.

It identifies pairs of "Lesson" and "Action" statements and transforms them
into a standardized, machine-readable format. These formatted entries are then
appended to the `knowledge_core/lessons.jsonl` file, which serves as the
agent's persistent memory of what has worked, what has failed, and what can be
improved in future tasks.

The script is executed via the command line, taking the path to a completed
post-mortem file as its primary argument.
- **`knowledge_integrator.py`**: No docstring found.
- **`lba_validator.py`**: A Linear Bounded Automaton (LBA) for validating Context-Sensitive Development Cycle (CSDC) plans.

This module implements a validator that enforces the context-sensitive rules of the CSDC.
Unlike a simple FSM, an LBA can inspect the entire input "tape" (the plan) to make
validation decisions. This is necessary to enforce rules where the validity of one
command depends on the presence or absence of another command elsewhere in the plan.

The CSDC defines two mutually exclusive models:
- Model A: Permits `define_set_of_names`, but forbids `define_diagonalization_function`.
- Model B: Permits `define_diagonalization_function`, but forbids `define_set_of_names`.

This validator checks for these co-occurrence constraints.
- **`lfi_ill_halting_decider.py`**: A tool for analyzing the termination of LFI-ILL programs.

This script takes an LFI-ILL file, interprets it in a paraconsistent logic
environment, and reports on its halting status. It does this by setting up
a paradoxical initial state and observing how the program resolves it.
- **`lfi_udc_model.py`**: A paraconsistent execution model for UDC plans.

This module provides the classes necessary to interpret a UDC (Un-decidable
Computation) plan within a Logic of Formal Inconsistency (LFI). Instead of
concrete values, the state of the machine (registers, tape, etc.) is modeled
using paraconsistent truth values (TRUE, FALSE, BOTH, NEITHER).

This allows the system to reason about paradoxical programs, such as a program
that halts if and only if it does not halt. By executing the program under
paraconsistent semantics, the model can arrive at a final state of `BOTH`,
effectively demonstrating the paradoxical nature of the input without crashing.

Key classes:
- `ParaconsistentTruth`: An enum for the four truth values.
- `ParaconsistentState`: A wrapper for a value that holds a paraconsistent truth.
- `LFIInstruction`: A UDC instruction that operates on paraconsistent states.
- `LFIExecutor`: A virtual machine that executes a UDC plan using LFI semantics.
- `ParaconsistentHaltingDecider`: The main entry point that orchestrates the
  analysis of a UDC plan.
- **`log_failure.py`**: A dedicated script to log a catastrophic failure event to the main activity log.

This tool is designed to be invoked in the rare case of a severe, unrecoverable
error that violates a core protocol. Its primary purpose is to ensure that such
a critical event is formally and structurally documented in the standard agent
activity log (`logs/activity.log.jsonl`), even if the main agent loop has
crashed or been terminated.

The script is pre-configured to log a `SYSTEM_FAILURE` event, specifically
attributing it to the "Unauthorized use of the `reset_all` tool." This creates a
permanent, machine-readable record of the failure, which is essential for
post-mortem analysis, debugging, and the development of future safeguards.

By using the standard `Logger` class, it ensures that the failure log entry
conforms to the established `LOGGING_SCHEMA.md`, making it processable by
auditing and analysis tools.
- **`master_agents_md_generator.py`**: No docstring found.
- **`master_control.py`**: The master orchestrator for the agent's lifecycle, implementing the Context-Free Development Cycle (CFDC).

This script, master_control.py, is the heart of the agent's operational loop.
It implements the CFDC, a hierarchical planning and execution model based on a
Pushdown Automaton. This allows the agent to execute complex tasks by calling
plans as sub-routines.

Core Responsibilities:
- **Hierarchical Plan Execution:** Manages a plan execution stack to enable
  plans to call other plans via the `call_plan` directive. This allows for
  modular, reusable, and complex task decomposition. A maximum recursion depth
  is enforced to guarantee decidability.
- **Plan Validation:** Contains the in-memory plan validator. Before execution,
  it parses a plan and simulates its execution against a Finite State Machine
  (FSM) to ensure it complies with the agent's operational protocols.
- **"Registry-First" Plan Resolution:** When resolving a `call_plan` directive,
  it first attempts to look up the plan by its logical name in the
  `knowledge_core/plan_registry.json`. If not found, it falls back to treating
  the argument as a direct file path.
- **FSM-Governed Lifecycle:** The entire workflow, from orientation to
  finalization, is governed by a strict FSM definition (e.g., `tooling/fsm.json`)
  to ensure predictable and auditable behavior.

This module is designed as a library to be controlled by an external shell
(e.g., `agent_shell.py`), making its interaction purely programmatic.
- **`master_control_cli.py`**: The official command-line interface for the agent's master control loop.

This script is now a lightweight wrapper that passes control to the new,
API-driven `agent_shell.py`. It preserves the command-line interface while
decoupling the entry point from the FSM implementation.
- **`message_user.py`**: A dummy tool that prints its arguments to simulate the message_user tool.

This script is a simple command-line utility that takes a string as an
argument and prints it to standard output, prefixed with "[Message User]:".
Its purpose is to serve as a stand-in or mock for the actual `message_user`
tool in testing environments where the full agent framework is not required.

This allows for the testing of scripts or workflows that call the
`message_user` tool without needing to invoke the entire agent messaging
subsystem.
- **`migrate_protocols.py`**: No docstring found.
- **`parser.py`**: No docstring found.
- **`plan_executor.py`**: A simple plan executor for simulating agent behavior.

This script reads a plan file, parses it, and executes the commands in a
simplified, simulated environment. It supports a limited set of tools
(`message_user` and `run_in_bash_session`) to provide a basic demonstration
of how an agent would execute a plan.
- **`plan_generator.py`**: No docstring found.
- **`plan_manager.py`**: Provides a command-line interface for managing the agent's Plan Registry.

This script is the administrative tool for the Plan Registry, a key component
of the Context-Free Development Cycle (CFDC) that enables hierarchical and
modular planning. The registry, located at `knowledge_core/plan_registry.json`,
maps human-readable, logical names to the file paths of specific plans. This
decouples the `call_plan` directive from hardcoded file paths, making plans
more reusable and the system more robust.

This CLI provides three essential functions:
- **register**: Associates a new logical name with a plan file path, adding it
  to the central registry.
- **deregister**: Removes an existing logical name and its associated path from
  the registry.
- **list**: Displays all current name-to-path mappings in the registry.

By providing a simple, standardized interface for managing this library of
reusable plans, this tool improves the agent's ability to compose complex
workflows from smaller, validated sub-plans.
- **`plan_parser.py`**: Parses a plan file into a structured list of commands.

This module provides the `parse_plan` function and the `Command` dataclass,
which are central to the agent's ability to understand and execute plans.
The parser correctly handles multi-line arguments and ignores comments,
allowing for robust and readable plan files.
- **`plan_runner.py`**: A self-executing plan runner for Jules, the AI agent.

This script reads a plan file in a specific format, executes the commands,
verifies their success, and handles failures.
- **`plllu_interpreter.py`**: A resource-sensitive, four-valued interpreter for pLLLU formulas.

This script implements an interpreter for the pLLLU language. It operates on
an AST generated by the `plllu_parser.py` script. The interpreter is designed
to be resource-sensitive, meaning that each atomic formula in the initial
context must be consumed exactly once during the evaluation of the proof.

The logic is four-valued, supporting TRUE, FALSE, BOTH, and NEITHER, allowing
it to reason about paraconsistent and paracomplete states.

The core of the interpreter is the `FourValuedInterpreter` class, which
recursively walks the AST, consuming resources from a context (a Counter of
available atoms) and returning the resulting logical value.
- **`plllu_lexer.py`**: No docstring found.
- **`plllu_parser.py`**: A parser for pLLLU (paraconsistent Linear Logic with Undeterminedness) formulas.

This script uses the PLY (Python Lex-Yacc) library to define a
parser for a simple, string-based representation of pLLLU formulas. It can
handle basic atomic formulas, unary operators (like negation and consistency),
and binary operators (like implication and conjunction).

The main function `parse_formula` takes a string and returns a simple AST
(Abstract Syntax Tree) represented as nested tuples.
- **`plllu_runner.py`**: A command-line runner for pLLLU files.

This script provides an entry point for executing `.plllu` files. It
integrates the pLLLU lexer, parser, and interpreter to execute the logic
defined in a given pLLLU source file and print the result.
- **`pre_submit_check.py`**: A pre-submission script that runs a series of checks to ensure code quality
and adherence to repository protocols before a commit is made.

This script currently includes the following checks:
1.  **Code Linting:** Runs `make lint` to check for style issues (currently disabled).
2.  **Docstring Enforcement:** Ensures all Python files in key directories have
    module-level docstrings.
3.  **Guardian Protocol Validation:** Validates any staged review documents
    against the Guardian Protocol.

The script is designed to be easily extensible with additional checks.
- **`process_witnesses.py`**: No docstring found.
- **`protocol_compiler.py`**: No docstring found.
- **`protocol_manager.py`**: A command-line tool for managing agent protocols.

This script provides a set of commands for creating, testing, and versioning
agent protocols. It is designed to be used by developers to manage the
protocol lifecycle.
- **`protocol_migration_tool.py`**: A tool to migrate protocols from the old, manual AGENTS.md format to the new,
structured, and compiler-friendly format.

This script is designed to be a one-time migration utility that helps to
transition the valuable, detailed protocols from the original AGENTS.md file
into a format that can be processed by the new, dynamic build system.

The tool works by:
1.  Reading the `AGENTS.md.bak` file, which is a backup of the original.
2.  Parsing the file to identify the distinct protocol sections (Phase 1-6 and
    the "STANDING ORDER").
3.  Creating a new `protocols/manual_protocol/` directory to house the
    migrated protocols.
4.  Writing each extracted protocol into its own formatted Markdown file within
    the new directory.

This ensures that the protocols are preserved and integrated into the new
system without requiring manual copying and pasting.
- **`protocol_oracle.py`**: No docstring found.
- **`protocol_updater.py`**: A command-line tool for programmatically updating protocol source files.

This script provides the mechanism for the agent to perform self-correction
by modifying its own governing protocols based on structured, actionable
lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)
workflow.

The tool operates on the .protocol.json files located in the `protocols/`
directory, performing targeted updates based on command-line arguments.
- **`py_to_udc.py`**: A tool for converting Python code to UDC assembly-like code.
- **`read_file.py`**: No docstring found.
- **`refactor.py`**: A tool for performing automated symbol renaming in Python code.

This script provides a command-line interface to find a specific symbol
(a function or a class) in a given Python file and rename it, along with all of
its textual references throughout the entire repository. This provides a safe
and automated way to perform a common refactoring task, reducing the risk of
manual errors.
- **`refactor_add_fuel.py`**: A tool for refactoring a Python function to use a "fuel"-based approach to recursion.
This tool is designed to be idempotent and handle nested while loops.
- **`refactor_cf_to_r.py`**: A tool for refactoring context-free Python code into regular components.
- **`refactor_cs_to_cf.py`**: A tool for refactoring context-sensitive Python code into context-free components.
- **`reliable_ls.py`**: A tool for reliably listing files and directories.

This script provides a consistent, sorted, and recursive listing of files and
directories, excluding the `.git` directory. It is intended to be a more
reliable alternative to the standard `ls` command for agent use cases.
- **`reorientation_manager.py`**: Re-orientation Manager

This script is the core of the automated re-orientation process. It is
designed to be triggered by the build system whenever the agent's core
protocols (`AGENTS.md`) are re-compiled.

The manager performs the following key functions:
1.  **Diff Analysis:** It compares the old version of AGENTS.md with the new
    version to identify new protocols, tools, or other key concepts that have
    been introduced.
2.  **Temporal Orientation (Shallow Research):** For each new concept, it
    invokes the `temporal_orienter.py` tool to fetch a high-level summary from
    an external knowledge base like DBpedia. This ensures the agent has a
    baseline understanding of new terms.
3.  **Knowledge Storage:** The summaries from the temporal orientation are
    stored in a structured JSON file (`knowledge_core/temporal_orientations.json`),
    creating a persistent, queryable knowledge artifact.
4.  **Deep Research Trigger:** It analyzes the nature of the changes. If a
    change is deemed significant (e.g., the addition of a new core
    architectural protocol), it programmatically triggers a formal L4 Deep
    Research Cycle by creating a `deep_research_required.json` file.

This automated workflow ensures that the agent never operates with an outdated
understanding of its own protocols. It closes the loop between protocol
modification and the agent's self-awareness, making the system more robust,
adaptive, and reliable.
- **`research.py`**: This module contains the logic for executing research tasks based on a set of
constraints. It acts as a dispatcher, calling the appropriate tool (e.g.,
read_file, google_search) based on the specified target and scope.
- **`research_planner.py`**: This module is responsible for generating a formal, FSM-compliant research plan
for a given topic. The output is a string that can be executed by the agent's
master controller.
- **`run_tests.py`**: No docstring found.
- **`self_correction_orchestrator.py`**: Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.

This script is the engine of the automated feedback loop. It reads structured,
actionable lessons from `knowledge_core/lessons.jsonl` and uses the
`protocol_updater.py` tool to apply them to the source protocol files.
- **`self_improvement_cli.py`**: Analyzes agent activity logs to identify opportunities for self-improvement.

This script is a command-line tool that serves as a key part of the agent's
meta-cognitive loop. It parses the structured activity log
(`logs/activity.log.jsonl`) to identify patterns that may indicate
inefficiencies or errors in the agent's workflow.

The primary analysis currently implemented is:
- **Planning Efficiency Analysis:** It scans the logs for tasks that required
  multiple `set_plan` actions. A high number of plan revisions for a single
  task can suggest that the initial planning phase was insufficient, the task
  was poorly understood, or the agent struggled to adapt to unforeseen
  challenges.

By flagging these tasks, the script provides a starting point for a deeper
post-mortem analysis, helping the agent (or its developers) to understand the
root causes of the planning churn and to develop strategies for more effective
upfront planning in the future.

The tool is designed to be extensible, with future analyses (such as error
rate tracking or tool usage anti-patterns) to be added as the system evolves.
- **`session_manager.py`**: This module provides a simple way to save and load the agent's session.
- **`state.py`**: Defines the core data structures for managing the agent's state.

This module provides the `AgentState` and `PlanContext` dataclasses, which are
fundamental to the operation of the Context-Free Development Cycle (CFDC). These
structures allow the `master_control.py` orchestrator to maintain a complete,
snapshot-able representation of the agent's progress through a task.

- `AgentState`: The primary container for all information related to the current
  task, including the plan execution stack, message history, and error states.
- `PlanContext`: A specific structure that holds the state of a single plan
  file, including its content and the current execution step. This is the
  element that gets pushed onto the `plan_stack` in `AgentState`.

Together, these classes enable the hierarchical, stack-based planning and
execution that is the hallmark of the CFDC.
- **`symbol_extractor.py`**: No docstring found.
- **`symbol_map_generator.py`**: Generates a code symbol map for the repository to aid in contextual understanding.

This script creates a `symbols.json` file in the `knowledge_core` directory,
which acts as a high-level index of the codebase. This map contains information
about key programming constructs like classes and functions, including their
name, location (file path and line number), and language.

The script employs a two-tiered approach for symbol generation:
1.  **Universal Ctags (Preferred):** It first checks for the presence of the
    `ctags` command-line tool. If available, it uses `ctags` to perform a
    comprehensive, multi-language scan of the repository. This is the most
    robust and accurate method.
2.  **AST Fallback (Python-only):** If `ctags` is not found, the script falls
    back to using Python's built-in Abstract Syntax Tree (`ast`) module. This
    method parses all `.py` files and extracts symbol information for Python
    code. While less comprehensive than `ctags`, it ensures that a baseline
    symbol map is always available.

The resulting `symbols.json` artifact is a critical input for the agent's
orientation and planning phases, allowing it to quickly locate relevant code
and understand the structure of the repository without having to read every file.
- **`temporal_orienter.py`**: A tool for performing temporal orientation by fetching a summary of a concept from DBPedia.
- **`udc_orchestrator.py`**: An orchestrator for executing Unrestricted Development Cycle (UDC) plans.

This script provides a sandboxed environment for running UDC plans, which are
low-level assembly-like programs that can perform Turing-complete computations.
The orchestrator acts as a virtual machine with a tape-based memory model,
registers, and a set of simple instructions.

To prevent non-termination and other resource-exhaustion issues, the
orchestrator imposes strict limits on the number of instructions executed,
the amount of memory used, and the total wall-clock time.
- **`untested_code_detector.py`**: No docstring found.
- **`unused_import_remover.py`**: No docstring found.
- **`validate_tdd.py`**: No docstring found.
