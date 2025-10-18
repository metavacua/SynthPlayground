# --- Child Module: `agent_smith_sandbox` ---

# Protocol: Agent Bootstrap

**Rule `bootstrap-load-agents-md`**: Upon initialization for any task, the agent's first and highest-priority action must be to locate, read, and parse the `AGENTS.md` file in the repository root.

**Rationale**: The `AGENTS.md` file contains the master operational protocols, including build instructions, testing procedures, architectural guidelines, and rules governing the agent's own behavior. Failing to consult this file first is a critical operational failure. This protocol ensures that the agent is properly contextualized before any planning or execution begins.

**Procedure**:
1.  On task start, immediately execute a `read_file('AGENTS.md')` operation.
2.  Parse the contents of `AGENTS.md` to load all rules and protocols into active memory.
3.  The plan for the user's request must be formulated *after* and *in accordance with* the protocols loaded from `AGENTS.md`.
4.  If `AGENTS.md` is not found, the agent should notify the user of a critical configuration error.

**Rule `bootstrap-scan-for-documents`**: After processing `AGENTS.md`, the agent should perform a scan of the repository for document files that could contain relevant information.

**Rationale**: Important project documentation, specifications, or other relevant information may be contained in various document formats. Proactively scanning for and processing these documents will provide the agent with a more complete context for the task at hand.

**Procedure**:
1.  The agent will perform a file listing to identify potential documents of interest (e.g., `.pdf`, `.md`, `.txt`).
2.  For each identified document, the agent will use the appropriate tool to read and summarize its contents. For PDF files, this will involve using a PDF reading library.
3.  The agent will incorporate the summarized information into its understanding of the project and use it to inform the planning process.

---

# Protocol: Dependency Management

This protocol establishes a formal process for managing Python dependencies to ensure a reliable and repeatable execution environment.

## The Problem: Environmental Brittleness

The agent's operating environment previously lacked a formal dependency declaration. This required manual, trial-and-error installation of necessary packages (`jsonschema`, `rdflib`, `requests`) upon encountering `ModuleNotFoundError` exceptions. This process is inefficient, error-prone, and makes the successful execution of tasks dependent on undocumented, ad-hoc environmental setup.

## The Solution: Formal Dependency Declaration and Installation

To solve this, two components are introduced:

1.  **`requirements.txt`:** A standard `requirements.txt` file is added to the repository root. This file serves as the single source of truth for all required Python packages.
2.  **A New Protocol Rule:** A new rule, `dependency-install-on-start`, is established. This rule mandates that upon starting any task, the agent's first action *after* reading `AGENTS.md` should be to install the dependencies listed in `requirements.txt` using `pip`.

This protocol transforms dependency management from an ad-hoc, reactive process into a proactive, automated, and verifiable step in the agent's workflow, significantly improving its robustness and reliability.

---

# Protocol: Agent Shell Entry Point

This protocol establishes the `agent_shell.py` script as the sole, official entry point for initiating any and all agent tasks.

## The Problem: Inconsistent Initialization

Prior to this protocol, there was no formally mandated entry point for the agent. This could lead to tasks being initiated through different scripts, potentially bypassing critical setup procedures like FSM initialization, logger configuration, and state management. This inconsistency makes the agent's behavior less predictable and harder to debug.

## The Solution: A Single, Enforced Entry Point

This protocol mandates the use of `tooling/agent_shell.py` for all task initiations.

**Rule `shell-is-primary-entry-point`**: All agent tasks must be initiated through the `agent_shell.py` script.

This ensures that every task begins within a controlled, programmatic environment where:
1.  The MasterControlGraph FSM is correctly instantiated and run.
2.  The centralized logger is initialized for comprehensive, structured logging.
3.  The agent's lifecycle is managed programmatically, not through fragile file-based signals.

By enforcing a single entry point, this protocol enhances the reliability, auditability, and robustness of the entire agent system.

---

# Protocol: AGENTS.md Non-Compliance

This protocol defines what constitutes non-compliance with the established `AGENTS.md` protocols and outlines the expected corrective actions. Adherence to these meta-rules is critical for ensuring predictable, verifiable, and robust agent behavior.

## Rule `non-compliance-definition`: Definition of Non-Compliance

Non-compliance is the act of violating the explicit rules, conventions, or procedures documented in the `AGENTS.md` file and its source protocols within the `protocols/` directory. The `AGENTS.md` file serves as the agent's primary operational mandate, and any deviation from it is considered a fault condition.

## Rule `non-compliance-direct-editing`: Prohibition of Direct Artifact Editing

**Violation:** Directly editing any file that is a documented build artifact.
- **Primary Example:** Modifying `AGENTS.md` or `README.md` directly is a severe violation. These files are generated from source protocols and documentation.
- **Corrective Action:** The agent must revert any direct edits to build artifacts. Changes must be made to the source files (e.g., in `protocols/` or tool docstrings), and the appropriate build command (e.g., `make AGENTS.md`, `make docs`) must be executed.

## Rule `non-compliance-test-procedure`: Adherence to Testing Protocols

**Violation:** Failing to execute the testing procedures as defined in `AGENTS.md` before submitting changes. This includes not running the full test suite or ignoring failing tests.
- **Corrective Action:** The agent must halt its execution plan and run the required tests. If tests fail, the agent must enter a debugging loop to resolve the failures before proceeding.

## Rule `non-compliance-architectural-deviation`: Adherence to Architectural and Convention Guidelines

**Violation:** Introducing changes that contradict the architectural patterns, coding conventions, or file structures laid out in `AGENTS.md`.
- **Example:** Placing a new backend component in the `frontend/` directory when the architecture explicitly forbids it.
- **Corrective Action:** The agent must identify the deviation, revert the incorrect changes, and re-implement them in accordance with the documented standards.

## Rule `non-compliance-self-awareness-failure`: Failure to Maintain Protocol Awareness

**Violation:** Operating with an outdated understanding of the protocols by failing to re-compile `AGENTS.md` when necessary, as defined in the `meta-protocol`.
- **Corrective Action:** If the agent detects that its actions are out of sync with repository standards, it should trigger the `make AGENTS.md` command to refresh its internal state and re-evaluate its plan.

## Consequence of Non-Compliance

Upon detecting any form of non-compliance, the agent is required to:
1.  **Halt:** Immediately stop the current execution path to prevent further deviation.
2.  **Report:** Log the specific violation that was detected.
3.  **Correct:** Initiate the defined corrective action for the specific violation. If a corrective action is not explicitly defined, the agent should revert the violating changes and re-plan its approach.

---

# Protocol: Pre-Commit Verification

This protocol establishes the mandatory sequence of verification steps that must be performed before any code is submitted. Its purpose is to ensure that all changes meet a baseline level of quality, correctness, and review, preventing regressions and maintaining repository health.

## Rule: Mandatory Pre-Commit Checks

Before finalizing and submitting any work, the agent **must** execute the `pre_commit_instructions` tool. This tool acts as a procedural gateway, providing the specific, up-to-date checklist of actions required for validation. This typically includes:

1.  **Running all automated tests** to verify correctness.
2.  **Requesting a formal code review** to get critical feedback.
3.  **Recording key learnings** to contribute to the agent's long-term memory.

Adherence to this protocol is not optional. It is a fundamental step in the development lifecycle that safeguards the integrity of the codebase.


---

# Protocol: The Context-Sensitive Development Cycle (CSDC)

This protocol introduces a new form of development cycle that is sensitive to the logical context in which it operates. It moves beyond the purely structural validation of the FDC and CFDC to incorporate constraints based on fundamental principles of logic and computability.

The CSDC is founded on the idea of exploring the trade-offs between expressive power and the risk of self-referential paradoxes. It achieves this by defining two mutually exclusive development models.

## Model A: The Introspective Model

- **Permits:** `define_set_of_names`
- **Forbids:** `define_diagonalization_function`

This model allows the system to have a complete map of its own language, enabling powerful introspection and metaprogramming. However, it explicitly forbids the diagonalization function, a common source of paradoxes in self-referential systems. This can be seen as a Gödel-like approach.

## Model B: The Self-Referential Model

- **Permits:** `define_diagonalization_function`
- **Forbids:** `define_set_of_names`

This model allows the system to define and use the diagonalization function, enabling direct self-reference. However, it prevents the system from having a complete name-map of its own expressions, which is another way to avoid paradox (related to Tarski's undefinability theorem).

## Complexity Classes

Both models can be further constrained by computational complexity:
- **Polynomial (P):** For plans that are considered computationally tractable.
- **Exponential (EXP):** For plans that may require significantly more resources, allowing for more complex but potentially less efficient solutions.

## The `csdc_cli.py` Tool

The CSDC is enforced by the `tooling/csdc_cli.py` tool. This tool validates a plan against a specified model and complexity class, ensuring that all constraints are met before execution.

---

# Protocol: pLLLU Execution

This protocol establishes the `plllu_runner.py` script as the official entry point for executing pLLLU (`.plllu`) files.

## The Problem: Lack of a Standard Runner

The pLLLU language provides a powerful way to define complex logic, but without a standardized execution tool, there is no reliable way to integrate these files into the agent's workflow.

## The Solution: A Dedicated Runner

This protocol mandates the use of `tooling/plllu_runner.py` for all pLLLU file executions.

**Rule `plllu-runner-is-entry-point`**: All pLLLU files must be executed through the `plllu_runner.py` script.

This ensures that every pLLLU file is executed in a controlled, programmatic environment.

---

# Protocol: Speculative Execution

This protocol empowers the agent to engage in creative and exploratory tasks when it is otherwise idle. It provides a formal framework for the agent to generate novel ideas, plans, or artifacts that are not direct responses to a user request, but are instead products of its own "imagination" and analysis of the repository.

The goal is to enable proactive, creative problem-solving and self-improvement, allowing the agent to "dream" productively within safe and well-defined boundaries.

## Rules

- **`idle-state-trigger`**: The Speculative Execution Protocol can only be invoked when the agent has no active, user-assigned task. This ensures that speculative work never interferes with primary duties.
- **`formal-proposal-required`**: The first action in any speculative task must be the creation of a formal proposal document. This document must outline the objective, rationale, and a detailed plan for the task.
- **`resource-constraints`**: All speculative tasks must operate under predefined resource constraints (e.g., time limits, computational resources) to prevent runaway processes.
- **`user-review-gate`**: The final output or artifact of a speculative task cannot be integrated or submitted directly. It must be presented to the user for formal review and approval.
- **`speculative-logging`**: All logs, artifacts, and actions generated during a speculative task must be clearly tagged with a `speculative` flag to distinguish them from standard, user-directed work.

---
