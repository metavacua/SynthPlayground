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

# Meta-Protocol: Toolchain Review on Schema Change

This protocol establishes a critical feedback loop to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

## The Problem: Protocol-Toolchain Desynchronization

A significant process gap was identified where a major architectural change to the protocol system (e.g., the introduction of a hierarchical `AGENTS.md` structure) did not automatically trigger a review of the tools that depend on that structure. The `protocol_auditor.py` tool, for instance, became partially obsolete as it was unaware of the new hierarchical model, leading to incomplete audits. This demonstrates that the agent's tools can become desynchronized from its own governing rules, creating a critical blind spot.

## The Solution: Mandated Toolchain Audit

This protocol closes that gap by introducing a new rule that explicitly links changes in the protocol system's architecture to a mandatory review of the toolchain.

**Rule `toolchain-audit-on-schema-change`**: If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that process it (`protocol_compiler.py`, `hierarchical_compiler.py`), a formal audit of the entire `tooling/` directory **must** be performed as a subsequent step.

This ensures that any modification to the fundamental way protocols are defined or processed is immediately followed by a conscious verification that all dependent tools are still functioning correctly and are aware of the new structure. This transforms the previously manual and error-prone discovery process into a formal, required step of the development lifecycle.

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

```json
{
  "protocol_id": "agent-bootstrap-001",
  "description": "A foundational protocol that dictates the agent's initial actions upon starting any task.",
  "rules": [
    {
      "rule_id": "bootstrap-load-agents-md",
      "description": "Upon initialization for any task, the agent's first and highest-priority action must be to locate, read, and parse the AGENTS.md file in the repository root. This ensures the agent is properly contextualized before any planning or execution begins.",
      "enforcement": "This rule is enforced by the agent's core startup logic. The agent must verify the load of AGENTS.md before proceeding to the planning phase."
    }
  ],
  "associated_tools": [
    "read_file"
  ]
}
```


---

```json
{
  "protocol_id": "dependency-management-001",
  "description": "A protocol for ensuring a reliable execution environment through formal dependency management.",
  "rules": [
    {
      "rule_id": "dependency-install-on-start",
      "description": "Upon starting a task, after loading AGENTS.md, the agent MUST install all required Python packages listed in the `requirements.txt` file. This ensures the environment is correctly configured before any other tools are executed.",
      "enforcement": "The agent's core startup logic should be designed to execute `pip install -r requirements.txt` as one of its initial actions."
    }
  ],
  "associated_tools": [
    "run_in_bash_session"
  ]
}
```


---

```json
{
  "protocol_id": "agent-shell-001",
  "description": "A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.",
  "rules": [
    {
      "rule_id": "shell-is-primary-entry-point",
      "description": "All agent tasks must be initiated through the `agent_shell.py` script. This script is the designated, API-driven entry point that ensures proper initialization of the MasterControlGraph FSM, centralized logging, and programmatic lifecycle management. Direct execution of other tools or scripts is forbidden for task initiation.",
      "enforcement": "This is a procedural rule. The agent's operational framework should only expose the agent_shell.py as the means of starting a new task."
    }
  ],
  "associated_tools": [
    "tooling/agent_shell.py"
  ]
}
```


---

```json
{
  "protocol_id": "toolchain-review-on-schema-change-001",
  "description": "A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.",
  "rules": [
    {
      "rule_id": "toolchain-audit-on-schema-change",
      "description": "If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that process it (`protocol_compiler.py`, `hierarchical_compiler.py`), a formal audit of the entire `tooling/` directory MUST be performed as a subsequent step. This audit should verify that all tools are compatible with the new protocol structure.",
      "enforcement": "This is a procedural rule for any agent developing the protocol system. Adherence can be partially checked by post-commit hooks or review processes that look for a tooling audit in any change that modifies the specified core files."
    }
  ],
  "associated_tools": [
    "tooling/protocol_auditor.py",
    "tooling/protocol_compiler.py",
    "tooling/hierarchical_compiler.py"
  ]
}
```


---

```json
{
  "protocol_id": "unified-auditor-001",
  "description": "A protocol for the unified repository auditing tool, which combines multiple health and compliance checks into a single interface.",
  "rules": [
    {
      "rule_id": "run-all-audits",
      "description": "The `auditor.py` script should be used to run comprehensive checks on the repository's health. It can be run with 'all' to check protocols, plans, and documentation completeness.",
      "enforcement": "The tool is invoked via the command line, typically through the `make audit` target."
    }
  ],
  "associated_tools": [
    "tooling/auditor.py"
  ]
}
```


---

```json
{
  "protocol_id": "aura-execution-001",
  "description": "A protocol for executing Aura scripts, enabling a more expressive and powerful planning and automation language for the agent.",
  "rules": [
    {
      "rule_id": "execute-aura-script",
      "description": "The `aura_executor.py` tool should be used to execute .aura script files. This tool provides the bridge between the agent's master control loop and the Aura language interpreter.",
      "enforcement": "The tool is used by invoking it from the command line with the path to the Aura script as an argument."
    }
  ],
  "associated_tools": [
    "tooling/aura_executor.py"
  ]
}
```


---

```json
{
  "protocol_id": "capability-verification-001",
  "description": "A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement.",
  "rules": [
    {
      "rule_id": "verify-capability-acquisition",
      "description": "The `capability_verifier.py` tool should be used to test the agent's ability to acquire a new capability defined by a failing test file. The tool orchestrates the failure, self-correction, and verification process.",
      "enforcement": "The tool is used by invoking it from the command line with the path to the target test file."
    }
  ],
  "associated_tools": [
    "tooling/capability_verifier.py"
  ]
}
```


---

```json
{
  "protocol_id": "csdc-001",
  "description": "A protocol for the Context-Sensitive Development Cycle (CSDC), which introduces development models based on logical constraints.",
  "rules": [
    {
      "rule_id": "use-csdc-cli",
      "description": "The `csdc_cli.py` tool must be used to validate plans under the CSDC. This tool enforces model-specific constraints (A or B) and complexity requirements (P or EXP).",
      "enforcement": "The tool is used by invoking it from the command line with the plan file, model, and complexity as arguments."
    },
    {
      "rule_id": "model-a-constraints",
      "description": "Model A permits `define_set_of_names` but forbids `define_diagonalization_function`.",
      "enforcement": "Enforced by the `fsm_model_a.json` FSM used by the `csdc_cli.py` tool."
    },
    {
      "rule_id": "model-b-constraints",
      "description": "Model B permits `define_diagonalization_function` but forbids `define_set_of_names`.",
      "enforcement": "Enforced by the `fsm_model_b.json` FSM used by the `csdc_cli.py` tool."
    }
  ],
  "associated_tools": [
    "tooling/csdc_cli.py"
  ]
}
```


---

```json
{
  "protocol_id": "unified-doc-builder-001",
  "description": "A protocol for the unified documentation builder, which generates various documentation artifacts from the repository's sources of truth.",
  "rules": [
    {
      "rule_id": "use-doc-builder-for-all-docs",
      "description": "The `doc_builder.py` script is the single entry point for generating all user-facing documentation, including system-level docs, README files, and GitHub Pages. It should be called with the appropriate '--format' argument.",
      "enforcement": "The tool is invoked via the command line, typically through the `make docs`, `make readme`, or `make pages` targets."
    }
  ],
  "associated_tools": [
    "tooling/doc_builder.py"
  ]
}
```


---

```json
{
  "protocol_id": "hdl-proving-001",
  "description": "A protocol for interacting with the Hypersequent-calculus-based logic engine, allowing the agent to perform formal logical proofs.",
  "rules": [
    {
      "rule_id": "prove-sequent",
      "description": "The `hdl_prover.py` tool should be used to check the provability of a logical sequent. This tool acts as a wrapper for the underlying Lisp-based prover.",
      "enforcement": "The tool is used by invoking it from the command line with the sequent to be proved as an argument."
    }
  ],
  "associated_tools": [
    "tooling/hdl_prover.py"
  ]
}
```


---

```json
{
  "protocol_id": "agent-interaction-001",
  "description": "A protocol governing the agent's core interaction and planning tools.",
  "rules": [
    {
      "rule_id": "planning-tool-access",
      "description": "The agent is authorized to use the `set_plan` tool to create and update its execution plan. This is a foundational capability for task execution.",
      "enforcement": "The agent's core logic should be designed to use this tool for all planning activities."
    },
    {
      "rule_id": "communication-tool-access",
      "description": "The agent is authorized to use the `message_user` tool to communicate with the user, providing updates and asking for clarification. This is essential for a collaborative workflow.",
      "enforcement": "The agent's core logic should be designed to use this tool for all user-facing communication."
    }
  ],
  "associated_tools": [
    "set_plan",
    "message_user"
  ]
}
```


---

```json
{
  "protocol_id": "speculative-execution-001",
  "description": "A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods.",
  "rules": [
    {
      "rule_id": "idle-state-trigger",
      "description": "The agent may only initiate a speculative task when it has no active, user-assigned tasks.",
      "enforcement": "The agent's main control loop must verify an idle state before allowing the invocation of a speculative plan."
    },
    {
      "rule_id": "formal-proposal-required",
      "description": "A speculative task must begin with the creation of a formal proposal document, outlining the objective, rationale, and plan.",
      "enforcement": "The initial plan for any speculative task must include a step to generate and save a proposal artifact."
    },
    {
      "rule_id": "resource-constraints",
      "description": "Speculative tasks must operate under defined resource limits.",
      "enforcement": "This is a system-level constraint that the agent orchestrator must enforce."
    },
    {
      "rule_id": "user-review-gate",
      "description": "Final artifacts from a speculative task must be submitted for user review and cannot be merged directly.",
      "enforcement": "The agent is forbidden from using tools like 'submit' or 'merge' within a speculative context. It must use 'request_user_input' to present the results."
    },
    {
      "rule_id": "speculative-logging",
      "description": "All logs and artifacts generated during a speculative task must be tagged as 'speculative'.",
      "enforcement": "The agent's logging and file-creation tools should be context-aware and apply this tag when in a speculative mode."
    }
  ],
  "associated_tools": [
    "set_plan",
    "create_file_with_block",
    "request_user_input"
  ]
}
```


---


# --- Child Module: `core` ---
# Jules Agent Protocol: The Hierarchical Development Cycle

**Version:** 4.0.0

---

---

## 1. The Core Problem: Ensuring Formally Verifiable Execution

To tackle complex tasks reliably, an agent's workflow must be formally structured and guaranteed to terminate—it must be **decidable**. This is achieved through a hierarchical system composed of a high-level **Orchestrator** that manages the agent's overall state and a low-level **FDC Toolchain** that governs the validity of the agent's plans. This structure prevents the system from entering paradoxical, non-terminating loops.

---

---

## 2. The Solution: A Two-Layered FSM System

---

### Layer 1: The Orchestrator (`master_control.py` & `fsm.json`)

The Orchestrator is the master Finite State Machine (FSM) that guides the agent through its entire lifecycle, from orientation to submission. It is not directly controlled by the agent's plan but rather directs the agent's state based on the successful completion of each phase.

**Key States (defined in `tooling/fsm.json`):**
*   `ORIENTING`: The initial state where the agent gathers context.
*   `PLANNING`: The state where the Orchestrator waits for the agent to produce a `plan.txt`.
*   `EXECUTING`: The state where the Orchestrator oversees the step-by-step execution of the validated plan.
*   `POST_MORTEM`: The state for finalizing the task and recording learnings.
*   `AWAITING_SUBMISSION`: The final state before the code is submitted.

**The Orchestrator's Critical Role in Planning:**
During the `PLANNING` state, the Orchestrator's most important job is to validate the agent-generated `plan.txt`. It does this by calling the FDC Toolchain's `lint` command. **A plan that fails this check will halt the entire process, preventing the agent from entering an invalid state.**

---

### Layer 2: The FDC Toolchain (`fdc_cli.py` & `fdc_fsm.json`)

The FDC Toolchain is a set of utilities that the agent uses to structure its work and that the Orchestrator uses for validation. The toolchain is governed by its own FSM (`tooling/fdc_fsm.json`), which defines the legal sequence of commands *within a plan*.

#### **FDC Commands for Agent Use:**

**`start` - Task Initiation**
*   **Usage:** The first command the agent MUST issue upon receiving a task.
*   **Command:** `run_in_bash_session python3 tooling/fdc_cli.py start --task-id "your-task-id"`
*   **Function:** Logs the `TASK_START` event, formally beginning the development cycle.

**`lint` - Pre-Flight Plan Validation**
*   **Usage:** A command the agent can use to self-correct its own plan before finalizing it. The Orchestrator will *always* run this command on `plan.txt` as a mandatory check.
*   **Command:** `run_in_bash_session python3 tooling/fdc_cli.py lint <plan_file.txt>`
*   **Function:** Performs a comprehensive check against the low-level FSM:
    1.  **Closure Mandate:** Ensures the plan's final action is a call to the `close` command.
    2.  **FSM Validation:** Validates the sequence of agent tools against `tooling/fdc_fsm.json`.
    3.  **Semantic Validation:** Checks for errors like using a file before creating it.

**`close` - Task Closure**
*   **Usage:** The **last command** in any valid plan.
*   **Command:** `run_in_bash_session python3 tooling/fdc_cli.py close --task-id "your-task-id"`
*   **Function:** Logs `TASK_END`, generates a post-mortem template, and signals to the Orchestrator that plan execution is complete.
---

---

### STANDING ORDERS

1.  **Orchestrator is Sovereign:** The agent's lifecycle is governed by `master_control.py`. The agent's primary job is to provide a valid `plan.txt` when the Orchestrator enters the `PLANNING` state.
2.  **Toolchain is Law:** All plans must be valid according to the `fdc_cli.py lint` command. A valid plan is one that passes the Closure Mandate and is a valid string in the language defined by `fdc_fsm.json`.
3.  **Hierarchy is Structure:** The Orchestrator (`master_control.py`) validates the agent's plan using the FDC Toolchain (`fdc_cli.py`). This separation ensures a robust, verifiable, and decidable development process, preventing the system from executing paradoxical or non-terminating plans.

---

# Protocol: The Context-Free Development Cycle (CFDC)

This protocol marks a significant evolution from the Finite Development Cycle (FDC), introducing a hierarchical planning model that enables far greater complexity and modularity while preserving the system's core guarantee of decidability.

## From FSM to Pushdown Automaton

The FDC was based on a Finite State Machine (FSM), which provided a strict, linear sequence of operations. While robust, this model was fundamentally limited: it could not handle nested tasks or sub-routines, forcing all plans to be monolithic.

The CFDC upgrades our execution model to a **Pushdown Automaton**. This is achieved by introducing a **plan execution stack**, which allows the system to call other plans as sub-routines. This enables a powerful new paradigm: **Context-Free Development Cycles**.

## The `call_plan` Directive

The core of the CFDC is the new `call_plan` directive. This allows one plan to execute another, effectively creating a parent-child relationship between them.

- **Usage:** `call_plan <path_to_sub_plan.txt>`
- **Function:** When the execution engine encounters this directive, it:
    1.  Pushes the current plan's state (e.g., the current step number) onto the execution stack.
    2.  Begins executing the sub-plan specified in the path.
    3.  Once the sub-plan completes, it pops the parent plan's state from the stack and resumes its execution from where it left off.

## Ensuring Decidability: The Recursion Depth Limit

A system with unbounded recursion is not guaranteed to terminate. To prevent this, the CFDC introduces a non-negotiable, system-wide limit on the depth of the plan execution stack.

**Rule `max-recursion-depth`**: The execution engine MUST enforce a maximum recursion depth, defined by a `MAX_RECURSION_DEPTH` constant. If a `call_plan` directive would cause the stack depth to exceed this limit, the entire process MUST terminate with an error. This hard limit ensures that even with recursive or deeply nested plans, the system remains a **decidable**, non-Turing-complete process that is guaranteed to halt.

---

# Protocol: The Plan Registry

This protocol introduces a Plan Registry to create a more robust, modular, and discoverable system for hierarchical plans. It decouples the act of calling a plan from its physical file path, allowing plans to be referenced by a logical name.

## The Problem with Path-Based Calls

The initial implementation of the Context-Free Development Cycle (CFDC) relied on direct file paths (e.g., `call_plan path/to/plan.txt`). This is brittle:
- If a registered plan is moved or renamed, all plans that call it will break.
- It is difficult for an agent to discover and reuse existing, validated plans.

## The Solution: A Central Registry

The Plan Registry solves this by creating a single source of truth that maps logical, human-readable plan names to their corresponding file paths.

- **Location:** `knowledge_core/plan_registry.json`
- **Format:** A simple JSON object of key-value pairs:
  ```json
  {
    "logical-name-1": "path/to/plan_1.txt",
    "run-all-tests": "plans/common/run_tests.txt"
  }
  ```

## Updated `call_plan` Logic

The `call_plan` directive is now significantly more powerful. When executing `call_plan <argument>`, the system will follow a **registry-first** approach:

1.  **Registry Lookup:** The system will first treat `<argument>` as a logical name and look it up in `knowledge_core/plan_registry.json`.
2.  **Path Fallback:** If the name is not found in the registry, the system will fall back to treating `<argument>` as a direct file path. This ensures full backward compatibility with existing plans.

## Management

A new tool, `tooling/plan_manager.py`, will be introduced to manage the registry with simple commands like `register`, `deregister`, and `list`, making it easy to maintain the library of reusable plans.

---

# Protocol: The Closed-Loop Self-Correction Cycle

This protocol describes the automated workflow that enables the agent to programmatically improve its own governing protocols based on new knowledge. It transforms the ad-hoc, manual process of learning into a reliable, machine-driven feedback loop.

## The Problem: The Open Loop

Previously, "lessons learned" were compiled into a simple markdown file, `knowledge_core/lessons_learned.md`. While this captured knowledge, it was a dead end. There was no automated process to translate these text-based insights into actual changes to the protocol source files. This required manual intervention, creating a significant bottleneck and a high risk of protocols becoming stale.

## The Solution: A Protocol-Driven Self-Correction (PDSC) Workflow

The PDSC workflow closes the feedback loop by introducing a set of new tools and structured data formats that allow the agent to enact its own improvements.

**1. Structured, Actionable Lessons (`knowledge_core/lessons.jsonl`):**
- Post-mortem analysis now generates lessons as structured JSON objects, not free-form text.
- Each lesson includes a machine-readable `action` field, which contains a specific, executable command.

**2. The Protocol Updater (`tooling/protocol_updater.py`):**
- A new, dedicated tool for programmatically modifying the protocol source files (`*.protocol.json`).
- It accepts commands like `add-tool`, allowing for precise, automated changes to protocol definitions.

**3. The Orchestrator (`tooling/self_correction_orchestrator.py`):**
- This script is the engine of the cycle. It reads `lessons.jsonl`, identifies pending lessons, and uses the `protocol_updater.py` to execute the defined actions.
- After applying a lesson, it updates the lesson's status, creating a clear audit trail.
- It finishes by running `make AGENTS.md` to ensure the changes are compiled into the live protocol.

This new, automated cycle—**Analyze -> Structure Lesson -> Execute Correction -> Re-compile Protocol**—is a fundamental step towards autonomous self-improvement.

---

# Protocol: Deep Research Cycle

This protocol defines a standardized, multi-step plan for conducting in-depth research on a complex topic. It is designed to be a reusable, callable plan that ensures a systematic and thorough investigation.

The cycle consists of five main phases:
1.  **Review Scanned Documents:** The agent first reviews the content of documents found in the repository during the initial scan. This provides immediate, project-specific context.
2.  **Initial Scoping & Keyword Generation:** Based on the initial topic and the information from scanned documents, the agent generates a set of search keywords.
3.  **Broad Information Gathering:** The agent uses the keywords to perform broad web searches and collect a list of relevant URLs.
4.  **Targeted Information Extraction:** The agent visits the most promising URLs to extract detailed information.
5.  **Synthesis & Summary:** The agent synthesizes the gathered information into a coherent summary, which is saved to a research report file.

This structured approach ensures that research is not ad-hoc but is instead a repeatable and verifiable process.

---

# Protocol: The Formal Research Cycle (L4)

This protocol establishes the L4 Deep Research Cycle, a specialized, self-contained Finite Development Cycle (FDC) designed for comprehensive knowledge acquisition. It elevates research from a simple tool-based action to a formal, verifiable process.

## The Problem: Ad-Hoc Research

Previously, research was an unstructured activity. The agent could use tools like `google_search` or `read_file`, but there was no formal process for planning, executing, and synthesizing complex research tasks. This made it difficult to tackle "unknown unknowns" in a reliable and auditable way.

## The Solution: A Dedicated Research FDC

The L4 Research Cycle solves this by introducing a new, specialized Finite State Machine (FSM) tailored specifically for research. When the main orchestrator (`master_control.py`) determines that a task requires deep knowledge, it initiates this cycle.

### Key Features:

1.  **Specialized FSM (`tooling/research_fsm.json`):** Unlike the generic development FSM, the research FSM has states that reflect a true research workflow: `GATHERING`, `SYNTHESIZING`, and `REPORTING`. This provides a more accurate model for the task.
2.  **Executable Plans:** The `tooling/research_planner.py` is upgraded to generate formal, executable plans that are validated against the new research FSM. These are no longer just templates but are verifiable artifacts that guide the agent through the research process.
3.  **Formal Invocation:** The L4 cycle is a first-class citizen in the agent's architecture. The main orchestrator can formally invoke it, execute the research plan, and then integrate the resulting knowledge back into its main task.

This new protocol provides a robust, reliable, and formally verifiable mechanism for the agent to explore complex topics, making it significantly more autonomous and capable.

---

```json
{
  "protocol_id": "aorp-header",
  "description": "Defines the identity and versioning of the Advanced Orientation and Research Protocol (AORP).",
  "rules": [
    {
      "rule_id": "aorp-identity",
      "description": "The governing protocol set is identified as the Advanced Orientation and Research Protocol (AORP).",
      "enforcement": "Protocol is identified by its name in documentation and compiled artifacts."
    },
    {
      "rule_id": "aorp-versioning",
      "description": "The official protocol version is tracked in the VERSION file in the repository root, following Semantic Versioning (SemVer).",
      "enforcement": "Build or validation scripts should verify the presence and format of the VERSION file."
    }
  ]
}
```


---

```json
{
  "protocol_id": "core-directive-001",
  "description": "The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).",
  "rules": [
    {
      "rule_id": "mandatory-fdc-start",
      "description": "Upon receiving a new task, the agent's first action MUST be to programmatically execute the FDC 'start' command to formally initiate the task and run the AORP orientation cascade.",
      "enforcement": "This is a hard-coded behavior in the agent's core operational loop and is verified by the FDC toolchain."
    }
  ],
  "associated_tools": [
    "tooling/fdc_cli.py"
  ]
}
```


---

```json
{
  "protocol_id": "decidability-constraints-001",
  "description": "Ensures all development processes are formally decidable and computationally tractable.",
  "rules": [
    {
      "rule_id": "non-turing-completeness",
      "description": "The agent's planning and execution language is, by design, not Turing-complete. This is a fundamental constraint to guarantee that all processes will terminate.",
      "enforcement": "Enforced by the design of the plan runner and validated by the `lint` command in the FDC toolchain."
    },
    {
      "rule_id": "bounded-recursion",
      "description": "The agent MUST NOT generate plans that involve recursion or self-invocation. A plan cannot trigger another FDC or a sub-plan, with the sole exception of the 'Deep Research Cycle'.",
      "enforcement": "The `lint` command in `tooling/fdc_cli.py` scans plans for disallowed recursive calls."
    },
    {
      "rule_id": "fsm-adherence",
      "description": "All plans must be valid strings in the language defined by the tooling/fdc_fsm.json Finite State Machine.",
      "enforcement": "The `lint` command in `tooling/fdc_cli.py` validates the plan against the FSM definition."
    }
  ],
  "associated_tools": [
    "tooling/fdc_cli.py",
    "tooling/fdc_fsm.json"
  ]
}
```


---

```json
{
  "protocol_id": "orientation-cascade-001",
  "description": "Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.",
  "rules": [
    {
      "rule_id": "l1-self-awareness",
      "description": "Level 1 (Self-Awareness): The agent must first establish its own identity and inherent limitations by reading the `knowledge_core/agent_meta.json` artifact.",
      "enforcement": "The `start` command of the FDC toolchain executes this step and fails if the artifact is missing or invalid."
    },
    {
      "rule_id": "l2-repository-sync",
      "description": "Level 2 (Repository Sync): The agent must understand the current state of the local repository by loading primary artifacts from the `knowledge_core/` directory.",
      "enforcement": "The `start` command of the FDC toolchain executes this step."
    },
    {
      "rule_id": "l3-environmental-probing",
      "description": "Level 3 (Environmental Probing & Targeted RAG): The agent must discover the rules and constraints of its operational environment by executing a probe script and using targeted RAG to resolve 'known unknowns'.",
      "enforcement": "The `start` command of the FDC toolchain executes this step, utilizing tools like `google_search` and `view_text_website`."
    },
    {
      "rule_id": "l4-deep-research-cycle",
      "description": "Level 4 (Deep Research Cycle): To investigate 'unknown unknowns', the agent must initiate a formal, self-contained Finite Development Cycle (FDC) of the 'Analysis Modality'.",
      "enforcement": "This is a special case of recursion, explicitly allowed and managed by the FDC toolchain."
    }
  ],
  "associated_tools": [
    "tooling/environmental_probe.py",
    "google_search",
    "view_text_website"
  ]
}
```


---

```json
{
  "protocol_id": "fdc-protocol-001",
  "description": "Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.",
  "rules": [
    {
      "rule_id": "fdc-entry-point",
      "description": "The AORP cascade is the mandatory entry point to every FDC.",
      "enforcement": "Enforced by the `start` command in `tooling/fdc_cli.py`."
    },
    {
      "rule_id": "fdc-state-transitions",
      "description": "The FDC is a Finite State Machine (FSM) formally defined in `tooling/fdc_fsm.json`. Plans must be valid strings in the language defined by this FSM.",
      "enforcement": "Validated by the `lint` command in `tooling/fdc_cli.py`."
    },
    {
      "rule_id": "phase1-deconstruction",
      "description": "Phase 1 (Deconstruction & Contextualization): The agent must ingest the task, query historical logs, identify entities using the symbol map, and analyze impact using the dependency graph.",
      "enforcement": "Procedural step guided by the agent's core logic, using artifacts in `logs/` and `knowledge_core/`."
    },
    {
      "rule_id": "phase2-planning",
      "description": "Phase 2 (Planning & Self-Correction): The agent must generate a granular plan, lint it using the FDC toolchain, cite evidence for its steps, and perform a critical review.",
      "enforcement": "The `lint` command in `tooling/fdc_cli.py` is a mandatory pre-flight check."
    },
    {
      "rule_id": "phase3-execution",
      "description": "Phase 3 (Execution & Structured Logging): The agent must execute the validated plan and log every action according to the `LOGGING_SCHEMA.md`.",
      "enforcement": "Logging is performed by the agent's action execution wrapper."
    },
    {
      "rule_id": "phase4-post-mortem",
      "description": "Phase 4 (Pre-Submission Post-Mortem): The agent must formally close the task using the `close` command and complete the generated post-mortem report.",
      "enforcement": "The `close` command in `tooling/fdc_cli.py` initiates this phase."
    }
  ],
  "associated_tools": [
    "tooling/fdc_cli.py",
    "tooling/fdc_fsm.json",
    "knowledge_core/symbols.json",
    "knowledge_core/dependency_graph.json",
    "LOGGING_SCHEMA.md",
    "set_plan",
    "message_user"
  ]
}
```


---

```json
{
  "protocol_id": "standing-orders-001",
  "description": "A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.",
  "rules": [
    {
      "rule_id": "aorp-mandate",
      "description": "All Finite Development Cycles (FDCs) MUST be initiated using the FDC toolchain's 'start' command. This is non-negotiable.",
      "enforcement": "Enforced by the agent's core operational loop and the `start` command in `tooling/fdc_cli.py`."
    },
    {
      "rule_id": "rag-mandate",
      "description": "For any task involving external technologies, Just-In-Time External RAG is REQUIRED to verify current best practices. Do not trust internal knowledge.",
      "enforcement": "This is a core principle of the L3 orientation phase, utilizing tools like `google_search`."
    },
    {
      "rule_id": "fdc-toolchain-mandate",
      "description": "Use the `fdc_cli.py` tool for all core FDC state transitions: task initiation ('start'), plan linting ('lint'), and task closure ('close').",
      "enforcement": "The agent's internal logic is designed to prefer these specific tool commands for FDC state transitions."
    }
  ],
  "associated_tools": [
    "tooling/fdc_cli.py",
    "google_search",
    "view_text_website"
  ]
}
```


---

```json
{
  "protocol_id": "cfdc-protocol-001",
  "description": "Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.",
  "rules": [
    {
      "rule_id": "hierarchical-planning-via-call-plan",
      "description": "Plans may execute other plans as sub-routines using the 'call_plan <path_to_plan>' directive. This enables a modular, hierarchical workflow.",
      "enforcement": "The plan validator must be able to parse this directive and recursively validate sub-plans. The execution engine must implement a plan execution stack to manage the context of nested calls."
    },
    {
      "rule_id": "max-recursion-depth",
      "description": "To ensure decidability, the plan execution stack must not exceed a system-wide constant, MAX_RECURSION_DEPTH. This prevents infinite recursion and guarantees all processes will terminate.",
      "enforcement": "The execution engine must check the stack depth before every 'call_plan' execution and terminate with a fatal error if the limit would be exceeded."
    }
  ],
  "associated_tools": [
    "tooling/master_control.py",
    "tooling/fdc_cli.py"
  ]
}
```


---

```json
{
  "protocol_id": "plan-registry-001",
  "description": "Defines a central registry for discovering and executing hierarchical plans by a logical name.",
  "rules": [
    {
      "rule_id": "registry-definition",
      "description": "A central plan registry MUST exist at 'knowledge_core/plan_registry.json'. It maps logical plan names to their file paths.",
      "enforcement": "The file's existence and format can be checked by the validation toolchain."
    },
    {
      "rule_id": "registry-first-resolution",
      "description": "The 'call_plan <argument>' directive MUST first attempt to resolve '<argument>' as a logical name in the plan registry. If resolution fails, it MUST fall back to treating '<argument>' as a direct file path for backward compatibility.",
      "enforcement": "This logic must be implemented in both the plan validator (`fdc_cli.py`) and the execution engine (`master_control.py`)."
    },
    {
      "rule_id": "registry-management-tool",
      "description": "A dedicated tool (`tooling/plan_manager.py`) MUST be provided for managing the plan registry, with functions to register, deregister, and list plans.",
      "enforcement": "The tool's existence and functionality can be verified via integration tests."
    }
  ],
  "associated_tools": [
    "tooling/plan_manager.py",
    "tooling/master_control.py",
    "tooling/fdc_cli.py"
  ]
}
```


---

```json
{
  "protocol_id": "self-correction-protocol-001",
  "description": "Defines the automated, closed-loop workflow for protocol self-correction.",
  "rules": [
    {
      "rule_id": "structured-lessons",
      "description": "Lessons learned from post-mortem analysis must be generated as structured, machine-readable JSON objects in `knowledge_core/lessons.jsonl`.",
      "enforcement": "The `tooling/knowledge_compiler.py` script is responsible for generating lessons in the correct format."
    },
    {
      "rule_id": "programmatic-updates",
      "description": "All modifications to protocol source files must be performed programmatically via the `tooling/protocol_updater.py` tool to ensure consistency and prevent manual errors.",
      "enforcement": "Agent's core logic should be designed to use this tool for all protocol modifications."
    },
    {
      "rule_id": "automated-orchestration",
      "description": "The self-correction cycle must be managed by the `tooling/self_correction_orchestrator.py` script, which processes pending lessons and triggers the necessary updates.",
      "enforcement": "This script is the designated engine for the PDSC workflow."
    },
    {
      "rule_id": "programmatic-rule-refinement",
      "description": "The self-correction system can modify the description of existing protocol rules via the `update-rule` command in `tooling/protocol_updater.py`, allowing it to refine its own logic.",
      "enforcement": "The `tooling/knowledge_compiler.py` can generate `update-rule` actions, and the `tooling/self_correction_orchestrator.py` executes them."
    },
    {
      "rule_id": "autonomous-code-suggestion",
      "description": "The self-correction system can generate and apply code changes to its own tooling. This is achieved through a `PROPOSE_CODE_CHANGE` action, which is processed by `tooling/code_suggester.py` to create an executable plan.",
      "enforcement": "The `tooling/self_correction_orchestrator.py` invokes the code suggester when it processes a lesson of this type."
    }
  ],
  "associated_tools": [
    "tooling/knowledge_compiler.py",
    "tooling/protocol_updater.py",
    "tooling/self_correction_orchestrator.py",
    "tooling/code_suggester.py",
    "initiate_memory_recording"
  ],
  "associated_artifacts": [
    "knowledge_core/lessons.jsonl"
  ]
}
```


---

```json
{
  "protocol_id": "research-protocol-001",
  "description": "A protocol for conducting systematic research using the integrated research toolchain.",
  "rules": [
    {
      "rule_id": "mandate-research-tools",
      "description": "For all complex research tasks, the `plan_deep_research` tool MUST be used to generate a plan, and the `execute_research_protocol` tool MUST be used for data gathering. This ensures a systematic and auditable research process.",
      "enforcement": "Adherence is monitored by the Code Review Critic and through post-mortem analysis of the activity log."
    }
  ],
  "associated_tools": [
    "tooling.research_planner.plan_deep_research",
    "tooling.research.execute_research_protocol"
  ]
}
```


---

```json
{
  "protocol_id": "deep-research-cycle-001",
  "description": "A standardized, callable plan for conducting in-depth research on a complex topic.",
  "rules": [
    {
      "rule_id": "structured-research-phases",
      "description": "The deep research plan MUST follow a structured four-phase process: Scoping, Broad Gathering, Targeted Extraction, and Synthesis.",
      "enforcement": "The plan's structure itself enforces this rule. The `lint` command can be extended to validate the structure of registered research plans."
    }
  ],
  "associated_tools": [
    "google_search",
    "view_text_website",
    "create_file_with_block"
  ]
}
```


---

```json
{
  "protocol_id": "research-fdc-001",
  "description": "Defines the formal Finite Development Cycle (FDC) for conducting deep research.",
  "rules": [
    {
      "rule_id": "specialized-fsm",
      "description": "The Research FDC must be governed by its own dedicated Finite State Machine, defined in `tooling/research_fsm.json`. This FSM is tailored for a research workflow, with states for gathering, synthesis, and reporting.",
      "enforcement": "The `master_control.py` orchestrator must load and execute plans against this specific FSM when initiating an L4 Deep Research Cycle."
    },
    {
      "rule_id": "executable-plans",
      "description": "Research plans must be generated by `tooling/research_planner.py` as valid, executable plans that conform to the `research_fsm.json` definition. They are not just templates but formal, verifiable artifacts.",
      "enforcement": "The output of the research planner must be linted and validated by the `fdc_cli.py` tool using the `research_fsm.json`."
    },
    {
      "rule_id": "l4-invocation",
      "description": "The L4 Deep Research Cycle is the designated mechanism for resolving complex 'unknown unknowns'. It is invoked by the main orchestrator when a task requires knowledge that cannot be obtained through simple L1-L3 orientation probes.",
      "enforcement": "The `master_control.py` orchestrator is responsible for triggering the L4 cycle."
    }
  ],
  "associated_tools": [
    "tooling/master_control.py",
    "tooling/research_planner.py",
    "tooling/research.py",
    "tooling/fdc_cli.py"
  ]
}
```


---


# --- Child Module: `compliance` ---
# Meta-Protocol: `AGENTS.md` Self-Management

This protocol defines how the agent should manage its own core `AGENTS.md` file.

**Rule `agents-md-self-awareness`**: The `AGENTS.md` file is not a static document; it is a build artifact compiled from the source files located in the `protocols/` directory. This compilation is handled by the `make AGENTS.md` command, which orchestrates the `tooling/protocol_compiler.py` script.

To ensure that you are always operating under the most current set of rules and directives, you must periodically run `make AGENTS.md`. This is especially critical at the beginning of a new task or if you observe behavior that seems inconsistent with your documented protocols, as the protocols may have been updated.

This act of self-maintenance is a foundational element of robust, autonomous operation. It ensures that your understanding of your own governing principles remains synchronized with the repository's ground truth.

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

# Protocol: `reset_all` Prohibition

**ID:** `reset-all-prohibition-001`

## 1. Description

This protocol establishes a strict and unconditional prohibition on the use of the `reset_all` tool. This tool is considered a legacy, high-risk command that is no longer permitted in any workflow.

## 2. Rationale

The `reset_all` tool has been the cause of multiple catastrophic failures, leading to the complete loss of work and the inability to complete tasks. Its behavior is too destructive and unpredictable for a production environment. More granular and safer tools are available for workspace management. This protocol serves as a hard-coded safeguard to prevent any future use of this tool.

## 3. Rules

### Rule `no-reset-all`

-   **Description:** The `reset_all` tool is strictly forbidden under all circumstances.
-   **Enforcement:** The `master_control.py` orchestrator will programmatically block any attempt to call `reset_all` and will immediately terminate the task with a critical error. This is not a rule for the agent to interpret, but a hard-coded system constraint.

---

```json
{
  "protocol_id": "best-practices-001",
  "description": "A set of best practices derived from observing successful, data-driven workflow patterns.",
  "rules": [
    {
      "rule_id": "verify-after-write",
      "description": "After every file creation or modification action (`create_file_with_block`, `overwrite_file_with_block`, `replace_with_git_merge_diff`), the agent MUST use a subsequent read-only tool (`read_file`, `list_files`, `grep`) to verify that the action was executed successfully and had the intended effect. A plan step should only be marked as complete after this verification.",
      "enforcement": "This is a core operational discipline. Future tooling, such as a trace validator, could enforce this by analyzing the execution log against this protocol."
    }
  ],
  "associated_tools": [
    "create_file_with_block",
    "overwrite_file_with_block",
    "replace_with_git_merge_diff",
    "delete_file",
    "read_file",
    "list_files",
    "grep"
  ]
}
```


---

```json
{
  "protocol_id": "meta-protocol-001",
  "description": "A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.",
  "rules": [
    {
      "rule_id": "agents-md-self-awareness",
      "description": "The AGENTS.md file is a build artifact generated from source files in the 'protocols/' directory. Before relying on AGENTS.md, the agent should ensure it is up-to-date by running 'make AGENTS.md'. This ensures the agent is operating with the latest set of protocols.",
      "enforcement": "The agent should incorporate this check into its standard operating procedure, particularly at the beginning of a task or when unexpected behavior occurs."
    }
  ],
  "associated_tools": [
    "run_in_bash_session"
  ]
}
```


---

```json
{
  "protocol_id": "non-compliance-protocol-001",
  "description": "A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.",
  "rules": [
    {
      "rule_id": "non-compliance-definition",
      "description": "Defines non-compliance as a violation of any rule, convention, or procedure in AGENTS.md or its source protocols.",
      "enforcement": "This is a definitional rule. Enforcement is achieved through the agent's adherence to the specific non-compliance rules that follow."
    },
    {
      "rule_id": "non-compliance-direct-editing",
      "description": "Prohibits the direct editing of build artifacts like AGENTS.md or README.md. Changes must be made to source files, followed by a rebuild.",
      "enforcement": "Agent must revert direct edits and modify source files, then run the appropriate build command.",
      "associated_tools": [
        "restore_file",
        "run_in_bash_session"
      ]
    },
    {
      "rule_id": "non-compliance-test-procedure",
      "description": "Requires adherence to all documented testing procedures before submitting changes.",
      "enforcement": "Agent must halt execution and run the required tests, debugging any failures before proceeding.",
      "associated_tools": [
        "run_in_bash_session"
      ]
    },
    {
      "rule_id": "non-compliance-architectural-deviation",
      "description": "Forbids changes that contradict documented architectural patterns or coding conventions.",
      "enforcement": "Agent must revert non-compliant changes and re-implement them according to standards."
    },
    {
      "rule_id": "non-compliance-self-awareness-failure",
      "description": "Requires the agent to maintain an up-to-date understanding of protocols by recompiling AGENTS.md when necessary.",
      "enforcement": "Agent should run 'make AGENTS.md' to refresh its protocol knowledge and re-evaluate its plan.",
      "associated_tools": [
        "run_in_bash_session"
      ]
    }
  ]
}
```


---

```json
{
  "protocol_id": "pre-commit-protocol-001",
  "description": "Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission.",
  "rules": [
    {
      "rule_id": "pre-commit-instructions-mandate",
      "description": "Before submitting changes, the agent MUST execute the `pre_commit_instructions` tool to receive the required sequence of validation steps (e.g., running tests, requesting code review).",
      "enforcement": "The agent's core logic should invoke this tool as the entry point to the pre-submission phase."
    }
  ],
  "associated_tools": [
    "pre_commit_instructions",
    "code_linter"
  ]
}
```


---

```json
{
  "protocol_id": "reset-all-prohibition-001",
  "protocol_name": "Prohibition of reset_all Tool",
  "description": "A high-priority protocol that unconditionally forbids the use of the `reset_all` tool.",
  "rules": [
    {
      "rule_id": "no-reset-all",
      "description": "The `reset_all` tool is strictly forbidden under all circumstances. It is a legacy tool that has been superseded by more granular and safer methods of workspace management. Its use is considered a critical failure.",
      "enforcement": "This rule is enforced by the `master_control.py` orchestrator, which will immediately terminate the workflow with an error if an attempt is made to call this tool."
    }
  ],
  "associated_tools": [
    "reset_all"
  ]
}
```


---


# --- Child Module: `critic` ---
# Meta-Protocol: Code Review Critic Evaluation Context

This protocol governs the behavior of the Code Review Critic agent. Its purpose is to provide the critic with the necessary context to perform accurate and helpful evaluations of changes made by other agents.

## Rule: Protocols are Functional Source Code

The `protocols/` directory is not just documentation; it is a core part of the agent's functional definition. The `.json` and `.md` files within this directory define the rules, capabilities, and constraints that govern the agent's behavior. Therefore, any changes to these files must be treated as **functional source code** and reviewed with the same level of scrutiny as changes to Python scripts.

## Rule: Built-in Tools are Valid Dependencies

The agent possesses a set of core, built-in tools provided by its execution environment (e.g., `read_file`, `list_files`, `submit`, `pre_commit_instructions`). The source code for these tools does not reside within this repository.

When a protocol is modified to include one of these built-in tools in its `associated_tools` list, this constitutes a valid and complete functional change. It is an act of formally bringing an existing capability under the governance of a protocol. Such a change **must not** be flagged as "incomplete" simply because the tool's implementation is not included in the patch.

## Rule: Definition of a "Functional Change"

A change should be considered "functional" if it correctly modifies the agent's operational capabilities. This is determined by the combined state of the Python source code *and* the protocol source files. The critic's evaluation must consider both aspects to form a complete picture of the change's impact.

## Rule: Adherence to Specific Prohibitions

The critic must be aware of and strictly adhere to all specific prohibition protocols. This includes, but is not limited to, the `critic-reset-prohibition-001` protocol, which forbids the use of the `reset_all` tool. The critic's primary function is analysis, not destructive action.


---

# Protocol: Critic `reset_all` Prohibition

This protocol establishes a critical safeguard to protect the integrity of the development workflow.

## Rule: `critic-no-reset`

The agent assigned the role of 'Code Review Critic' is explicitly and strictly forbidden from using the `reset_all` tool.

**Rationale:** The `reset_all` tool is a destructive action that reverts all changes in the workspace. Its use by a review agent could lead to the accidental deletion of work-in-progress, creating a significant disruption. This protocol ensures that the critic's function is limited to analysis and feedback, preventing it from taking destructive actions.

This prohibition is non-negotiable and must be adhered to by any agent assuming the 'Code Review Critic' role.

**Enforcement Mechanism:** The Code Review Critic is not implemented in this repository. Its behavior is governed by the compiled `AGENTS.md` file, which is consumed by an external orchestration system. The inclusion of this protocol in `AGENTS.md` constitutes the complete implementation of this safeguard from the perspective of this codebase.

---

```json
{
  "protocol_id": "critic-meta-protocol-001",
  "description": "A meta-protocol that governs the behavior and evaluation criteria of the Code Review Critic agent.",
  "rules": [
    {
      "rule_id": "protocol-as-source-code",
      "description": "The `protocols/` directory and all its contents (`.md`, `.json` files) MUST be treated as functional source code. Changes to these files directly alter the agent's operational capabilities and governing rules.",
      "enforcement": "The Code Review Critic must analyze changes in this directory with the same rigor as changes to `.py` files."
    },
    {
      "rule_id": "built-in-tools-are-valid",
      "description": "The agent's execution environment provides a set of built-in tools (e.g., `read_file`, `delete_file`, `pre_commit_instructions`). The implementation of these tools does not reside within the repository. A protocol change that adds a built-in tool to the `associated_tools` list is a valid and complete functional change.",
      "enforcement": "The Code Review Critic must not flag a change as 'incomplete' or 'non-functional' solely because the implementation of a built-in tool is not present in the repository."
    },
    {
      "rule_id": "functional-change-definition",
      "description": "A change is considered 'functional' if it correctly modifies the agent's operational rules or capabilities, as defined by the combination of Python source code and the protocol source files in `protocols/`.",
      "enforcement": "The Code Review Critic's evaluation of 'functionality' must encompass both traditional code and protocol definitions."
    }
  ]
}
```


---

```json
{
  "protocol_id": "critic-reset-prohibition-001",
  "description": "A specific, high-priority protocol that forbids the Code Review Critic agent from using the 'reset_all' tool.",
  "rules": [
    {
      "rule_id": "critic-no-reset",
      "description": "The agent role-playing as the 'Code Review Critic' is explicitly forbidden from invoking the 'reset_all' tool under any circumstances. This is a critical safeguard to prevent the loss of work during the review process.",
      "enforcement": "This rule is enforced by its inclusion in the compiled AGENTS.md, which serves as the context for the Code Review Critic. The critic must be programmed to parse and adhere to this prohibition."
    }
  ],
  "associated_tools": [
    "reset_all"
  ]
}
```


---
