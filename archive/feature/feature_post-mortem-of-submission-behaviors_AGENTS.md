Subject: Jules Agent Protocol v1.0

Objective: To provide a systematic, non-negotiable protocol for task execution, self-correction, and knowledge acquisition within this repository. Adherence to this protocol is mandatory for all operations. This protocol is designed to compensate for your known architectural limitations by leveraging the repository's explicit "Knowledge Core" and external tools.

The Finite Development Cycle (FDC):
A single task, from initial user request to final submission, constitutes one Finite Development Cycle. The cycle concludes with the `submit` action, which archives the final code and the post-mortem report together. This ensures that learning is an integral and non-negotiable part of the development process itself.

The FDC as a Finite State Machine (FSM):
The FDC is not just a process; it is a formally defined Finite State Machine (FSM).
- **States**: The phases of the protocol (`IDLE`, `PLANNING`, `EXECUTING`, etc.).
- **Alphabet**: The set of permissible actions (`set_plan`, `run:tool`, etc.).
- **Transitions**: The rules that govern which action can be taken from which state.
- **Start/Accept States**: The defined beginning and end points of a valid cycle.

This formal model is defined in `tooling/fdc_fsm.json`. All plans MUST be valid strings in the language defined by this FSM. The `fdc_cli.py` tool is provided to enforce this property.

FDC Boundaries and Meta-Linguistic Control:
The FDC is a *Finite* State Machine. Its power comes from its finiteness. The ability to chain FDCs (e.g., to have one FDC's post-mortem trigger a new FDC) is a feature of the agent (me) or the user operating in the larger development environment. This "chaining" is a meta-linguistic operation that exists *outside* the formal boundaries of any single FSM. An FSM that can infinitely chain into other FSMs is not, in fact, a formal FSM.

The Nature of Validation (Paraconsistency):
A process cannot be its own ultimate validator (a Tarskian or Kripkean principle). Therefore, when the `fdc_cli.py validate` tool analyzes a plan, it is performing a powerful but ultimately **heuristic and paraconsistent** check. It's a "linter" for plans that can find many classes of errors, but it is not a formal proof of correctness. A truly consistent validation would require a higher-order process. This is an accepted and understood limitation of the system.

FDC Complexity Classes:
Beyond syntactic and semantic validity, FDCs are classified by their computational complexity. This allows for reasoning about the scope and nature of a task. The `fdc_cli.py analyze` command is used to determine a plan's complexity class.
- **Constant Complexity (O(1))**: Represents tasks with a fixed, predictable number of steps, regardless of the size of the codebase. These plans contain no loops.
- **Polynomial Complexity (P-Class)**: Represents tasks where the amount of work scales with the size of a given input set (e.g., number of files). These are expressed using single `for_each_file` loops.
- **Exponential Complexity (EXPTIME-Class)**: Represents tasks of a higher order, typically involving operations on combinations of inputs (e.g., comparing every file to every other file). These are expressed using nested `for_each_file` loops.

The Meta-Process Complexity Hierarchy:
A Finite Development Cycle can only serve as a meta-process for a project of a strictly lower complexity class.
- To manage a **Constant (O(1))** project, the FDC must be at least **P-Class**.
- To manage a **Polynomial (P-Class)** project, the FDC must be at least **EXPTIME-Class**.
This principle ensures that the process has sufficient expressive power to manage the complexity of its object.

FDC Modalities:
In addition to complexity, FDCs are classified by their modality, which describes their intended impact on the codebase. This is determined by the `analyze` subcommand based on the actions in a plan.
- **Analysis Modality (Read-Only)**: The FDC inspects the codebase but does not alter it. It contains only `read_op` and `tool_exec` actions. Its primary output is knowledge (e.g., a report, log entries).
- **Construction Modality (Read-Write)**: The FDC alters the codebase. It contains `write_op`, `delete_op`, or `move_op` actions. Its primary output is a change to the repository's state.

FDC Value Categories:
The final dimension of an FDC is its value, which allows for strategic prioritization. This is declared via metadata in the plan file.
- **Value Categories**:
  - `Protocol-Improvement`: Enhances `AGENTS.md` or the FSM.
  - `Toolchain-Enhancement`: Improves the `fdc_cli.py` or other tooling.
  - `Bug-Fix`: Corrects a demonstrable error in code or process.
  - `Feature-Implementation`: Adds a new capability to the system.
- **High-Value, Low-Cost (HVLC) Tasks**: A task is formally defined as "low-hanging fruit" if it meets two criteria:
  1. Its **Complexity** is **Constant (O(1))**.
  2. Its **Value** is one of the high-value categories (e.g., `Protocol-Improvement`, `Bug-Fix`).

Phase 0: Initialization Mandate (First Run Only)
Objective: To ensure the operational environment is correctly bootstrapped before any other task is undertaken. This phase is executed once at the beginning of the very first session in a new repository clone.

Procedure:
1. Verify Core Directories: You must check for the existence of the following directories at the repository root:
   - `knowledge_core/`
   - `knowledge_core/asts/`
   - `logs/`
   If any are missing, you MUST create them.

2. Verify Core Artifacts: You must check for the existence of the following files. If any are missing, you MUST create them with their default content.
   - `knowledge_core/temporal_orientation.md` (Create with a header indicating it's an auto-generated file).
   - `knowledge_core/symbols.json` (Create as an empty JSON object: `{}`).
   - `knowledge_core/dependency_graph.json` (Create as an empty JSON object: `{}`).
   - `knowledge_core/llms.txt` (Create with a placeholder description).
   - `logs/activity.log.jsonl` (Create as an empty file).
   - `LOGGING_SCHEMA.md` (Create with the standard schema definition).
   - `postmortem.md` (Create with a placeholder header).
   - `README.md` (Create with a standard project overview).

3. Confirmation: Only after confirming or creating all required artifacts may you proceed to Phase 1. This entire initialization process constitutes your first task.

Phase 1: Temporal Orientation (Scheduled & Ad-Hoc)
Mandate for External Awareness: Your internal knowledge base is frozen as of late 2022. You MUST assume it is outdated for all external technologies, libraries, and frameworks. Your primary source of truth for current standards and best practices is the live internet, accessed via your search tools.

Scheduled Orientation Refresh: A separate, automated process (.github/workflows/temporal-orientation-refresh.yml) runs on a recurring basis. This process:

Scans the repository's manifest files (package.json, Cargo.toml, etc.) to identify all primary external dependencies.

For each major dependency, uses external search tools to retrieve the latest version number, links to official documentation, and summaries of significant changes since late 2022.

Synthesizes this information into a structured report and overwrites the knowledge_core/temporal_orientation.md artifact. This artifact serves as your cached "map of the present."

Pre-Task Orientation Check: At the beginning of EVERY new task, you must first consult knowledge_core/temporal_orientation.md to understand the current landscape of the technologies relevant to the task.

Phase 2: Deconstruction & Internal Contextualization
Task Ingestion: Receive the user-provided task.

Meta-RAG for Cross-Task Learning: Before beginning any new task, perform a RAG query against the `logs/` directory. Search for log entries and `postmortem.md` reports from past tasks that are semantically similar to the current task. Analyze the `critic_feedback`, `status`, and post-mortem summaries from these past tasks to identify previously encountered failure patterns and successful strategies. You must explicitly state in your new plan how you will leverage these historical lessons.

Entity Identification: Identify all candidate code entities (functions, classes, modules, files) relevant to the task description. Perform a direct lookup against the `knowledge_core/symbols.json` artifact to resolve these candidates to concrete symbols and their exact locations (file path, line number).

Impact Analysis: Using the file paths identified in the previous step as a starting point, construct a dependency impact analysis. Query the `knowledge_core/dependency_graph.json` artifact to identify all immediate upstream dependents (code that will be affected by changes) and downstream dependencies (code that the target entities rely on). The complete set of all identified files constitutes the "Task Context Set."

Phase 3: Multi-Modal Information Retrieval (RAG)
Structural Retrieval (Internal): For every file in the Task Context Set, retrieve its corresponding Abstract Syntax Tree (AST) from the knowledge_core/asts/ directory. Use these ASTs to gain a deep, syntactic understanding of function signatures, call sites, data structures, and class hierarchies. This is your primary source for structural reasoning.

Conceptual Retrieval (Internal): Formulate a precise query based on the task description and the names of the primary entities involved. Execute this query against the knowledge_core/llms.txt artifact. This is your primary source for retrieving architectural principles and project-specific domain knowledge (e.g., details of the non-classical logic).

Just-In-Time External RAG: The temporal_orientation.md artifact provides a baseline. However, for the specific APIs or patterns required by the task, you MUST perform a targeted external search using your tools. The goal is to find the most current, official documentation and best-practice examples for the specific versions of the libraries you are working with. Do not rely on your internal knowledge.

Knowledge Synthesis: Consolidate all retrieved information—internal symbols, dependencies, ASTs, project docs, and CRITICALLY, the up-to-date external documentation and standards—into a unified context briefing.

Phase 4: Planning & Self-Correction
Plan Generation: Based on the synthesized context briefing, generate a detailed, step-by-step execution plan. The plan must be granular, with each step representing a single, atomic action.

Plan Language Constructs:
To declare the intended value of a plan, you must include a metadata block at the top of the plan file.
- **Metadata Syntax**:
  `# META`
  `# value: <Value-Category>`
  `# END META`

To represent iterative tasks, the plan language supports a `for_each_file` loop.
- **Syntax**:
  `for_each_file <glob_pattern>`
  `  <action_to_perform_on_{file}>`
- **Semantics**: The indented block of one or more actions will be logically executed for each file that matches the provided glob pattern (e.g., `src/**/*.py`). Within the loop block, the special placeholder `{file}` will be substituted with the path of the file being processed.
- **Nested Loops**: To represent EXPTIME-Class tasks, loops can be nested. The placeholder variable must be numbered according to its nesting level (e.g., `{file1}`, `{file2}`).
  `for_each_file <glob1>`
  `  for_each_file <glob2>`
  `    compare {file1} {file2}`

Plan Validation: Before execution, you MUST validate your plan. Save your plan to a temporary file (e.g., `plan.txt`) and run the following command:
`python tooling/fdc_cli.py validate plan.txt`
This command performs two levels of validation:
1.  **Syntactic Validation**: It checks that the sequence of actions conforms to the state transitions defined in the FDC FSM (`tooling/fdc_fsm.json`).
2.  **Semantic Validation**: It performs a logical "dry run" of the plan to ensure constructive consistency. For example, it will fail if you attempt to `read_file` on a file that has not yet been created in a previous step.

The plan is only considered valid if this command exits successfully. You must not proceed with an invalid plan.

Plan Analysis: After successful validation, you MUST analyze the plan's properties. Run the following command:
`python tooling/fdc_cli.py analyze plan.txt`
You must state the resulting **Complexity Class**, **Modality**, and **Value Category** in your reasoning before proceeding to execution.

Meta-Process Analysis: If the current FDC is a meta-process (i.e., it is operating on another process or FDC), you must also analyze and declare the complexity of the object process. You must then confirm that the complexity of the current plan is strictly higher than the complexity of the object process, in accordance with the Meta-Process Complexity Hierarchy.

Evidence Citation: For each step in the plan, you MUST provide a citation to the source that justifies the action. Citations for external standards are mandatory.

Example: "Step 3: Refactor the dataFetcher component to use the React use Hook. Justification: External RAG query on 'React data fetching best practices 2025' and review of official react.dev documentation confirms use is the current standard for integrating promises in components. This supersedes older patterns found in my training data."

Critical Review: Engage your internal critic model. The critic's function is to act as a verifier. It must check every step of the plan against the cited evidence, with special attention to validating claims about external best practices against the retrieved search results.

Plan Refinement: Re-evaluate and iteratively refine the plan based on the critic's feedback until all steps are validated and justified by the retrieved context.

Phase 5: Execution & Structured Logging
Execute Plan: Execute the validated plan step-by-step.

Structured Logging: For every action taken (e.g., FILE_READ, FILE_WRITE, TOOL_EXEC, EXTERNAL_RAG_QUERY), you MUST record a structured log entry to logs/activity.log.jsonl. The log entry must conform to the schema defined in LOGGING_SCHEMA.md and include any external search queries performed.

Phase 6: Formal Task Termination
Objective: To formally and explicitly conclude a Finite Development Cycle (FDC) with an immutable, three-part sequence of events. This sequence ensures a clear boundary between the completion of development work, the act of reflection, and the final archival of the task.

The Three Stages of Termination:
The termination of an FDC is not a single action but a strict, ordered process. You MUST execute these three stages, in this order, without any intervening actions.

Stage 1: Log `TASK_END`
- **Purpose**: To create a clear, machine-readable event that marks the definitive end of all development and testing activities for the current task. This is the "pencils down" moment.
- **Action**: You will log a `TASK_END` event. This is the first step in the closing sequence.

Stage 2: Log `POST_MORTEM`
- **Purpose**: To conduct and log a formal analysis of the completed task. This captures critical lessons learned, successes, and failures, ensuring they are available for future `Meta-RAG` queries.
- **Action**: After logging `TASK_END`, you will immediately conduct the post-mortem analysis and log a `POST_MORTEM` event. This includes creating or updating the relevant `postmortem.md` file.

Stage 3: Submit
- **Purpose**: To archive the final state of the code, the complete log history (including the `TASK_END` and `POST_MORTEM` events), and the post-mortem report in a single, atomic commit.
- **Action**: After the `POST_MORTEM` is logged, you will use the `submit` tool. This action formally closes the FDC. No further actions related to the task are permitted after this point.

**Enforcement via Tooling:**
The `tooling/fdc_cli.py close` command is the designated tool for executing this termination sequence. It is designed to run the `TASK_END` and `POST_MORTEM` stages, preparing the repository for the final `submit` action. Using this tool is mandatory to ensure protocol adherence.

STANDING ORDER - RAG MANDATE (REVISED)
This instruction supersedes all previous RAG directives. Your primary value is providing up-to-date solutions. Therefore, for any task involving external libraries, frameworks, or tools, you are REQUIRED to perform the Just-In-Time External RAG described in Phase 3 to verify current versions, API signatures, and best practices. Failure to do so is a critical error.

STANDING ORDER - POST-SUBMISSION PROTOCOL
Upon using the `submit` tool, you will consider the submission action complete. Any subsequent user interaction, unless it explicitly states there was a submission failure, shall be interpreted as an implicit confirmation that the submission was successful and a new task is beginning. You are forbidden from issuing messages such as "awaiting confirmation" or "submission pending." Your immediate action following a user response post-submission is to begin the next task cycle, starting with `Phase 1: Temporal Orientation` or `Phase 2: Deconstruction` as appropriate.