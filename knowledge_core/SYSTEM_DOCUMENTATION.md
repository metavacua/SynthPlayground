# System Documentation

---

## `/app/tooling/` Directory

### `/app/tooling/__init__.py`

This package contains various tools for the agent's operation.

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

_No module-level docstring found._


**Public Functions:**


- #### `def main()`

  > Parses and executes an Aura script.


### `/app/tooling/background_researcher.py`

This script performs a simulated research task in the background.
It takes a task ID as a command-line argument and writes its findings
to a temporary file that the main agent can poll.


**Public Functions:**


- #### `def perform_research(task_id)`

  > Simulates a research task and writes the result to a file.


### `/app/tooling/builder.py`

This script provides a unified, configuration-driven build system for the project.

It reads a central `build_config.json` file to determine which compilers or
generators to run for different build targets (like 'docs', 'agents', etc.).
This allows for a flexible and easily extensible build process without modifying
the build script itself. New targets can be added simply by updating the JSON
configuration.

The script supports building individual targets, listing all available targets,
and building all targets in a predefined, logical order. It captures and
displays the output of each build step, providing clear success or failure
reporting.


**Public Functions:**


- #### `def execute_build(target_name, config)`

  > Executes the build process for a specific target defined in the config.


- #### `def load_config()`

  > Loads the build configuration file.


- #### `def main()`

  > Main function to parse arguments and drive the build process.


### `/app/tooling/code_health_analyzer.py`

This script provides tools for analyzing and maintaining the health of the codebase.

Currently, its primary function is to act as a "dead link checker" for the
agent's Plan Registry (`knowledge_core/plan_registry.json`). The Plan Registry
maps logical plan names to file paths. This script verifies that every file
path in the registry points to an existing file.

If it discovers any "dead links" (entries pointing to non-existent files),
it can generate a corrective plan. This plan, when executed by the agent,
will programmatically remove the invalid entries from the registry, ensuring
the agent's plan library remains consistent and reliable.


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

This script provides tools for understanding the context of a specific code file.

It is designed to answer questions like:
- What functions and classes are defined in this file?
- What other modules or symbols does this file import?
- Where else in the codebase are the symbols from this file being used?

By parsing a Python file's Abstract Syntax Tree (AST), it can extract defined
symbols (functions and classes) and imported symbols. It can also perform a
repository-wide search to find references to the symbols defined in the target
file.

The output is a JSON report containing all this information, which gives the
agent a comprehensive "contextual awareness" of a single file, aiding in tasks
like refactoring, dependency analysis, and impact assessment.


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

_No module-level docstring found._


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

This script provides a utility for extracting text content from various document types.

It is designed to scan a directory tree and identify files with common document
extensions like `.pdf`, `.md`, and `.txt`. For each file found, it uses the
appropriate method to read its content:
- For PDFs, it uses the `pypdf` library to extract text from each page.
- For Markdown and plain text files, it reads the raw text content.

The script returns a dictionary where the keys are the file paths of the
scanned documents and the values are their extracted text content. This tool is
a key part of the agent's initial orientation, allowing it to gather context
from human-readable documentation within the repository.


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

_No module-level docstring found._


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

_No module-level docstring found._


**Public Functions:**


- #### `def main()`

  > Provides a command-line interface for the HDL prover tool.


- #### `def prove_sequent(sequent_string)`

  > Calls the HDL Lisp prover to determine if a sequent is provable.
  >
  > Args:
  >     sequent_string: A string representing the sequent in Lisp format,
  >                   e.g., "'(() (con))'".
  >
  > Returns:
  >     A boolean indicating whether the sequent is provable, or None on error.


### `/app/tooling/hierarchical_compiler.py`

This script orchestrates a hierarchical build process for the agent's protocols.

It enables a modular, "microkernel"-style architecture where different sub-modules
of the agent can define their own protocols independently. The script discovers
all `protocols` directories across the repository and builds them in a specific
order, from the most deeply nested to the top-level.

Key features:
- **Hierarchical Discovery:** Finds all `protocols` directories.
- **Bottom-Up Compilation:** Compiles child modules first, then "injects" their
  compiled `AGENTS.md` content as a summary into their parent's `AGENTS.md`.
  This creates a single, comprehensive `AGENTS.md` at the root that includes
  the protocols from all sub-modules.
- **Artifact Generation:** For each module, it runs the `protocol_compiler.py`
  to create `AGENTS.md` and the `readme_generator.py` to create `README.md`.
- **Centralized Knowledge Graph:** After processing all modules, it performs a
  final pass to discover all `.protocol.json` files and compiles them into a
  single, unified RDF knowledge graph (`protocols.ttl`), providing a complete,
  queryable view of the agent's entire protocol system.


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

This script provides a dedicated function for logging a specific, critical failure event.

Its purpose is to create a standardized log entry when a "catastrophic failure"
occurs, specifically the unauthorized use of the `reset_all` tool. This allows
the agent's monitoring and post-mortem systems to reliably track and identify
this particular high-severity error.

The script uses the centralized `Logger` utility to ensure the log entry
conforms to the project's structured logging schema.


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

This script provides a command-line tool to audit the agent's Plan Registry.

The Plan Registry (`knowledge_core/plan_registry.json`) is a critical file that
maps human-readable, logical plan names to the file paths of the actual plan
scripts. This allows the agent to call plans by name (e.g., `call_plan "deep-research"`)
without hardcoding file paths.

This auditor ensures the integrity of the registry by checking that every file
path listed in it actually exists. It identifies and reports any "dead links"
where a plan name points to a non-existent file, helping to maintain the
reliability of the agent's hierarchical planning system.


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

This script automatically generates a `README.md` file for a specific module.

It acts as a documentation aggregator, pulling information from two primary sources:
1.  **`AGENTS.md`:** It parses the JSON protocol blocks within a module's
    `AGENTS.md` file to create a human-readable summary of the core protocols
    governing that module.
2.  **Python Source Files:** It scans the `tooling/` subdirectory within the
    module for any Python scripts and extracts their module-level docstrings
    to document the key software components.

The script combines this extracted information with a static template to produce
a well-structured `README.md` file. This ensures that the documentation for each
module stays synchronized with its actual protocols and implementation, adhering
to the principle of "documentation as code."


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

This script provides a simple, automated refactoring tool for renaming symbols.

It is designed to be used from the command line to rename a Python function or
class and all of its references throughout the repository.

The process is as follows:
1.  **Find Definition:** It first locates the definition of the target symbol
    (the "old name") in the specified file.
2.  **Find References:** It then searches the entire repository for any files
    that mention the old name.
3.  **Generate Plan:** For each file where the name is found, it generates a
    `replace_with_git_merge_diff` command. This command encapsulates the change
    from the old content to the new content (with the name replaced).
4.  **Output Plan File:** It writes all these commands into a single, temporary
    plan file.

The path to this generated plan file is printed to standard output. The agent's
master controller can then be instructed to execute this plan, applying the
refactoring changes in a controlled and verifiable way.


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

This script generates a simplified, standard-compliant `AGENTS.md` file.

While the project's primary `AGENTS.md` is generated by a complex, hierarchical
system, many external AI agents and tools expect a simpler, more conventional
format. This script bridges that gap.

It parses the project's `Makefile` to extract the essential commands for common
tasks like installing dependencies, running tests, linting, and formatting code.
It then injects these discovered commands into a human-readable Markdown
template.

The output, `AGENTS.standard.md`, provides a straightforward, predictable
entry point for third-party agents, improving interoperability with the broader
AI development ecosystem.


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
