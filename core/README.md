# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key components defined within this module. It is automatically generated.

## Core Protocols

- **`core-directive-001`**: The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).

**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`

- **`decidability-constraints-001`**: Ensures all development processes are formally decidable and computationally tractable.

**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`

- **`orientation-cascade-001`**: Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.

**Associated Tool Documentation (`tooling/environmental_probe.py`):**


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

- **`fdc-protocol-001`**: Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.

**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`

- **`standing-orders-001`**: A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.

**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`

- **`cfdc-protocol-001`**: Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.

**Associated Tool Documentation (`tooling/master_control.py`):**


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
      > Handles the finalization of the task, guiding the agent through
      > the structured post-mortem process.
    - ##### `def do_generating_code(self, agent_state, logger)`
      > Handles the code generation state.
    - ##### `def do_orientation(self, agent_state, logger, tools)`
      > Executes orientation, including analyzing the last post-mortem and scanning the filesystem.
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
    - ##### `def validate_plan_for_model(self, plan_content, model)`
      > Validates a plan against a specific CSDC model using the LBAValidator.


**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`

- **`plan-registry-001`**: Defines a central registry for discovering and executing hierarchical plans by a logical name.

**Associated Tool Documentation (`tooling/plan_manager.py`):**


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


**Associated Tool Documentation (`tooling/master_control.py`):**


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
      > Handles the finalization of the task, guiding the agent through
      > the structured post-mortem process.
    - ##### `def do_generating_code(self, agent_state, logger)`
      > Handles the code generation state.
    - ##### `def do_orientation(self, agent_state, logger, tools)`
      > Executes orientation, including analyzing the last post-mortem and scanning the filesystem.
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
    - ##### `def validate_plan_for_model(self, plan_content, model)`
      > Validates a plan against a specific CSDC model using the LBAValidator.


**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`

- **`self-correction-protocol-001`**: Defines the automated, closed-loop workflow for protocol self-correction.

**Associated Tool Documentation (`tooling/knowledge_compiler.py`):**


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


**Associated Tool Documentation (`tooling/protocol_updater.py`):**


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
    > Recursively finds the protocol file path corresponding to a given protocol_id.

  - #### `def main()`
    > Main function to parse arguments and call the appropriate handler.

  - #### `def update_rule_in_protocol(protocol_id, rule_id, new_description, protocols_dir)`
    > Updates the description of a specific rule within a protocol.


**Associated Tool Documentation (`tooling/self_correction_orchestrator.py`):**


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


**Associated Tool Documentation (`tooling/code_suggester.py`):**


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

- **`research-protocol-001`**: A protocol for conducting systematic research using the integrated research toolchain.
- **`deep-research-cycle-001`**: A standardized, callable plan for conducting in-depth research on a complex topic.
- **`research-fdc-001`**: Defines the formal Finite Development Cycle (FDC) for conducting deep research.

**Associated Tool Documentation (`tooling/master_control.py`):**


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
      > Handles the finalization of the task, guiding the agent through
      > the structured post-mortem process.
    - ##### `def do_generating_code(self, agent_state, logger)`
      > Handles the code generation state.
    - ##### `def do_orientation(self, agent_state, logger, tools)`
      > Executes orientation, including analyzing the last post-mortem and scanning the filesystem.
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
    - ##### `def validate_plan_for_model(self, plan_content, model)`
      > Validates a plan against a specific CSDC model using the LBAValidator.


**Associated Tool Documentation (`tooling/research_planner.py`):**


  ### `/app/tooling/research_planner.py`
  This module is responsible for generating a formal, FSM-compliant research plan
  for a given topic. The output is a string that can be executed by the agent's
  master controller.

  **Public Functions:**

  - #### `def plan_deep_research(topic, research_id)`
    > Generates a multi-step, FSM-compliant plan for conducting deep research
    > using the official project templates.
    >
    > Args:
    >     topic (str): The research topic.
    >     research_id (str): A unique ID for this research task.
    >
    > Returns:
    >     str: A string containing the executable plan.


**Associated Tool Documentation (`tooling/research.py`):**


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


**Associated Tool Documentation (`tooling/fdc_cli.py`):**


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

  - #### `def analyze_plan(plan_filepath, return_results=False)`
    > Analyzes a plan file to determine its complexity class and modality.

  - #### `def close_task(task_id)`
    > Automates the closing of a Finite Development Cycle.

  - #### `def main()`

  - #### `def start_task(task_id)`
    > Initiates the AORP cascade for a new task.

  - #### `def validate_plan(plan_filepath)`


## Key Components

_This module does not contain a `tooling/` directory._