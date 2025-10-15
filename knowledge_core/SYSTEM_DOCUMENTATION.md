# System Documentation

---

## `/app/tooling/` Directory

### `/app/tooling/__init__.py`

This directory contains the core tooling for the agent's development,
build, and self-analysis capabilities.

### `/app/tooling/agent_shell.py`

The new, interactive, API-driven entry point for the agent.

This script replaces the old file-based signaling system with a direct,
programmatic interface to the MasterControlGraph FSM. It is responsible for:
1.  Initializing the agent's state and a centralized logger.
2.  Instantiating and running the MasterControlGraph.
3.  Driving the FSM by calling its methods and passing data and the logger.
4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans
    and respond to requests for action.


**Public Functions:**


- #### `def find_fsm_transition(fsm, source_state, trigger)`

  > Finds the destination state for a given source and trigger.


- #### `def main()`

  > Main entry point for the agent shell.


- #### `def run_agent_loop(task_description)`

  > The main loop that drives the agent's lifecycle via the FSM.


### `/app/tooling/aura_executor.py`

This script serves as the command-line executor for `.aura` files.

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


**Public Functions:**


- #### `def dynamic_agent_call_tool(tool_name, *args)`

  > Dynamically imports and calls a tool from the 'tooling' directory.
  > Tool name should be the module name, without .py.


- #### `def main()`

  > Main entry point for the Aura script executor.


### `/app/tooling/background_researcher.py`

This script performs a simulated research task in the background.
It takes a task ID as a command-line argument and writes its findings
to a temporary file that the main agent can poll.


**Public Functions:**


- #### `def perform_research(task_id)`

  > Simulates a research task and writes the result to a file.


### `/app/tooling/builder.py`

The unified build script for this repository.

This script replaces a complex Makefile with a single, data-driven entry point
for all build-related tasks. It reads its configuration from `build_config.json`,
which defines a series of build "targets."

Each target specifies a "compiler" (a Python script in the `tooling/` directory),
input sources, and an output artifact. This script is responsible for
orchestrating the execution of these compilers in the correct order to generate
all necessary project artifacts, such as `AGENTS.md`, `README.md`, and
`SYSTEM_DOCUMENTATION.md`.

This centralized approach makes the build process more transparent, maintainable,
and easier to extend.


**Public Functions:**


- #### `def execute_build(target_name, config)`

  > Executes the build process for a specific target defined in the config.


- #### `def load_config()`

  > Loads the build configuration file.


- #### `def main()`

  > Main function to parse arguments and drive the build process.


### `/app/tooling/code_health_analyzer.py`

Audits the Plan Registry for dead links and generates a corrective plan.

This script scans the `knowledge_core/plan_registry.json` file, which maps
logical plan names to their file paths. It checks if each file path in the
registry points to an existing file.

If any "dead links" (entries pointing to non-existent files) are found,
this script will:
1.  Identify the invalid entries.
2.  Generate a new, corrected version of the plan registry with the dead links
    removed.
3.  Print a complete, executable plan to the console. This plan uses the
    `overwrite_file_with_block` command to replace the old registry with the
    new, corrected version.

This provides a semi-automated way to maintain the integrity of the Plan
Registry, a key component of the hierarchical planning system.


**Public Functions:**


- #### `def generate_plan_to_fix_dead_links(dead_links, current_registry)`

  > Generates a plan using `overwrite_file_with_block` to fix dead links.


- #### `def get_dead_links_and_content()`

  > Audits the plan registry, returns a list of dead links and the original content.


- #### `def main()`

  > Main entry point for the code health analyzer.
  > Identifies dead links and prints a plan to fix them.


### `/app/tooling/code_suggester.py`

Handles the generation and application of autonomous code change suggestions.

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


**Public Functions:**


- #### `def generate_suggestion_plan(filepath, diff_content)`

  > Generates a temporary, single-step plan file to apply a code change.
  >
  > Args:
  >     filepath: The path to the file that needs to be modified.
  >     diff_content: The git-style merge diff block to be applied.
  >
  > Returns:
  >     The path to the generated temporary plan file.


- #### `def main()`

  > Main entry point for the code suggester tool.
  > Parses arguments, generates a plan, and prints the plan's path to stdout.


### `/app/tooling/context_awareness_scanner.py`

Performs static analysis on a Python file to map its contextual role.

This script acts as a code intelligence tool. Given a Python file, it performs
a static analysis to understand its connections to the rest of the codebase.
It generates a detailed JSON report that includes:

1.  **Defined Symbols:** All functions and classes defined within the target file,
    along with their line numbers.
2.  **Imported Symbols:** All modules and symbols that the target file imports
    from other modules.
3.  **Cross-Repository References:** For each function and class defined in the
    target file, it finds all other Python files in the repository that
    reference that symbol.

The resulting report provides a comprehensive "contextual awareness map" for a
single file, showing what it provides to the system and what it consumes from
it. This is invaluable for understanding the impact of potential changes.


**Public Functions:**


- #### `def find_references(symbol_name, search_path)`

  > Finds all files in a directory that reference a given symbol.


- #### `def get_defined_symbols(filepath)`

  > Parses a Python file to find all defined functions and classes.


- #### `def get_imported_symbols(filepath)`

  > Parses a Python file to find all imported modules and symbols.


- #### `def main()`


### `/app/tooling/dependency_graph_generator.py`

Scans the repository for dependency files and generates a unified dependency graph.

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


**Public Functions:**


- #### `def find_package_json_files(root_dir)`

  > Finds all package.json files in the repository, excluding node_modules.


- #### `def find_requirements_txt_files(root_dir)`

  > Finds all requirements.txt files in the repository.


- #### `def generate_dependency_graph(root_dir='.')`

  > Generates a dependency graph for all supported dependency files found.


- #### `def main()`

  > Main function to generate and save the dependency graph.


- #### `def parse_package_json(package_json_path)`

  > Parses a single package.json file to extract its name and dependencies.


- #### `def parse_requirements_txt(requirements_path, root_dir)`

  > Parses a requirements.txt file to extract its dependencies.


### `/app/tooling/doc_auditor.py`

This script provides a tool for auditing the completeness of the system documentation.

It scans the generated `SYSTEM_DOCUMENTATION.md` file and searches for a specific
pattern: a module header followed immediately by the text "_No module-level
docstring found._". This pattern indicates that the `doc_generator.py` script
was unable to find a docstring for that particular Python module.

The auditor then prints a list of all such files, providing a clear and
actionable report of which modules require documentation. This is a key tool for
maintaining code health and ensuring that the agent's knowledge base is complete.


**Public Functions:**


- #### `def audit_documentation(filepath)`

  > Scans the system documentation file for modules missing docstrings.
  >
  > Args:
  >     filepath: The path to the SYSTEM_DOCUMENTATION.md file.
  >
  > Returns:
  >     A list of file paths for modules that are missing docstrings.


- #### `def main()`

  > Command-line interface for the documentation auditor.


### `/app/tooling/doc_generator.py`

Generates detailed system documentation from Python source files.

This script scans specified directories for Python files, parses their
Abstract Syntax Trees (ASTs), and extracts documentation for the module,
classes, and functions. The output is a structured Markdown file.

This is a key component of the project's self-documentation capabilities,
powering the `SYSTEM_DOCUMENTATION.md` artifact in the `knowledge_core`.

The script is configured via top-level constants:
- `SCAN_DIRECTORIES`: A list of directories to search for .py files.
- `OUTPUT_FILE`: The path where the final Markdown file will be written.
- `DOC_TITLE`: The main title for the generated documentation file.

It uses Python's `ast` module to reliably parse source files without
importing them, which avoids issues with dependencies or script side-effects.


**Public Functions:**


- #### `def find_python_files(directories)`

  > Finds all Python files in the given directories, ignoring test files.


- #### `def format_args(args)`

  > Formats ast.arguments into a printable string, including defaults.


- #### `def generate_documentation(all_docs)`

  > Generates a single Markdown string from a list of ModuleDoc objects.


- #### `def generate_documentation_for_module(mod_doc)`

  > Generates Markdown content for a single module.


- #### `def main(source_dirs, output_file)`

  > Main function to find files, parse them, and write documentation.


- #### `def parse_file_for_docs(filepath)`

  > Parses a Python file and extracts documentation for its module, classes,
  > and functions.



**Public Classes:**


- #### `class ClassDoc`

  > Holds documentation for a single class.


  **Methods:**

  - ##### `def __init__(self, name, docstring, methods)`


- #### `class DocVisitor`

  > AST visitor to extract documentation from classes and functions.
  > It navigates the tree and builds lists of discovered documentation objects.


  **Methods:**

  - ##### `def __init__(self)`

  - ##### `def visit_ClassDef(self, node)`

  - ##### `def visit_FunctionDef(self, node)`


- #### `class FunctionDoc`

  > Holds documentation for a single function or method.


  **Methods:**

  - ##### `def __init__(self, name, signature, docstring)`


- #### `class ModuleDoc`

  > Holds all documentation for a single Python module.


  **Methods:**

  - ##### `def __init__(self, name, docstring, classes, functions)`


### `/app/tooling/document_scanner.py`

Recursively scans a directory to find and extract text from documents.

This script provides a crucial capability for the agent's orientation phase.
It walks through a given directory structure and identifies files with common
document extensions: `.pdf`, `.md`, and `.txt`.

For each file found, it attempts to extract the full text content:
- For `.pdf` files, it uses the `pypdf` library to parse the document and
  extract text from each page.
- For `.md` and `.txt` files, it reads the raw text content.

The script returns a dictionary where the keys are the file paths of the
scanned documents and the values are their extracted text content. This allows
the agent to gather a broad base of knowledge from the human-readable
documentation available in a repository.


**Public Functions:**


- #### `def scan_documents(directory='.')`

  > Scans a directory for PDF, Markdown, and text files and extracts their content.


### `/app/tooling/environmental_probe.py`

Performs a series of checks to assess the capabilities of the execution environment.

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


**Public Functions:**


- #### `def main()`

  > Runs all environmental probes and prints a summary report.


- #### `def probe_environment_variables()`

  > Checks for the presence of a common environment variable.


- #### `def probe_filesystem()`

  > Tests file system write/read/delete capabilities and measures latency.


- #### `def probe_network()`

  > Tests network connectivity and measures latency to a reliable external endpoint.


### `/app/tooling/fdc_cli.py`

This script provides a command-line interface (CLI) for managing the Finite
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


**Public Functions:**


- #### `def analyze_plan(plan_filepath)`

  > Analyzes a plan file to determine its complexity class and modality.


- #### `def close_task(task_id)`

  > Automates the closing of a Finite Development Cycle.


- #### `def main()`


- #### `def start_task(task_id)`

  > Initiates the AORP cascade for a new task.


- #### `def validate_plan(plan_filepath)`


### `/app/tooling/generate_docs.py`

This script generates comprehensive Markdown documentation for the agent's
architecture, including the FSM, the agent shell, and the master control script.


**Public Functions:**


- #### `def generate_documentation()`

  > Generates the final Markdown documentation.


- #### `def get_fsm_details()`

  > Extracts FSM states and transitions from fsm.json.


- #### `def get_master_control_details()`

  > Extracts details about the master control script's state handlers.


### `/app/tooling/hdl_prover.py`

A command-line interface for a simple Hypersequent-calculus-based logic prover.

This script provides a tool for checking the provability of a logical sequent
formatted for a subset of Intuitionistic Linear Logic. It is governed by the
`hdl-proving-001` protocol.

The script takes a sequent as a command-line argument (e.g., "A, A -> B |- B"),
parses it into a formal data structure, and then uses a simple proof search
algorithm to determine if the sequent is provable.

NOTE: The current proof search implementation is a basic placeholder and is not
a complete or sound prover. It is intended as a scaffold for a more
sophisticated logic engine.


**Public Functions:**


- #### `def main()`


- #### `def parse_formula(s)`

  > A very basic parser for formulas.


- #### `def parse_sequent(s)`

  > A very basic parser for sequents.


- #### `def prove_sequent(sequent)`

  > A very simple proof search algorithm.
  > This is a placeholder for a more sophisticated prover.


### `/app/tooling/hierarchical_compiler.py`

A two-pass compiler for building hierarchical agent protocol documentation.

This script is the master engine for the "protocol as code" architecture. It
orchestrates the compilation of `AGENTS.md` and `README.md` files across a
nested directory structure and generates a unified, repository-wide knowledge
graph of all defined protocols.

The process works in two main passes:

**Pass 1: Hierarchical Documentation Build**
1.  **Discovery:** It recursively finds all directories named `protocols`,
    starting from the most deeply nested ones and working its way up to the root.
2.  **Child-First Compilation:** For each `protocols` directory, it invokes the
    `protocol_compiler.py` and `readme_generator.py` scripts to build the
    `AGENTS.md` and `README.md` for that specific module.
3.  **Summary Injection:** After a child module is built, the script extracts the
    full, rendered text of its protocols from its `AGENTS.md`. It then injects
    this text into a temporary file within the parent's `protocols` directory.
4.  **Parent Compilation:** The parent module is then compiled. Its `AGENTS.md`
    now seamlessly includes the complete, unabridged protocols of all its
    children, creating a single, comprehensive `AGENTS.md` at each level of the
    hierarchy.

**Pass 2: Centralized Knowledge Graph Compilation**
1.  **Discovery:** The script finds every `*.protocol.json` file in the entire
    repository.
2.  **Validation & Aggregation:** It validates each file against the master
    `protocol.schema.json`.
3.  **RDF Generation:** It uses `rdflib` to parse all validated JSON-LD protocol
    definitions into a single RDF graph.
4.  **Serialization:** The final, unified graph is serialized to
    `knowledge_core/protocols.ttl`, creating a machine-queryable single source
    of truth for all agent protocols in the repository.


**Public Functions:**


- #### `def cleanup_summaries(directory)`

  > Removes temporary summary files from a protocols directory.


- #### `def compile_centralized_knowledge_graph()`

  > Finds all protocol.json files in the entire repository, loads them, and
  > compiles them into a single, unified knowledge graph.


- #### `def find_protocol_dirs(root_dir)`

  > Finds all directories named 'protocols' within the root directory,
  > ignoring any special-cased directories.


- #### `def generate_summary(child_agents_md_path)`

  > Extracts the full, rendered protocol blocks from a child AGENTS.md file.
  > This function finds all protocol definitions (human-readable markdown and
  > the associated machine-readable JSON block) and concatenates them into a
  > single string to be injected into the parent AGENTS.md.


- #### `def get_parent_module(module_path, all_module_paths)`

  > Finds the direct parent module of a given module.


- #### `def main()`

  > Main function to orchestrate the hierarchical compilation.


- #### `def run_compiler(source_dir)`

  > Invokes the protocol_compiler.py script as a library.


- #### `def run_readme_generator(source_agents_md)`

  > Invokes the readme_generator.py script as a library.


### `/app/tooling/knowledge_compiler.py`

Extracts structured lessons from post-mortem reports and compiles them into a
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


**Public Functions:**


- #### `def extract_lessons_from_postmortem(postmortem_content)`

  > Parses a post-mortem report to extract lessons learned.
  > Handles multiple possible section headers and formats.


- #### `def extract_metadata_from_postmortem(postmortem_content)`

  > Parses a post-mortem report to extract metadata like Task ID and Date.


- #### `def format_lesson_entry(metadata, lesson_data)`

  > Formats an extracted lesson into a structured JSON object.


- #### `def main()`


- #### `def parse_action_to_command(action_text)`

  > Parses a natural language action string into a machine-executable command.
  >
  > This is the core of translating insights into automated actions. It uses
  > pattern matching to identify specific, supported commands.


### `/app/tooling/knowledge_integrator.py`

Enriches the local knowledge graph with data from external sources like DBPedia.

This script loads the RDF graph generated from the project's protocols,
identifies key concepts (like tools and rules), queries the DBPedia SPARQL
endpoint to find related information, and merges the external data into a new,
enriched knowledge graph.


**Public Functions:**


- #### `def extract_concepts(graph)`

  > Extracts key concepts (e.g., tools) from the local graph to query externally.
  > This version dynamically extracts tool names from the graph.


- #### `def load_local_graph(graph_file)`

  > Loads the local RDF graph from a file.


- #### `def query_dbpedia(concept)`

  > Queries DBPedia for a given concept and returns a graph of results.


- #### `def run_knowledge_integration(input_graph_path, output_graph_path)`

  > The main library function to run the knowledge integration process.
  > It loads a graph, extracts concepts, queries DBPedia, and saves the
  > enriched graph.


### `/app/tooling/log_failure.py`

A special-purpose script to log a pre-defined catastrophic failure event.

This is not a general-purpose tool. Its sole function is to create a very
specific log entry in `logs/activity.log.jsonl` that represents a
catastrophic, unrecoverable system failure.

The logged event is hard-coded to represent a critical protocol violation: the
unauthorized use of the `reset_all` tool, which is documented as a cause of
past workflow collapses.

This script is likely used for:
1.  Testing the logging and auditing systems' ability to handle critical failure
    events.
2.  Seeding the log with a known failure event for post-mortem analysis drills.
3.  Providing a programmatic way to signal a system-wide halt in a controlled
    manner during simulations.


**Public Functions:**


- #### `def log_catastrophic_failure()`

  > Logs the catastrophic failure event.


### `/app/tooling/master_control.py`

The master orchestrator for the agent's lifecycle, implementing the Context-Free Development Cycle (CFDC).

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


**Public Classes:**


- #### `class MasterControlGraph`

  > A Finite State Machine (FSM) that enforces the agent's protocol.
  > This graph reads a state definition and orchestrates the agent's workflow,
  > ensuring that all protocol steps are followed in the correct order.


  **Methods:**

  - ##### `def __init__(self, fsm_path='tooling/fsm.json')`

  - ##### `def do_awaiting_result(self, agent_state, logger)`

    > Checks for the result of the background research process.

  - ##### `def do_debugging(self, agent_state, logger)`

    > Handles the debugging state.

  - ##### `def do_execution(self, agent_state, step_result, logger)`

    > Processes the result of a step and advances the execution state.

  - ##### `def do_finalizing(self, agent_state, analysis_content, logger)`

    > Handles the finalization of the task with agent-provided analysis.

  - ##### `def do_generating_code(self, agent_state, logger)`

    > Handles the code generation state.

  - ##### `def do_orientation(self, agent_state, logger)`

    > Executes orientation, including analyzing the last post-mortem.

  - ##### `def do_planning(self, agent_state, plan_content, logger)`

    > Validates a given plan, parses it, and initializes the plan stack.

  - ##### `def do_researching(self, agent_state, logger)`

    > Launches the background research process.

  - ##### `def do_running_tests(self, agent_state, logger)`

    > Handles the test execution state.

  - ##### `def get_current_step(self, agent_state)`

    > Returns the current command to be executed by the agent, or None if execution is complete.

  - ##### `def get_trigger(self, source_state, dest_state)`

    > Finds a trigger in the FSM definition for a transition from a source
    > to a destination state. This is a helper to avoid hardcoding trigger
    > strings in the state handlers.


### `/app/tooling/master_control_cli.py`

The official command-line interface for the agent's master control loop.

This script is now a lightweight wrapper that passes control to the new,
API-driven `agent_shell.py`. It preserves the command-line interface while
decoupling the entry point from the FSM implementation.


**Public Functions:**


- #### `def main()`

  > The main entry point for the agent.
  >
  > This script parses the task description and invokes the agent shell.


### `/app/tooling/message_user.py`

A simple, local simulation of the `message_user` tool.

In a real agent execution environment, the `message_user` tool would be a
special function provided by the environment to communicate with the end-user.
This script provides a lightweight, standalone equivalent for local testing
and development.

Its sole purpose is to take a string as a command-line argument and print it
to standard output, prefixed with "[Message User]:". This allows developers to
test plans and scripts that involve user communication without needing the full
agent framework.


**Public Functions:**


- #### `def main()`


### `/app/tooling/pages_generator.py`

Generates a single HTML file for GitHub Pages from the repository's metalanguage.

This script combines the human-readable `README.md` and the machine-readable
`AGENTS.md` into a single, navigable HTML document. It uses the `markdown`
library to convert the Markdown content to HTML and to automatically generate
a Table of Contents.

The final output is a semantic HTML5 document, `index.html`, which serves as
the main page for the project's GitHub Pages site.


**Public Functions:**


- #### `def generate_html_page()`

  > Reads the source Markdown files, converts them to HTML, and builds the
  > final index.html page.


### `/app/tooling/plan_manager.py`

Provides a command-line interface for managing the agent's Plan Registry.

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


**Public Functions:**


- #### `def deregister_plan(name)`

  > Removes a plan from the registry by its logical name.


- #### `def get_registry()`

  > Loads the plan registry from its JSON file.


- #### `def list_plans()`

  > Lists all currently registered plans.


- #### `def main()`

  > Main function to run the plan management CLI.


- #### `def register_plan(name, path)`

  > Registers a new plan by mapping a logical name to a file path.


- #### `def save_registry(registry_data)`

  > Saves the given data to the plan registry JSON file.


### `/app/tooling/plan_parser.py`

Parses a plan file into a structured list of commands.

This module provides the `parse_plan` function and the `Command` dataclass,
which are central to the agent's ability to understand and execute plans.
The parser correctly handles multi-line arguments and ignores comments,
allowing for robust and readable plan files.


**Public Functions:**


- #### `def parse_plan(plan_content)`

  > Parses the raw text of a plan into a list of Command objects.
  > This parser correctly handles multi-line arguments, comments, and the '---' separator.



**Public Classes:**


- #### `class Command`

  > Represents a single, parsed command from a plan.
  > This structure correctly handles multi-line arguments for tools.


### `/app/tooling/plan_registry_auditor.py`

A command-line tool to audit the Plan Registry for broken links.

This script is the reference implementation for the `plan-registry-audit-001`
protocol. Its purpose is to ensure the integrity of the hierarchical planning
system by verifying the `knowledge_core/plan_registry.json` file.

The Plan Registry maps logical, human-readable names to the file paths of
reusable plans. This auditor reads the registry and checks every entry to
confirm that the specified file path points to an actual, existing file.

It prints a report to the console, listing all valid entries and flagging any
"dead links" where the target file is missing. This allows for quick diagnosis
and correction of the plan library, preventing runtime errors when the agent
tries to execute a plan that no longer exists.


**Public Functions:**


- #### `def audit_plan_registry(registry_path=DEFAULT_PLAN_REGISTRY_PATH)`

  > Audits the plan registry to find registered plans that point to
  > non-existent files.
  >
  > Args:
  >     registry_path (str): The path to the plan registry JSON file.
  >
  > Returns:
  >     list: A list of tuples, where each tuple contains the name and
  >           path of a dead link.


### `/app/tooling/protocol_auditor.py`

Audits the agent's behavior against its governing protocols and generates a report.

This script performs a comprehensive analysis to ensure the agent's actions,
as recorded in the activity log, align with the defined protocols in AGENTS.md.
It serves as a critical feedback mechanism for maintaining operational integrity.
The final output is a detailed `audit_report.md` file.

The auditor performs three main checks:
1.  **`AGENTS.md` Source Check:** Verifies if the `AGENTS.md` build artifact is
    potentially stale by comparing its modification time against the source
    protocol files in the `protocols/` directory.
2.  **Protocol Completeness:** It cross-references the tools used in the log
    (`logs/activity.log.jsonl`) against the tools defined in `AGENTS.md` to find:
    - Tools used but not associated with any formal protocol.
    - Tools defined in protocols but never used in the log.
3.  **Tool Centrality:** It conducts a frequency analysis of tool usage to
    identify which tools are most critical to the agent's workflow.

The script parses all embedded JSON protocol blocks within `AGENTS.md` and reads
from the standard `logs/activity.log.jsonl` log file, providing a reliable and
accurate audit.


**Public Functions:**


- #### `def find_all_agents_md_files(root_dir)`

  > Finds all AGENTS.md files in the repository, ignoring any special-cased
  > directories that are not part of the standard hierarchical build.


- #### `def generate_markdown_report(source_checks, unreferenced, unused, centrality)`

  > Generates a Markdown-formatted string from the audit results.


- #### `def get_protocol_tools_from_agents_md(agents_md_paths)`

  > Parses a list of AGENTS.md files to get a set of all tools associated
  > with protocols.


- #### `def get_used_tools_from_log(log_path)`

  > Parses the JSONL log file to get a list of used tool names.
  > It specifically looks for 'TOOL_EXEC' actions and extracts the tool
  > from the 'command' field based on the logging schema.
  > This version is robust against malformed lines with multiple JSON objects.


- #### `def main()`

  > Main function to run the protocol auditor and generate a report.


- #### `def run_centrality_analysis(used_tools)`

  > Performs a frequency analysis on the tool log and returns the counts.


- #### `def run_completeness_check(used_tools, protocol_tools)`

  > Compares used tools with protocol-defined tools and returns the gaps.


- #### `def run_protocol_source_check(all_agents_files)`

  > Checks if each AGENTS.md file is older than its corresponding source files.
  > Returns a list of warning/error dictionaries.


### `/app/tooling/protocol_compiler.py`

Compiles source protocol files into unified, human-readable and machine-readable artifacts.

This script is the engine behind the "protocol as code" principle. It discovers,
validates, and assembles protocol definitions from a source directory (e.g., `protocols/`)
into high-level documents like `AGENTS.md`.

Key Functions:
- **Discovery:** Scans a directory for source files, including `.protocol.json`
  (machine-readable rules) and `.protocol.md` (human-readable context).
- **Validation:** Uses a JSON schema (`protocol.schema.json`) to validate every
  `.protocol.json` file, ensuring all protocol definitions are syntactically
  correct and adhere to the established structure.
- **Compilation:** Combines the human-readable markdown and the machine-readable
  JSON into a single, cohesive Markdown file, embedding the JSON in code blocks.
- **Documentation Injection:** Can inject other generated documents, like the
  `SYSTEM_DOCUMENTATION.md`, into the final output at specified locations.
- **Knowledge Graph Generation:** Optionally, it can process the validated JSON
  protocols and serialize them into an RDF knowledge graph (in Turtle format),
  creating a machine-queryable version of the agent's governing rules.

This process ensures that `AGENTS.md` and other protocol documents are not edited
manually but are instead generated from a validated, single source of truth,
making the agent's protocols robust, verifiable, and maintainable.


**Public Functions:**


- #### `def compile_protocols(source_dir, target_file, schema_file, knowledge_graph_file=None, autodoc_file=None)`

  > Reads all .protocol.json and corresponding .protocol.md files from the
  > source directory, validates them, and compiles them into a target markdown file.
  > Optionally, it can also generate a machine-readable knowledge graph.


- #### `def install_dependencies()`

  > Checks for required packages from requirements.txt and installs them if missing.


- #### `def load_schema(schema_file)`

  > Loads the protocol JSON schema.


- #### `def main_cli()`

  > Main function to run the compiler from the command line.


- #### `def sanitize_markdown(content)`

  > Sanitizes markdown content to remove potentially malicious instructions.
  > This function removes script tags and other potentially malicious HTML/JS.


### `/app/tooling/protocol_updater.py`

A command-line tool for programmatically updating protocol source files.

This script provides the mechanism for the agent to perform self-correction
by modifying its own governing protocols based on structured, actionable
lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)
workflow.

The tool operates on the .protocol.json files located in the `protocols/`
directory, performing targeted updates based on command-line arguments.


**Public Functions:**


- #### `def add_tool_to_protocol(protocol_id, tool_name, protocols_dir)`

  > Adds a tool to the 'associated_tools' list of a specified protocol.


- #### `def find_protocol_file(protocol_id, protocols_dir)`

  > Finds the protocol file path corresponding to a given protocol_id.


- #### `def main()`

  > Main function to parse arguments and call the appropriate handler.


- #### `def update_rule_in_protocol(protocol_id, rule_id, new_description, protocols_dir)`

  > Updates the description of a specific rule within a protocol.


### `/app/tooling/readme_generator.py`

A documentation generator that creates a module's README.md file.

This script is a key component of the "documentation as code" pipeline. It
automates the creation of a `README.md` file by dynamically combining content
from both machine-readable protocols and Python source code docstrings.

The generation process is as follows:
1.  **Parse `AGENTS.md`:** It reads the module's `AGENTS.md` file and extracts
    the `protocol_id` and `description` from every JSON protocol block to create
    a summary of the module's core protocols.
2.  **Parse Source Code:** It scans the module's `tooling/` subdirectory for all
    Python (`.py`) files. For each file, it parses the Abstract Syntax Tree (AST)
    to extract the module-level docstring.
3.  **Inject into Template:** It takes the generated protocol summaries and the
    extracted docstrings and injects them into a static Markdown template.
4.  **Write `README.md`:** The final, combined content is written to the
    `README.md` file in the same directory.

This ensures that the high-level `README.md` documentation always stays
synchronized with the ground-truth definitions in the `AGENTS.md` protocols and
the inline documentation within the tools themselves.


**Public Functions:**


- #### `def generate_core_protocols_section(agents_md_path)`

  > Parses a given AGENTS.md file to extract protocol definitions and generate a Markdown summary.


- #### `def generate_key_components_section(module_path)`

  > Generates the Markdown for the "Key Components" section by documenting
  > any `.py` files found in a `tooling/` subdirectory of the module.


- #### `def get_module_docstring(filepath)`

  > Parses a Python file and extracts the module-level docstring.


- #### `def main(source_file, output_file)`

  > Main function to generate the README.md content and write it to a file.


### `/app/tooling/refactor.py`

A command-line tool for automated, plan-based code refactoring.

This script provides a safe and repeatable way to perform common refactoring
tasks, such as renaming a symbol, across the entire codebase. It is the
reference implementation for the `refactor-001` protocol.

The tool operates by generating a detailed, executable plan file that the
agent's master controller can then execute. This decouples the analysis of the
refactoring from its execution.

Workflow for renaming a symbol:
1.  **AST-based Definition Finding:** It first parses the source file using
    Python's Abstract Syntax Tree (AST) to reliably locate the precise
    definition of the target function or class. This avoids the ambiguity of
    simple text searches.
2.  **Reference Searching:** It then searches the entire repository to find all
    files that contain the old symbol name, creating a list of potential
    references.
3.  **Plan Generation:** For each file that contains the old name, it generates a
    `replace_with_git_merge_diff` command. This command is a highly-specific
    search-and-replace that will substitute the old name for the new one.
4.  **Plan Output:** All generated commands are written to a single `.plan.txt`
    file. The script outputs the path to this file, which can then be passed to
    the agent's execution engine.


**Public Functions:**


- #### `def find_references(symbol_name, search_path)`

  > Finds all files in a directory that reference a given symbol.


- #### `def find_symbol_definition(filepath, symbol_name)`

  > Finds the definition of a symbol in a Python file.


- #### `def main()`


### `/app/tooling/reorientation_manager.py`

Re-orientation Manager

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


**Public Functions:**


- #### `def check_for_deep_research_trigger(new_concepts)`

  > Checks if any of the new concepts should trigger a deep research cycle.


- #### `def main()`


- #### `def parse_concepts_from_agents_md(content)`

  > Parses an AGENTS.md file to extract a set of key concepts.
  > This version uses a simple regex to find protocol IDs and tool names.


- #### `def run_temporal_orientation(concept)`

  > Runs the temporal_orienter.py tool for a given concept.


- #### `def update_temporal_orientations(new_orientations)`

  > Updates the temporal orientations knowledge base.


### `/app/tooling/research.py`

This module contains the logic for executing research tasks based on a set of
constraints. It acts as a dispatcher, calling the appropriate tool (e.g.,
read_file, google_search) based on the specified target and scope.


**Public Functions:**


- #### `def execute_research_protocol(constraints)`

  > Executes a research task based on a provided constraints dictionary.
  >
  > Args:
  >     constraints (dict): A dictionary specifying the research target,
  >                         scope, and other parameters.
  >
  > Returns:
  >     str: The result of the research action, or an error message.


### `/app/tooling/research_planner.py`

This module is responsible for generating a formal, FSM-compliant research plan
for a given topic. The output is a string that can be executed by the agent's
master controller.


**Public Functions:**


- #### `def plan_deep_research(topic)`

  > Generates a multi-step, FSM-compliant plan for conducting deep research.
  >
  > Args:
  >     topic (str): The research topic.
  >
  > Returns:
  >     str: A string containing the executable plan.


### `/app/tooling/self_correction_orchestrator.py`

Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.

This script is the engine of the automated feedback loop. It reads structured,
actionable lessons from `knowledge_core/lessons.jsonl` and uses the
`protocol_updater.py` tool to apply them to the source protocol files.


**Public Functions:**


- #### `def load_lessons()`

  > Loads all lessons from the JSONL file.


- #### `def main()`

  > Main function to run the self-correction workflow.


- #### `def process_lessons(lessons, protocols_dir)`

  > Processes all pending lessons, applies them, and updates their status.
  > Returns True if any changes were made, False otherwise.


- #### `def run_command(command)`

  > Runs a command and returns True on success, False on failure.


- #### `def save_lessons(lessons)`

  > Saves a list of lessons back to the JSONL file, overwriting it.


### `/app/tooling/self_improvement_cli.py`

Analyzes agent activity logs to identify opportunities for self-improvement.

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


**Public Functions:**


- #### `def analyze_planning_efficiency(log_file)`

  > Analyzes the log file to find tasks with multiple plan revisions.
  >
  > Args:
  >     log_file (str): Path to the activity log file.
  >
  > Returns:
  >     dict: A dictionary mapping task IDs to the number of plan updates.


- #### `def analyze_protocol_violations(log_file)`

  > Scans the log file for critical protocol violations, such as the
  > unauthorized use of `reset_all`.
  >
  > This function checks for two conditions:
  > 1. A `SYSTEM_FAILURE` log explicitly blaming `reset_all`.
  > 2. A `TOOL_EXEC` log where the command contains "reset_all".
  >
  > Args:
  >     log_file (str): Path to the activity log file.
  >
  > Returns:
  >     list: A list of unique task IDs where `reset_all` was used.


- #### `def main()`

  > Main function to run the self-improvement analysis CLI.


### `/app/tooling/standard_agents_compiler.py`

A compiler that generates a simplified, standard-compliant `AGENTS.md` file.

This script acts as an "adapter" to make the repository more accessible to
third-party AI agents that expect a conventional set of instructions. While the
repository's primary `AGENTS.md` is a complex, hierarchical, and
machine-readable artifact for its own specialized agent, the `AGENTS.standard.md`
file produced by this script offers a simple, human-readable summary of the
most common development commands.

The script works by:
1.  **Parsing the Makefile:** It dynamically parses the project's `Makefile`,
    which is the single source of truth for high-level commands. It specifically
    extracts the exact commands for common targets like `install`, `test`,
    `lint`, and `format`. This ensures the generated instructions are never
    stale.
2.  **Injecting into a Template:** It injects these extracted commands into a
    pre-defined, user-friendly Markdown template.
3.  **Generating the Artifact:** The final output is written to
    `AGENTS.standard.md`, providing a simple, stable, and conventional entry
    point for external tools, effectively bridging the gap between the complex
    internal protocol system and the broader agent ecosystem.


**Public Functions:**


- #### `def main()`

  > Generates a standard-compliant AGENTS.md file by parsing commands
  > from the project's Makefile.


- #### `def parse_makefile_command(target_name, makefile_content)`

  > Parses a Makefile to find the main command for a specific target,
  > skipping any 'echo' lines. This version iterates through lines for robustness.


### `/app/tooling/state.py`

Defines the core data structures for managing the agent's state.

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


**Public Classes:**


- #### `class AgentState`

  > Represents the complete, serializable state of the agent's workflow.
  >
  > This dataclass acts as a central container for all information related to the
  > agent's current task. It is designed to be passed between the different states
  > of the `MasterControlGraph` FSM, ensuring that context is maintained
  > throughout the lifecycle of a task.
  >
  > Attributes:
  >     task: A string describing the overall objective.
  >     plan_path: The file path to the root plan for the current task.
  >     plan_stack: A list of `PlanContext` objects, forming the execution
  >         stack for the CFDC. The plan at the top of the stack is the one
  >         currently being executed.
  >     messages: A history of messages, typically for interaction with an LLM.
  >     orientation_complete: A flag indicating if the initial orientation
  >         phase has been successfully completed.
  >     vm_capability_report: A string summarizing the results of the
  >         environmental probe.
  >     research_findings: A dictionary to store the results of research tasks.
  >     draft_postmortem_path: The file path to the draft post-mortem report
  >         generated during the AWAITING_ANALYSIS state.
  >     final_report: A string containing a summary of the final, completed
  >         post-mortem report.
  >     error: An optional string that holds an error message if the FSM
  >         enters an error state, providing a clear reason for the failure.


  **Methods:**

  - ##### `def to_json(self)`


- #### `class PlanContext`

  > Represents the execution context of a single plan file within the plan stack.
  >
  > This class holds the state of a specific plan being executed, including its
  > file path, its content (as a list of parsed Command objects), and a pointer
  > to the current step being executed.


### `/app/tooling/symbol_map_generator.py`

Generates a code symbol map for the repository to aid in contextual understanding.

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


**Public Functions:**


- #### `def generate_symbols_with_ast(root_dir='.')`

  > Fallback to generate a symbol map for Python files using the AST module.


- #### `def generate_symbols_with_ctags(root_dir='.')`

  > Generates a symbol map using Universal Ctags.


- #### `def has_ctags()`

  > Check if Universal Ctags is installed and available in the PATH.


- #### `def main()`

  > Main function to generate and save the symbol map.
