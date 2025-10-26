# AGENTS.md (Dynamically Generated)

**Last Generated:** 2025-10-26 00:07:24 UTC

## Objective

To provide a systematic, non-negotiable protocol for task execution, self-correction, and knowledge acquisition within this repository. Adherence to this protocol is mandatory for all operations. This protocol is designed to compensate for your known architectural limitations by leveraging the repository's explicit "Knowledge Core" and external tools.

---

## Setup & Build Commands

The following build targets are the primary way to test, build, and maintain this repository. To run any target, use the command: `python3 tooling/builder.py --target <name>`

### Build Groups

- **`all`**: Runs the following targets: `protocols, docs, knowledge-compile, knowledge-integrate, agents-md`
- **`knowledge`**: Runs the following targets: `knowledge-compile, knowledge-integrate`

### Individual Targets

- **`protocols`**: Compile all protocols.
- **`docs`**: Generate system documentation.
- **`knowledge-compile`**: Compile lessons from post-mortems.
- **`knowledge-integrate`**: Integrate knowledge from various sources.
- **`guardian-protocol`**: Compile the guardian protocol.
- **`agents-md`**: Generate the master AGENTS.md file.
- **`install`**: Install Python dependencies.
- **`format`**: Format the code using black.
- **`lint`**: Lint the code using flake8.
- **`test`**: Run the test suite using pytest.

---

## Core Directives & Protocols

The agent's behavior is governed by the following set of formal protocols, which are dynamically generated from the repository's enriched knowledge core. You are required to adhere to these protocols at all times.

### A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.

**Rules:**

- The AGENTS.md file is a build artifact generated from source files in the 'protocols/' directory. Before relying on AGENTS.md, the agent should ensure it is up-to-date by running 'make AGENTS.md'. This ensures the agent is operating with the latest set of protocols.

---
### Defines a central registry for discovering and executing hierarchical plans by a logical name.

**Rules:**

- A central plan registry MUST exist at 'knowledge_core/plan_registry.json'. It maps logical plan names to their file paths.
- The 'call_plan <argument>' directive MUST first attempt to resolve '<argument>' as a logical name in the plan registry. If resolution fails, it MUST fall back to treating '<argument>' as a direct file path for backward compatibility.
- A dedicated tool (`tooling/plan_manager.py`) MUST be provided for managing the plan registry, with functions to register, deregister, and list plans.

---
### A set of best practices derived from observing successful, data-driven workflow patterns.

**Rules:**

- After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_block`, `replace_with_git_merge_diff`), the agent MUST use a subsequent read-only tool (`read_file`, `list_files`, `grep`) to verify that the action was executed successfully and had the intended effect. A plan step should only be marked as complete after this verification.

---
### A protocol to enforce Test-Driven Development (TDD) practices.

**Rules:**

- When writing any new function or class, a corresponding test must be written first. The test should fail before the new code is implemented, and pass after.

---
### A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.

**Rules:**

- Defines non-compliance as a violation of any rule, convention, or procedure in AGENTS.md or its source protocols.
- Prohibits the direct editing of build artifacts like AGENTS.md or README.md. Changes must be made to source files, followed by a rebuild.
- Requires adherence to all documented testing procedures before submitting changes.
- Forbids changes that contradict documented architectural patterns or coding conventions.
- Requires the agent to maintain an up-to-date understanding of protocols by recompiling AGENTS.md when necessary.

---
### A protocol governing the agent's core interaction and planning tools.

**Rules:**

- The agent is authorized to use the `set_plan` tool to create and update its execution plan. This is a foundational capability for task execution.
- The agent is authorized to use the `message_user` tool to communicate with the user, providing updates and asking for clarification. This is essential for a collaborative workflow.

---
### A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

**Rules:**

- If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that process it (`protocol_compiler.py`), a formal audit of the entire `tooling/` directory MUST be performed as a subsequent step. This audit should verify that all tools are compatible with the new protocol structure.

---
### A high-priority protocol that unconditionally forbids the use of the `reset_all` tool.

**Rules:**

- The `reset_all` tool is strictly forbidden under all circumstances. It is a legacy tool that has been superseded by more granular and safer methods of workspace management. Its use is considered a critical failure.

---
### A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.

**Rules:**

- All agent tasks must be initiated through the `agent_shell.py` script. This script is the designated, API-driven entry point that ensures proper initialization of the MasterControlGraph FSM, centralized logging, and programmatic lifecycle management. Direct execution of other tools or scripts is forbidden for task initiation.

---
### Defines the identity and purpose of the Security Protocol document.

---
### A protocol for integrating with the Google Gemini API.

**Rules:**

- The agent is authorized to use the Gemini API for advanced tasks.
- The agent must handle the Gemini API key securely.
- The agent must adhere to a strict sub-protocol when using the Gemini API's 'Computer Use' feature.

---
### A protocol for ensuring a reliable execution environment through formal dependency management.

**Rules:**

- Upon starting a task, after loading AGENTS.md, the agent MUST install all required Python packages listed in the `requirements.txt` file. This ensures the environment is correctly configured before any other tools are executed.

---
### A protocol for greeting the world.

**Rules:**

- When this rule is invoked, the agent must use the `hello_world` tool to print the message "Hello, World!".

---
### A protocol for standardized interaction with external agent APIs.

**Rules:**

- A central registry of all approved external agent APIs MUST be maintained at 'knowledge_core/external_api_registry.json'.
- API keys for external services MUST be managed securely via environment variables.
- A standardized client for interacting with external agent APIs MUST be implemented in 'tooling/external_api_client.py'.

---
### A protocol for executing pLLLU scripts, enabling a more expressive and powerful planning and automation language for the agent.

**Rules:**

- The `plllu_runner.py` tool should be used to execute .plllu script files. This tool provides the bridge between the agent's master control loop and the pLLLU language interpreter.

---
### Defines the formal Finite Development Cycle (FDC) for conducting deep research.

**Rules:**

- The Research FDC must be governed by its own dedicated Finite State Machine, defined in `tooling/research_fsm.json`. This FSM is tailored for a research workflow, with states for gathering, synthesis, and reporting.
- Research plans must be generated by `tooling/research_planner.py` as valid, executable plans that conform to the `research_fsm.json` definition. They are not just templates but formal, verifiable artifacts.
- The L4 Deep Research Cycle is the designated mechanism for resolving complex 'unknown unknowns'. It is invoked by the main orchestrator when a task requires knowledge that cannot be obtained through simple L1-L3 orientation probes.

---
### A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.

**Rules:**

- The `capability_verifier.py` tool should be used to test the agent's ability to acquire a new capability defined by a failing test file. The tool orchestrates the failure, self-correction, and verification process.

---
### Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.

**Rules:**

- Level 1 (Self-Awareness): The agent must first establish its own identity and inherent limitations by reading the `knowledge_core/agent_meta.json` artifact.
- Level 2 (Repository Sync): The agent must understand the current state of the local repository by loading primary artifacts from the `knowledge_core/` directory.
- Level 3 (Environmental Probing & Targeted RAG): The agent must discover the rules and constraints of its operational environment by executing a probe script and using targeted RAG to resolve 'known unknowns'.
- Level 4 (Deep Research Cycle): To investigate 'unknown unknowns', the agent must initiate a formal, self-contained Finite Development Cycle (FDC) of the 'Analysis Modality'.

---
### An experimental protocol to test dynamic rule-following. It mandates a prologue action before file creation.

**Rules:**

- Before creating any new file as part of a task, the agent MUST first create a file named 'prologue.txt' with the content 'This is a prologue file.' This rule serves as a test of the agent's ability to adapt its behavior to new, dynamically loaded protocols.

---
### A protocol for the unified repository auditing tool, which combines multiple health and compliance checks into a single interface.

**Rules:**

- The `auditor.py` script should be used to run comprehensive checks on the repository's health. It can be run with 'all' to check protocols, plans, and documentation completeness.

---
### A demonstration of a protocol with executable code.

**Rules:**

- Prints a hello world message to the console.

---
### A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods.

**Rules:**

- The agent may only initiate a speculative task when it has no active, user-assigned tasks.
- A speculative task must begin with the creation of a formal proposal document, outlining the objective, rationale, and plan.
- Speculative tasks must operate under defined resource limits.
- Final artifacts from a speculative task must be submitted for user review and cannot be merged directly.
- All logs and artifacts generated during a speculative task must be tagged as 'speculative'.

---
### A protocol for the unified documentation builder, which generates various documentation artifacts from the repository's sources of truth.

**Rules:**

- The `doc_builder.py` script is the single entry point for generating all user-facing documentation, including system-level docs, README files, and GitHub Pages. It should be called with the appropriate '--format' argument.

---
### A formal protocol for the agent to propose, validate, and implement improvements to its own operational protocols and tools.

**Rules:**

- Proposals for self-improvement must be initiated via the `self_improvement_cli.py` tool.
- Improvement proposals must be formally structured, including sections for 'Problem Statement', 'Proposed Solution', 'Success Criteria', and 'Impact Analysis'.
- Any proposed changes to protocols must be implemented in the relevant source files within the `protocols/` subdirectories, not directly in the generated AGENTS.md files.
- After protocol source files are modified, the `protocol_compiler.py` must be executed to re-compile the protocols and validate the changes.
- The success of an improvement must be verified by running relevant tests or a new, specific verification script.

---
### Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.

**Rules:**

- Plans may execute other plans as sub-routines using the 'call_plan <path_to_plan>' directive. This enables a modular, hierarchical workflow.
- To ensure decidability, the plan execution stack must not exceed a system-wide constant, MAX_RECURSION_DEPTH. This prevents infinite recursion and guarantees all processes will terminate.

---
### A specific, high-priority protocol that forbids the Code Review Critic agent from using the 'reset_all' tool.

**Rules:**

- The agent role-playing as the 'Code Review Critic' is explicitly forbidden from invoking the 'reset_all' tool under any circumstances. This is a critical safeguard to prevent the loss of work during the review process.

---
### A standardized, callable plan for conducting in-depth research on a complex topic.

**Rules:**

- The deep research plan MUST follow a structured four-phase process: Scoping, Broad Gathering, Targeted Extraction, and Synthesis.

---
### A protocol for maintaining an up-to-date file index to accelerate tool performance.

**Rules:**

- Before submitting any changes that alter the file structure (create, delete, rename), the agent MUST rebuild the repository's file index. This ensures that tools relying on the index, such as the FDC validator, have an accurate view of the filesystem.

---
### Defines the official policy and procedure for reporting security vulnerabilities.

**Rules:**

- All suspected security vulnerabilities MUST be reported privately to the designated security contact.
- Vulnerabilities MUST NOT be disclosed publicly until a patch is available and has been distributed.

---
### A protocol for controlling a web browser using the GeminiComputerUse tool.

**Rules:**

- When this rule is invoked, the agent must use the `gemini_computer_use` tool to perform a web-based task.

---
### A protocol for interacting with the Hypersequent-calculus-based logic engine, allowing the agent to perform formal logical proofs.

**Rules:**

- The `hdl_prover.py` tool should be used to check the provability of a logical sequent. This tool acts as a wrapper for the underlying Lisp-based prover.

---
### Defines the identity and versioning of the Advanced Orientation and Research Protocol (AORP).

**Rules:**

- The governing protocol set is identified as the Advanced Orientation and Research Protocol (AORP).
- The official protocol version is tracked in the VERSION file in the repository root, following Semantic Versioning (SemVer).

---
### A foundational protocol that dictates the agent's initial actions upon starting any task.

**Rules:**

- Upon initialization for any task, the agent's first and highest-priority action must be to locate, read, and parse the AGENTS.md file in the repository root. This ensures the agent is properly contextualized before any planning or execution begins.

---
### Defines the automated, closed-loop workflow for protocol self-correction.

**Rules:**

- Lessons learned from post-mortem analysis must be generated as structured, machine-readable JSON objects in `knowledge_core/lessons.jsonl`.
- All modifications to protocol source files must be performed programmatically via the `tooling/protocol_updater.py` tool to ensure consistency and prevent manual errors.
- The self-correction cycle must be managed by the `tooling/self_correction_orchestrator.py` script, which processes pending lessons and triggers the necessary updates.
- The self-correction system can modify the description of existing protocol rules via the `update-rule` command in `tooling/protocol_updater.py`, allowing it to refine its own logic.
- The self-correction system can generate and apply code changes to its own tooling. This is achieved through a `PROPOSE_CODE_CHANGE` action, which is processed by `tooling/code_suggester.py` to create an executable plan.

---
### A protocol that empowers the agent to modify its own core tooling, enabling a recursive self-improvement cycle.

**Rules:**

- The agent is authorized to use the 'modify_tooling' action within the self_correction_orchestrator.py to apply patches to its own source code or other tools in the tooling/ directory. This action must be triggered by a structured lesson in knowledge_core/lessons.jsonl.

---
### A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.

**Rules:**

- All Finite Development Cycles (FDCs) MUST be initiated using the FDC toolchain's 'start' command. This is non-negotiable.
- For any task involving external technologies, Just-In-Time External RAG is REQUIRED to verify current best practices. Do not trust internal knowledge.
- Use the `fdc_cli.py` tool for all core FDC state transitions: task initiation ('start'), plan linting ('lint'), and task closure ('close').

---
### A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.

**Rules:**

- The `protocols/` directory and all its contents (`.md`, `.json` files) MUST be treated as functional source code. Changes to these files directly alter the agent's operational capabilities and governing rules.
- The agent's execution environment provides a set of built-in tools (e.g., `read_file`, `delete_file`, `pre_commit_instructions`). The implementation of these tools does not reside within the repository. A protocol change that adds a built-in tool to the `associated_tools` list is a valid and complete functional change.
- A change is considered 'functional' if it correctly modifies the agent's operational rules or capabilities, as defined by the combination of Python source code and the protocol source files in `protocols/`.

---
### Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission.

**Rules:**

- Before submitting changes, the agent MUST execute the `pre_commit_instructions` tool to receive the required sequence of validation steps (e.g., running tests, requesting code review).

---
### A protocol for the Context-Sensitive Development Cycle (CSDC), which introduces development models based on logical constraints.

**Rules:**

- The `csdc_cli.py` tool must be used to validate plans under the CSDC. This tool enforces model-specific constraints (A or B) and complexity requirements (P or EXP).
- Model A permits `define_set_of_names` but forbids `define_diagonalization_function`.
- Model B permits `define_diagonalization_function` but forbids `define_set_of_names`.

---
### A protocol for conducting systematic research using the integrated research toolchain.

**Rules:**

- For all complex research tasks, the `plan_deep_research` tool MUST be used to generate a plan, and the `execute_research_protocol` tool MUST be used for data gathering. This ensures a systematic and auditable research process.

---
### Ensures all development processes are formally decidable and computationally tractable.

**Rules:**

- The agent's planning and execution language is, by design, not Turing-complete. This is a fundamental constraint to guarantee that all processes will terminate.
- The agent MUST NOT generate plans that involve recursion or self-invocation. A plan cannot trigger another FDC or a sub-plan, with the sole exception of the 'Deep Research Cycle'.
- All plans must be valid strings in the language defined by the tooling/fdc_fsm.json Finite State Machine.

---
### A protocol for executing Aura scripts, enabling a more expressive and powerful planning and automation language for the agent.

**Rules:**

- The `aura_executor.py` tool should be used to execute .aura script files. This tool provides the bridge between the agent's master control loop and the Aura language interpreter.

---
### Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.

**Rules:**

- The AORP cascade is the mandatory entry point to every FDC.
- The FDC is a Finite State Machine (FSM) formally defined in `tooling/fdc_fsm.json`. Plans must be valid strings in the language defined by this FSM.
- Phase 1 (Deconstruction & Contextualization): The agent must ingest the task, query historical logs, identify entities using the symbol map, and analyze impact using the dependency graph.
- Phase 2 (Planning & Self-Correction): The agent must generate a granular plan, lint it using the FDC toolchain, cite evidence for its steps, and perform a critical review.
- Phase 3 (Execution & Structured Logging): The agent must execute the validated plan and log every action according to the `LOGGING_SCHEMA.md`.
- Phase 4 (Pre-Submission Post-Mortem): The agent must formally close the task using the `close` command and complete the generated post-mortem report.

---
### The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).

**Rules:**

- Upon receiving a new task, the agent's first action MUST be to programmatically execute the FDC 'start' command to formally initiate the task and run the AORP orientation cascade.

---
### A meta-protocol to ensure all autonomous actions, especially self-modification, are strategically sound and easily reviewable by humans.

**Rules:**

- All self-improvement and speculative execution tasks must generate a formal review document.
- The review document must be a markdown file located in the `reviews/` directory, named after the proposal or task.
- The review document must contain sections for 'Summary', 'Impact Analysis', and 'Verification Plan'.

---