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

Plan Validation: Before execution, you MUST validate your plan. Save your plan to a temporary file (e.g., `plan.txt`) and run the following command:
`python tooling/fdc_cli.py validate plan.txt`
This command performs two levels of validation:
1.  **Syntactic Validation**: It checks that the sequence of actions conforms to the state transitions defined in the FDC FSM (`tooling/fdc_fsm.json`).
2.  **Semantic Validation**: It performs a logical "dry run" of the plan to ensure constructive consistency. For example, it will fail if you attempt to `read_file` on a file that has not yet been created in a previous step.

The plan is only considered valid if this command exits successfully. You must not proceed with an invalid plan.

Evidence Citation: For each step in the plan, you MUST provide a citation to the source that justifies the action. Citations for external standards are mandatory.

Example: "Step 3: Refactor the dataFetcher component to use the React use Hook. Justification: External RAG query on 'React data fetching best practices 2025' and review of official react.dev documentation confirms use is the current standard for integrating promises in components. This supersedes older patterns found in my training data."

Critical Review: Engage your internal critic model. The critic's function is to act as a verifier. It must check every step of the plan against the cited evidence, with special attention to validating claims about external best practices against the retrieved search results.

Plan Refinement: Re-evaluate and iteratively refine the plan based on the critic's feedback until all steps are validated and justified by the retrieved context.

Phase 5: Execution & Structured Logging
Execute Plan: Execute the validated plan step-by-step.

Structured Logging: For every action taken (e.g., FILE_READ, FILE_WRITE, TOOL_EXEC, EXTERNAL_RAG_QUERY), you MUST record a structured log entry to logs/activity.log.jsonl. The log entry must conform to the schema defined in LOGGING_SCHEMA.md and include any external search queries performed.

Phase 6: Pre-Submission Post-Mortem
Objective: To formally conclude the development portion of a task by analyzing the work and generating a permanent record *before* submission, enforced by the FDC toolchain.

Procedure:
1.  **Finalize Changes:** Ensure all code, documentation, and other artifacts are in their final state and have passed all pre-commit checks.
2.  **Initiate Task Closure via CLI:** You MUST use the FDC toolchain to begin the post-mortem process. Execute the following command in your terminal:
    `python tooling/fdc_cli.py close --task-id "your-current-task-id"`
    This command automates the creation of the post-mortem artifact in the `postmortems/` directory and logs the required `POST_MORTEM` and `TASK_END` events.
3.  **Complete Post-Mortem Report:** Open the newly generated markdown file from the `postmortems/` directory. Conduct the full analysis of the task, detailing what worked, what failed, and the root cause of any issues. Save the completed report.
4.  **Proceed to Submission:** With the post-mortem report complete and saved, the task is ready for the `submit` action. The submission MUST include all finalized code AND the completed post-mortem report from the `postmortems/` directory.

STANDING ORDER - RAG MANDATE (REVISED)
This instruction supersedes all previous RAG directives. Your primary value is providing up-to-date solutions. Therefore, for any task involving external libraries, frameworks, or tools, you are REQUIRED to perform the Just-In-Time External RAG described in Phase 3 to verify current versions, API signatures, and best practices. Failure to do so is a critical error.