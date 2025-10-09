# System Documentation

---

## `tooling/` Directory

### `tooling/__init__.py`

_No module-level docstring found._

### `tooling/dependency_graph_generator.py`

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

### `tooling/doc_generator.py`

Generates system documentation from Python module-level docstrings.

This script scans specified directories for Python files, parses them to
extract their module-level docstrings, and compiles them into a single,
formatted Markdown file. It is the core engine for the project's automated
documentation generation, ensuring that the `SYSTEM_DOCUMENTATION.md` artifact
in the `knowledge_core` is always up-to-date with the in-code documentation.

The script is configured via top-level constants:
- `SCAN_DIRECTORIES`: A list of directories to search for .py files.
- `OUTPUT_FILE`: The path where the final Markdown file will be written.
- `DOC_TITLE`: The main title for the generated documentation file.

It uses Python's `ast` module to reliably parse source files without
importing them, which avoids issues with dependencies or script side-effects.

### `tooling/environmental_probe.py`

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

### `tooling/fdc_cli.py`

Provides the command-line interface for the Finite Development Cycle (FDC).

This script is a core component of the agent's protocol, offering tools to ensure
that all development work is structured, verifiable, and safe. It is used by both
the agent to signal progress and the `master_control.py` orchestrator to
validate the agent's plans before execution.

The CLI provides several key commands:
- `close`: Logs the formal end of a task, signaling to the orchestrator that
  execution is complete.
- `validate`: Performs a deep validation of a plan file against the FDC's Finite
  State Machine (FSM) definition. It checks for both syntactic correctness (Is
  the sequence of operations valid?) and semantic correctness (Does the plan try
  to use a file before creating it?).
- `analyze`: Reads a plan and provides a high-level analysis of its
  characteristics, such as its computational complexity and whether it is a
  read-only or read-write plan.
- `lint`: A comprehensive "linter" that runs a full suite of checks on a plan
  file, including `validate`, `analyze`, and checks for disallowed recursion.

### `tooling/knowledge_compiler.py`

Extracts structured lessons from post-mortem reports and compiles them into a
centralized, long-term knowledge base.

This script is a core component of the agent's self-improvement feedback loop.
After a task is completed, a post-mortem report is generated that includes a
section for "Corrective Actions & Lessons Learned." This script automates the
process of parsing that section to extract key insights.

It identifies pairs of "Lesson" and "Action" statements and transforms them
into a standardized, machine-readable format. These formatted entries are then
appended to the `knowledge_core/lessons_learned.md` file, which serves as the
agent's persistent memory of what has worked, what has failed, and what can be
improved in future tasks.

The script is executed via the command line, taking the path to a completed
post-mortem file as its primary argument.

### `tooling/master_control.py`

The master orchestrator for the agent's lifecycle, governed by a Finite State Machine.

This script, `master_control.py`, is the heart of the agent's operational loop.
It implements a strict, protocol-driven workflow defined in a JSON file
(typically `tooling/fsm.json`). The `MasterControlGraph` class reads this FSM
definition and steps through the prescribed states, ensuring that the agent
cannot deviate from the established protocol.

The key responsibilities of this orchestrator include:
- **State Enforcement:** Guiding the agent through the formal states of a task:
  ORIENTING, PLANNING, EXECUTING, AWAITING_ANALYSIS, POST_MORTEM, and finally
  AWAITING_SUBMISSION.
- **Plan Validation:** Before execution, it invokes the `fdc_cli.py` tool to
  formally validate the agent-generated `plan.txt`, preventing the execution of
  invalid or unsafe plans.
- **Hierarchical Execution (CFDC):** It manages the plan execution stack, which
  is the core mechanism of the Context-Free Development Cycle (CFDC). This
  allows plans to call other plans as sub-routines via the `call_plan`
  directive.
- **Recursion Safety:** It enforces a `MAX_RECURSION_DEPTH` on the plan stack to
  guarantee that the execution process is always decidable and will terminate.
- **Lifecycle Management:** It orchestrates the entire lifecycle, from initial
  orientation and environmental probing to the final post-mortem analysis and
  compilation of lessons learned.

The FSM operates by waiting for specific signals—typically the presence of
files like `plan.txt` or `step_complete.txt`—before transitioning to the next
state. This creates a robust, interactive loop where the orchestrator directs
the high-level state, and the agent is responsible for completing the work
required to advance that state.

### `tooling/plan_manager.py`

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

### `tooling/protocol_auditor.py`

Audits the agent's behavior against its governing protocols.

This script performs a comparative analysis between the tools defined in the
`AGENTS.md` protocol document and the tools actually used, as recorded in the
activity log. Its purpose is to provide a feedback loop for protocol enforcement
and to identify potential gaps or inconsistencies in the agent's behavior.

The auditor currently performs two main checks:
1.  **Protocol Completeness:** It identifies:
    - Tools that were used but are not associated with any formal protocol.
    - Tools that are defined in the protocols but were never used.
2.  **Tool Centrality:** It conducts a frequency analysis of the tools used,
    helping to identify which tools are most critical to the agent's workflow.

NOTE: The current implementation has known issues. It incorrectly parses the
`AGENTS.md` file by only reading the first JSON block and relies on a non-standard
log file. It requires modification to parse all JSON blocks and use the correct
`logs/activity.log.jsonl` file to be effective.

### `tooling/protocol_compiler.py`

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

### `tooling/protocol_updater.py`

A command-line tool for programmatically updating protocol source files.

This script provides the mechanism for the agent to perform self-correction
by modifying its own governing protocols based on structured, actionable
lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)
workflow.

The tool operates on the .protocol.json files located in the `protocols/`
directory, performing targeted updates based on command-line arguments.

### `tooling/research.py`

A unified, constraint-based interface for all research and data-gathering operations.

This script abstracts the various methods an agent might use to gather information
(reading local files, accessing the web, querying a database) into a single,
standardized function: `execute_research_protocol`. It is a core component of
the Advanced Orientation and Research Protocol (AORP), providing the mechanism
by which the agent fulfills the requirements of each orientation level (L1-L4).

The function operates on a `constraints` dictionary, which specifies the target,
scope, and other parameters of the research task. This design allows the calling
orchestrator (e.g., `master_control.py`) to request information without needing
to know the underlying implementation details of how that information is fetched.

The current implementation acts as a functional placeholder, simulating the
different research levels to provide a testable hook for the main FSM loop
without requiring live external services. It can simulate reading local files,
listing directories, and fetching content from external URLs.

### `tooling/research_planner.py`

Generates a structured, templated plan for conducting deep research tasks.

This script provides a standardized workflow for the agent when it needs to
perform in-depth research on a complex topic. The `plan_deep_research` function
creates a markdown document that outlines a multi-phase research process,
ensuring that the investigation is systematic and thorough.

The key features of the generated plan are:
- **Context-Awareness:** It can generate plans tailored to either the agent's
  internal repository context (using `AGENTS.md`) or an external one.
- **Structured Phases:** It breaks the research process down into four distinct
  phases:
    1.  Initial Planning & Question Formulation
    2.  Parallel Research Execution
    3.  Synthesis and Refinement
    4.  Final Report Generation
- **Tool Integration:** It explicitly references the `execute_research_protocol`
  tool, guiding the agent on how to perform the data-gathering steps.
- **Protocol Reference:** It includes a snippet of the governing protocol
  document directly in the plan, providing immediate context for the task.

This tool helps enforce a consistent and effective methodology for complex
investigative tasks, improving the quality and reliability of the research
findings.

### `tooling/self_correction_orchestrator.py`

Orchestrates the Protocol-Driven Self-Correction (PDSC) workflow.

This script is the engine of the automated feedback loop. It reads structured,
actionable lessons from `knowledge_core/lessons.jsonl` and uses the
`protocol_updater.py` tool to apply them to the source protocol files.

### `tooling/self_improvement_cli.py`

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

### `tooling/state.py`

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

### `tooling/symbol_map_generator.py`

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

### `tooling/test_dependency_graph_generator.py`

Unit tests for the dependency graph generator tool.

This test suite validates the functionality of the `dependency_graph_generator.py`
script. It uses a temporary file structure created in the `setUp` method to
simulate a repository with both JavaScript (`package.json`) and Python
(`requirements.txt`) projects, including nested and root-level files.

The tests cover:
- File discovery for both project types.
- Correct parsing of package names and dependencies from each file type.
- The successful generation of a complete dependency graph, including both
  internal and external dependencies and the correct creation of nodes and edges.

### `tooling/test_knowledge_compiler.py`

Unit tests for the knowledge_compiler.py script.

This test suite verifies that the knowledge compiler can correctly parse
a mock post-mortem report and generate a structured, machine-readable
lessons.jsonl file. It ensures that the generated lessons conform to the
expected JSON schema, including having unique IDs and a 'pending' status.

### `tooling/test_master_control.py`

Integration tests for the master control FSM and CFDC workflow.

This test suite provides end-to-end validation of the `master_control.py`
orchestrator. It uses a multi-threaded approach to simulate the interactive
nature of the agent's workflow, where the FSM runs in one thread and the test
script acts as the "agent" in the main thread, creating files like `plan.txt`
and `step_complete.txt` to drive the FSM through its states.

The suite is divided into two main classes:
- `TestMasterControlGraphFullWorkflow`: Validates the entire "atomic" workflow
  from orientation through planning, execution, analysis, and post-mortem,
  ensuring the FSM transitions correctly through all its states.
- `TestCFDCWorkflow`: Focuses specifically on the Context-Free Development
  Cycle features, including:
    - Executing hierarchical plans using the `call_plan` directive.
    - Using the Plan Registry to call sub-plans by a logical name.
    - Verifying that the system correctly halts when the maximum recursion
      depth is exceeded, ensuring decidability.

### `tooling/test_protocol_auditor.py`

_No module-level docstring found._

### `tooling/test_protocol_updater.py`

Unit tests for the protocol_updater.py script.

This test suite verifies that the protocol updater tool can correctly
find and modify protocol source files in a controlled, temporary
environment. It ensures that tools can be added to protocols and that
edge cases like duplicate additions are handled gracefully.

### `tooling/test_self_correction_orchestrator.py`

Unit tests for the self_correction_orchestrator.py script.

This test suite verifies the end-to-end functionality of the automated
self-correction workflow. It ensures that the orchestrator can correctly
read structured lessons, invoke the protocol_updater.py script as a
subprocess with the correct arguments, and update the lesson status file
to reflect the outcome.

### `tooling/test_self_improvement_cli.py`

Unit tests for the self-improvement analysis CLI tool.

This test suite validates the `analyze_planning_efficiency` function from the
`self_improvement_cli.py` script. The primary goal is to ensure that the tool
can correctly parse an activity log and identify tasks that involved multiple
plan revisions, which is a key indicator of potential inefficiency.

The test creates a temporary log file (`.jsonl`) containing a mix of scenarios:
- A task with a single, efficient planning step.
- A task with three separate plan revisions.
- A task that uses an alternative but valid log format for plan updates.
- A task with no planning actions at all.

The test asserts that the analysis correctly identifies only the inefficient
tasks and accurately counts the number of plan revisions for each, ensuring the
tool provides reliable feedback for the agent's self-improvement loop.

### `tooling/test_symbol_map_generator.py`

Unit tests for the symbol map generator tool.

This test suite validates the `symbol_map_generator.py` script, which is
responsible for creating a code symbol index for the repository. The tests
cover both of the script's operational modes: the preferred `ctags`-based
generation and the `ast`-based fallback.

The tests include:
- `test_generate_with_ctags_success`: Mocks the `subprocess.run` call to
  simulate a successful `ctags` execution. It verifies that the script correctly
  parses the JSON-lines output from `ctags` and wraps it in a valid JSON object.
- `test_generate_with_ast_fallback`: Validates that the Python-only `ast` parser
  correctly traverses a sample Python file and extracts class, method, and
  function definitions.
- `test_main_with_ast_fallback`: Mocks the `has_ctags` check to force the main
  function to use the `ast` fallback, ensuring the end-to-end logic works
  correctly when `ctags` is not available.

---

## `utils/` Directory

### `utils/__init__.py`

_No module-level docstring found._

### `utils/logger.py`

Provides a standardized, schema-validated logger for producing structured JSONL logs.

This module contains the `Logger` class, which is responsible for creating all
entries in the `logs/activity.log.jsonl` file. This is a critical component for
maintaining an auditable, machine-readable record of the agent's actions.

The logger enforces a strict structure on all log entries by validating them
against a formal JSON schema, which is extracted from the `LOGGING_SCHEMA.md`
document. This ensures that every log entry, regardless of its source, is
consistent and contains the required fields.

Key features of the `Logger` class:
- **Schema Validation:** Each log entry is validated against the official
  project schema before being written to disk, preventing data corruption.
- **Structured Data:** Logs are written in JSONL format, where each line is a
  valid JSON object, making them easy to parse and query.
- **Session Management:** It automatically assigns a unique `session_id` to
  all logs generated during its lifecycle, allowing actions to be traced back
  to a specific run.
- **Automatic Timestamps:** It injects a UTC timestamp into every log entry,
  providing a precise timeline of events.

This centralized logger is the sole mechanism by which the agent should record
its activities, ensuring a single source of truth for all post-mortem analysis
and self-improvement activities.

### `utils/test_logger.py`

Unit tests for the structured JSONL logger.

This test suite validates the `Logger` class from `utils/logger.py`. Its main
purpose is to ensure that the logger correctly performs schema validation and
writes well-formed log entries to the specified log file.

The tests use a temporary directory to house a mock schema file and a log file,
ensuring the tests are isolated and do not interfere with the actual project logs.

The suite covers two primary scenarios:
- **Success Case:** It tests that a log entry with a valid data structure that
  conforms to the schema is successfully written to the JSONL file.
- **Failure Case:** It tests that a log entry with data that violates the schema
  (e.g., incorrect data types) correctly raises a `ValidationError` from the
  `jsonschema` library and that no log file is written, preventing the creation
  of corrupted logs.