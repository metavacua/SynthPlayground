# System Documentation

This document provides a comprehensive overview of the scripts located in the `tooling/` and `utils/` directories. The purpose of this documentation is to build a detailed knowledge base that explains the functionality and usage of each component, facilitating better understanding and maintenance of the system.

---

## `tooling/` Directory

### `tooling/dependency_graph_generator.py`

**Purpose:**
This script is responsible for creating a dependency graph of the entire repository. It scans for common dependency management files (`package.json` for JavaScript/TypeScript and `requirements.txt` for Python), parses them, and builds a graph that represents the relationships between different projects and their external libraries.

**Key Functions:**
- `find_package_json_files(root_dir)`: Recursively searches the repository for `package.json` files, excluding `node_modules` directories.
- `find_requirements_txt_files(root_dir)`: Recursively searches the repository for `requirements.txt` files.
- `parse_package_json(package_json_path)`: Reads a `package.json` file and extracts its name, dependencies, and devDependencies.
- `parse_requirements_txt(requirements_path, root_dir)`: Reads a `requirements.txt` file and extracts its dependencies, handling version specifiers and comments.
- `generate_dependency_graph(root_dir)`: Orchestrates the entire process. It calls the finder and parser functions, then constructs a graph structure containing nodes (projects and libraries) and edges (dependencies).
- `main()`: The entry point of the script. It calls `generate_dependency_graph()` and saves the resulting graph as `knowledge_core/dependency_graph.json`.

**Usage:**
This script is intended to be run from the root of the repository:
```bash
python3 tooling/dependency_graph_generator.py
```
The output is a JSON file (`knowledge_core/dependency_graph.json`) that can be used by other tools to understand the repository's architecture and potential impact of changes.

### `tooling/environmental_probe.py`

**Purpose:**
This script serves as a diagnostic tool to assess the capabilities of the agent's execution environment. It runs a series of tests to verify core functionalities like filesystem access, network connectivity, and the presence of environment variables. The results are used to generate a "VM Capability Report" that helps the agent understand its operational constraints.

**Key Functions:**
- `probe_filesystem()`: Performs a write, read, and delete operation with a temporary file to test filesystem integrity and measures the latency of these operations.
- `probe_network()`: Sends a lightweight `HEAD` request to a reliable external endpoint (`google.com`) to check for internet access and measures the connection latency.
- `probe_environment_variables()`: Checks for the existence of the `PATH` environment variable to ensure a sane execution environment.
- `main()`: The entry point of the script. It calls all the `probe_*` functions and prints a formatted summary report to standard output.

**Usage:**
This script is executed directly to generate a report on the current environment's capabilities.
```bash
python3 tooling/environmental_probe.py
```

### `tooling/fdc_cli.py`

**Purpose:**
This script provides the command-line interface for the **Finite Development Cycle (FDC)**. It is a core component of the agent's protocol, offering tools to ensure that all development work is structured, verifiable, and safe. It is used by both the agent to signal progress and the `master_control.py` orchestrator to validate the agent's plans before execution.

**Key Functions & Commands:**

The script uses `argparse` to provide several subcommands:

1.  **`close`**:
    - **Function:** `close_task(task_id)`
    - **Purpose:** This command's primary role is to log a `TASK_END` event in the activity log. It signals that the agent has completed its work on a given task. The responsibility for creating the post-mortem report is handled by the higher-level `master_control.py` orchestrator.
    - **Usage:** `python3 tooling/fdc_cli.py close --task-id <your-task-id>`

2.  **`validate`**:
    - **Function:** `validate_plan(plan_filepath)`
    - **Purpose:** This is a powerful validator that checks if a given plan file is valid according to the FSM definition in `tooling/fdc_fsm.json`. It performs two types of checks:
        - **Syntactic Validation:** Ensures that the sequence of actions in the plan is a valid string in the language defined by the FSM.
        - **Semantic Validation:** Simulates the plan's execution to catch errors like trying to read a file before it's created or creating a file that already exists.
    - **Usage:** `python3 tooling/fdc_cli.py validate <path/to/plan.txt>`

3.  **`analyze`**:
    - **Function:** `analyze_plan(plan_filepath)`
    - **Purpose:** Reads a plan and provides a high-level analysis of its characteristics, including:
        - **Complexity:** Determines if the plan is Constant, Polynomial, or Exponential time based on its loop structure.
        - **Modality:** Classifies the plan as "Analysis (Read-Only)" or "Construction (Read-Write)" based on the tools it uses.
    - **Usage:** `python3 tooling/fdc_cli.py analyze <path/to/plan.txt>`

4.  **`lint`**:
    - **Function:** `lint_plan(plan_filepath)`
    - **Purpose:** A comprehensive "linter" that runs a full suite of checks on a plan file, including `validate`, `analyze`, and an additional `check_for_recursion` to ensure the plan doesn't contain disallowed recursive calls to the FDC tool itself.
    - **Usage:** `python3 tooling/fdc_cli.py lint <path/to/plan.txt>`

### `tooling/knowledge_compiler.py`

**Purpose:**
This script automates the process of building the agent's long-term memory. It parses completed post-mortem reports, extracts the structured "lessons learned," and appends them to the central `knowledge_core/lessons_learned.md` file. This ensures that insights gained from one task are captured and made available for future reference.

**Key Functions:**
- `extract_lessons_from_postmortem(postmortem_content)`: Uses regular expressions to find and parse the "Corrective Actions & Lessons Learned" section of a post-mortem file, extracting each "Lesson" and corresponding "Action".
- `extract_metadata_from_postmortem(postmortem_content)`: Pulls out metadata from the report, such as the `Task ID` and `Completion Date`, to provide context for the extracted lessons.
- `format_lesson_entry(metadata, lesson_data)`: Takes the extracted metadata and a lesson, and formats them into a standardized entry suitable for the `lessons_learned.md` file.
- `main()`: The script's entry point. It takes a path to a post-mortem file as a command-line argument, orchestrates the extraction and formatting process, and appends the new entries to the knowledge base.

**Usage:**
This script is typically called automatically by the `master_control.py` orchestrator after a post-mortem has been finalized, but it can also be run manually.
```bash
python3 tooling/knowledge_compiler.py <path/to/postmortem.md>
```

### `tooling/master_control.py`

**Purpose:**
This script is the **central orchestrator** of the agent's entire lifecycle. It acts as a high-level Finite State Machine (FSM) that guides the agent through a strict, protocol-defined workflow, from initial setup to final submission. Its primary responsibility is to enforce the correct sequence of operations and to act as a control gate, ensuring that the agent cannot proceed to the next phase until the current one is completed and validated.

**Core Component:**
- `MasterControlGraph`: This class implements the FSM logic. It reads its state definitions from `tooling/fsm.json` and transitions between states based on triggers returned by its state-handling functions.

**Key States & Workflow:**

1.  **`ORIENTING`**:
    - **Handler:** `do_orientation()`
    - **Action:** The script begins by executing a multi-level orientation protocol to gather context. This includes reading `knowledge_core/agent_meta.json` (L1 Self-Awareness), scanning the `knowledge_core/` directory (L2 Repo Sync), and probing the environment (L3 Environmental Probe).

2.  **`PLANNING`**:
    - **Handler:** `do_planning()`
    - **Action:** This is a critical control point. The orchestrator pauses and waits for the agent to create a `plan.txt` file. Once detected, it uses `tooling/fdc_cli.py validate` to formally verify the plan. The agent cannot proceed if the plan is invalid.

3.  **`EXECUTING`**:
    - **Handler:** `do_execution()`
    - **Action:** The orchestrator executes the validated plan one step at a time. It waits for the agent to create a `step_complete.txt` file after each step before advancing to the next one.

4.  **`AWAITING_ANALYSIS`**:
    - **Handler:** `do_awaiting_analysis()`
    - **Action:** After execution is complete, the orchestrator creates a draft post-mortem report and waits for the agent to signal that it has completed its analysis by creating an `analysis_complete.txt` file.

5.  **`POST_MORTEM`**:
    - **Handler:** `do_post_mortem()`
    - **Action:** The script finalizes the post-mortem report by renaming it. Crucially, it then calls `tooling/knowledge_compiler.py` to automatically extract lessons from the report and add them to the agent's long-term knowledge base.

6.  **`AWAITING_SUBMISSION`**:
    - **Action:** The final state where the agent's work is complete and ready for submission.

**Usage:**
This script is the main entry point for the agent's autonomous operation. The `if __name__ == "__main__":` block demonstrates how it is initialized and run, kicking off the entire task-handling process.

### `tooling/protocol_auditor.py`

**Purpose:**
This script is a meta-analysis tool designed to audit the agent's behavior and protocols. It answers two key questions:
1.  Are all tools used by the agent formally associated with a protocol? (Completeness)
2.  Which tools are most central to the agent's workflow? (Centrality)

It works by comparing the tools recorded in a usage log (`tool_demonstration_log.txt`) against the tools defined in the `AGENTS.md` protocol file.

**Key Functions:**
- `get_used_tools_from_log(log_path)`: Parses the simple text log of tool usage.
- `get_protocol_tools_from_agents_md(agents_md_path)`: Parses the JSON block within `AGENTS.md` to extract a set of all tools that are formally associated with at least one protocol.
- `run_completeness_check(used_tools, protocol_tools)`: Compares the two sets of tools and reports on any discrepancies, such as tools that are used but not documented in a protocol, or vice-versa.
- `run_centrality_analysis(used_tools)`: Performs a frequency count on the used tools to identify which are most critical to the agent's operations.
- `main()`: The entry point that orchestrates the audit by calling the data extraction and analysis functions.

**Usage:**
This script is a diagnostic tool for developers and system maintainers to ensure the agent's protocols remain comprehensive and that its behavior adheres to them.
```bash
python3 tooling/protocol_auditor.py
```

### `tooling/protocol_compiler.py`

**Purpose:**
This script acts as a build tool that generates the `AGENTS.md` file, which is the single source of truth for the agent's protocols. It combines human-readable documentation with machine-readable rules into a single, comprehensive artifact.

**Process:**
1.  **Find Sources:** The script scans the `protocols/` directory for two types of source files:
    - `*.protocol.md`: Contain the high-level, human-readable prose explaining the "why" behind a protocol.
    - `*.protocol.json`: Contain the formal, machine-readable rules and tool associations for that protocol.
2.  **Validate:** It validates each `.json` file against the schema defined in `protocols/protocol.schema.json` to ensure correctness.
3.  **Combine:** It pairs the `.md` and `.json` files based on their numeric prefixes (e.g., `01_...md` and `01_...json`).
4.  **Generate:** It writes the final `AGENTS.md` file, interleaving the prose from the markdown files with the corresponding JSON rules in formatted code blocks.

**Key Functions:**
- `load_schema()`: Loads the `protocol.schema.json` for validation purposes.
- `compile_protocols()`: The main function that orchestrates the entire find, validate, combine, and generate process.
- `main()`: The script's entry point, which simply calls `compile_protocols()`.

**Usage:**
This script is intended to be run as part of the build process, typically via the `Makefile`. It can also be run directly to manually regenerate the `AGENTS.md` file.
```bash
python3 tooling/protocol_compiler.py
```

### `tooling/research.py`

**Purpose:**
This script provides a **unified, constraint-based interface** for all of the agent's research activities. It acts as a single entry point that can dispatch to different research methods (e.g., reading local files, querying the web) based on a set of input `constraints`. In its current form, it primarily functions as a **mocked or simulated tool**, providing predictable responses that allow for the testing and development of the higher-level orientation protocol in `master_control.py`.

**Core Function:**
- `execute_research_protocol(constraints: Dict[str, Any]) -> str`: This is the main function of the script. It takes a dictionary of constraints that define the research task and returns a string result.

**Constraint-Based Dispatch & Research Levels:**

The `constraints` dictionary determines the type of research to be performed:

-   **Level 1 (Self-Awareness):**
    -   **Constraints:** `{"target": "local_filesystem", "scope": "file", "path": "..."}`
    -   **Action:** Reads and returns the content of a single local file. Used by the orchestrator to read `agent_meta.json`.

-   **Level 2 (Repository Sync):**
    -   **Constraints:** `{"target": "local_filesystem", "scope": "directory", "path": "..."}`
    -   **Action:** Lists and returns the contents of a local directory. Used by the orchestrator to scan the `knowledge_core/` directory.

-   **Level 3 (Targeted RAG):**
    -   **Constraints:** `{"target": "external_web", "scope": "narrow", "query": "..."}`
    -   **Action:** Simulates a narrow, targeted web search and returns a mock answer.

-   **Level 4 (Deep Research):**
    -   **Constraints:** `{"target": "external_web", "scope": "broad"}`
    -   **Action:** Simulates a broad, deep research task and returns a mock report.

-   **External Repository Research:**
    -   **Constraints:** `{"target": "external_repository", "path": "..."}`
    -   **Action:** Fetches and returns the content of a file from a remote Git repository via raw HTTP request.

**Usage:**
This script is not intended to be run directly. It is imported and called by other components, primarily `tooling/master_control.py`, which uses it to execute the different stages of the orientation protocol.

### `tooling/research_planner.py`

**Purpose:**
This script is a specialized templating tool designed to generate a structured **deep research plan** in markdown format. It provides a consistent, multi-phase workflow for the agent to follow when it needs to conduct in-depth research on a specific topic.

**Core Function:**
- `plan_deep_research(topic: str, repository: str) -> str`: The main function that takes a research `topic` and a `repository` context ('local' or 'external') and returns a formatted markdown plan.

**Workflow:**
1.  **Context Gathering:** Based on the `repository` argument, the function determines the governing protocol.
    -   If `'local'`, it reads the local `AGENTS.md` file.
    -   If `'external'`, it uses the `research.py` tool to fetch a protocol file from a remote repository.
2.  **Template Generation:** It injects the research `topic` and a snippet of the gathered protocol context into a predefined markdown template.
3.  **Structured Output:** The template outlines a clear, four-phase research process:
    -   Phase A: Initial Planning & Question Formulation
    -   Phase B: Parallel Research Execution
    -   Phase C: Synthesis and Refinement
    -   Phase D: Final Report Generation

**Usage:**
This script is a helper utility that can be used to kick-start a formal research process by providing a robust, repeatable plan structure. It can be run directly to see example outputs.
```bash
python3 tooling/research_planner.py
```

### `tooling/self_improvement_cli.py`

**Purpose:**
This script is a diagnostic tool designed for **meta-analysis and self-improvement**. Its primary function is to analyze the agent's activity log (`logs/activity.log.jsonl`) to identify patterns that may indicate inefficiencies in its workflow.

**Core Function:**
- `analyze_planning_efficiency(log_file)`: This is the main analysis function. It reads through the log file and counts the number of times a `PLAN_UPDATE` action occurs for each unique task ID.

**Workflow:**
1.  **Read Log:** The script ingests the JSONL activity log.
2.  **Count Plan Revisions:** It iterates through each log entry, identifying actions related to plan updates (e.g., `set_plan`).
3.  **Identify Inefficiencies:** It aggregates the counts of plan updates on a per-task basis.
4.  **Report Findings:** The script prints a report listing any tasks that had more than one plan revision, as this suggests that the agent had to stop and rethink its approach, which could be a sign of an inefficient initial planning phase.

**Usage:**
This script is used to get a high-level view of the agent's performance over time and to pinpoint specific tasks where the planning process could be improved.
```bash
python3 tooling/self_improvement_cli.py [--log-file <path/to/log>]
```

### `tooling/state.py`

**Purpose:**
This script defines the `AgentState` dataclass, which is a simple but critical component of the agent's architecture. Its sole purpose is to act as a **state container**, holding all the information that defines the agent's current workflow status. An instance of this class is passed between the different states of the `master_control.py` FSM.

**Core Component:**
- `AgentState`: A Python dataclass that aggregates various pieces of state information into a single, well-defined object.

**Key Attributes:**
- `task`: The high-level task description given to the agent.
- `plan`: The validated plan that the agent is currently executing.
- `messages`: A list of messages, likely for maintaining a conversational history.
- `orientation_complete`: A boolean flag indicating if the initial orientation phase is done.
- `vm_capability_report`: Stores the output from the `environmental_probe.py` script.
- `current_step_index`: An integer that tracks the agent's progress through its plan.
- `draft_postmortem_path`: The path to the draft post-mortem file during the analysis phase.
- `final_report`: Stores the confirmation message after the post-mortem is finalized.
- `error`: A field to store any critical error messages that halt the FSM.

**Usage:**
This script is not run directly. The `AgentState` class is imported and instantiated by `tooling/master_control.py` at the beginning of a new task. The object is then passed to each state-handling function (`do_orientation`, `do_planning`, etc.), which reads from and writes to it.

### `tooling/symbol_map_generator.py`

**Purpose:**
This script generates a **symbol map** of the codebase, which is a JSON file (`knowledge_core/symbols.json`) that lists all the important symbols (classes, functions, etc.) and their locations. This artifact is critical for the agent's ability to understand the structure of the code it is working with.

**Methodology:**
The script uses a two-tiered approach to symbol generation:

1.  **Primary Method (Universal Ctags):** It first checks if `Universal Ctags` is installed and available in the system's PATH. If it is, the script uses `ctags` to perform a deep, multi-language scan of the repository. This is the preferred method as it is fast, comprehensive, and supports multiple languages (Python, JavaScript).
2.  **Fallback Method (AST):** If `ctags` is not available, the script gracefully degrades to a fallback mode that uses Python's built-in `ast` (Abstract Syntax Tree) module. This method can only parse Python files, but it ensures that a basic level of symbol information is always available.

**Key Functions:**
- `has_ctags()`: Checks for the presence of the `ctags` executable.
- `generate_symbols_with_ctags(root_dir)`: Runs the `ctags` command with a JSON output format and then processes the line-delimited JSON output into a single, valid JSON array.
- `generate_symbols_with_ast(root_dir)`: Recursively walks the directory tree, reads Python files, parses them with the `ast` module, and extracts all class and function definitions.
- `main()`: The entry point that orchestrates the process, checking for `ctags` and calling the appropriate generator function.

**Usage:**
This script is intended to be run from the repository root to generate or update the symbol map.
```bash
python3 tooling/symbol_map_generator.py
```

---

## `utils/` Directory

### `utils/logger.py`

**Purpose:**
This script provides a `Logger` class that is responsible for creating structured, schema-validated log entries. It ensures that all agent activities are recorded in a consistent, machine-readable JSONL format (`logs/activity.log.jsonl`), which is essential for debugging, analysis, and self-improvement.

**Core Component:**
- `Logger`: A class that encapsulates the logic for creating and writing log entries.

**Workflow:**
1.  **Initialization:** When a `Logger` object is created, it loads the formal logging schema from `LOGGING_SCHEMA.md` and generates a unique `session_id` for the current work session.
2.  **Schema Loading:** The `_load_schema()` method extracts the JSON schema from the markdown file. If the schema cannot be loaded, the logger will continue to function but without the validation step.
3.  **Log Creation:** The `log()` method is the primary interface. It takes numerous arguments (e.g., `phase`, `task_id`, `action_type`, `outcome_status`) and constructs a dictionary representing the log entry.
4.  **Validation:** If a schema was loaded successfully, the `log()` method uses the `jsonschema` library to validate the newly created log entry against the schema. This prevents malformed data from being written to the log.
5.  **Writing to File:** The validated log entry is serialized to a JSON string and appended as a new line to the `activity.log.jsonl` file.

**Usage:**
This script is not run directly. An instance of the `Logger` class is created by the agent's main process, and the `log()` method is called whenever a significant action is performed.

```python
# Example instantiation and usage
from utils.logger import Logger

# Create a logger instance
logger = Logger()

# Log a tool execution event
logger.log(
    phase="Phase 3",
    task_id="example-task-01",
    plan_step=2,
    action_type="TOOL_EXEC",
    action_details={"command": "ls -l"},
    outcome_status="SUCCESS",
    outcome_message="Listed files successfully."
)
```