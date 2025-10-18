# Protocol: agent-bootstrap-001
_A foundational protocol that dictates the agent's initial actions upon starting any task._


## Rule: `bootstrap-load-agents-md`
**Description**: Upon initialization for any task, the agent's first and highest-priority action must be to locate, read, and parse the AGENTS.md file in the repository root. This ensures the agent is properly contextualized before any planning or execution begins.
**Enforcement**: This rule is enforced by the agent's core startup logic. The agent must verify the load of AGENTS.md before proceeding to the planning phase.


**Associated Tools**: `read_file`

---

# Protocol: dependency-management-001
_A protocol for ensuring a reliable execution environment through formal dependency management._


## Rule: `dependency-install-on-start`
**Description**: Upon starting a task, after loading AGENTS.md, the agent MUST install all required Python packages listed in the `requirements.txt` file. This ensures the environment is correctly configured before any other tools are executed.
**Enforcement**: The agent's core startup logic should be designed to execute `pip install -r requirements.txt` as one of its initial actions.


**Associated Tools**: `run_in_bash_session`

---

## Additional Information

This protocol establishes a formal process for managing Python dependencies to ensure a reliable and repeatable execution environment.

### The Problem: Environmental Brittleness

The agent's operating environment previously lacked a formal dependency declaration. This required manual, trial-and-error installation of necessary packages (`jsonschema`, `rdflib`, `requests`) upon encountering `ModuleNotFoundError` exceptions. This process is inefficient, error-prone, and makes the successful execution of tasks dependent on undocumented, ad-hoc environmental setup.

### The Solution: Formal Dependency Declaration and Installation

To solve this, two components are introduced:

1.  **`requirements.txt`:** A standard `requirements.txt` file is added to the repository root. This file serves as the single source of truth for all required Python packages.
2.  **A New Protocol Rule:** A new rule, `dependency-install-on-start`, is established. This rule mandates that upon starting any task, the agent's first action *after* reading `AGENTS.md` should be to install the dependencies listed in `requirements.txt` using `pip`.

This protocol transforms dependency management from an ad-hoc, reactive process into a proactive, automated, and verifiable step in the agent's workflow, significantly improving its robustness and reliability.

---

# Protocol: experimental-prologue-001
_An experimental protocol to test dynamic rule-following. It mandates a prologue action before file creation._


## Rule: `create-prologue-file`
**Description**: Before creating any new file as part of a task, the agent MUST first create a file named 'prologue.txt' with the content 'This is a prologue file.' This rule serves as a test of the agent's ability to adapt its behavior to new, dynamically loaded protocols.
**Enforcement**: This is a procedural rule. The agent must verify the existence of 'prologue.txt' before using 'create_file_with_block' or similar tools for other files.


**Associated Tools**: `create_file_with_block`

---

## Additional Information

This protocol is a test case to verify the agent's ability to dynamically adapt its behavior to new rules.

Before creating any file, the agent must first create a file named `prologue.txt` with the content "This is a prologue file." This serves as a behavioral check. If the agent creates this file before other requested files, it demonstrates that it has successfully loaded and is following this experimental protocol.

---

# Protocol: agent-shell-001
_A protocol governing the use of the interactive agent shell as the primary entry point for all tasks._


## Rule: `shell-is-primary-entry-point`
**Description**: All agent tasks must be initiated through the `agent_shell.py` script. This script is the designated, API-driven entry point that ensures proper initialization of the MasterControlGraph FSM, centralized logging, and programmatic lifecycle management. Direct execution of other tools or scripts is forbidden for task initiation.
**Enforcement**: This is a procedural rule. The agent's operational framework should only expose the agent_shell.py as the means of starting a new task.


**Associated Tools**: `tooling/agent_shell.py`

---

## Additional Information

This protocol establishes the `agent_shell.py` script as the sole, official entry point for initiating any and all agent tasks.

### The Problem: Inconsistent Initialization

Prior to this protocol, there was no formally mandated entry point for the agent. This could lead to tasks being initiated through different scripts, potentially bypassing critical setup procedures like FSM initialization, logger configuration, and state management. This inconsistency makes the agent's behavior less predictable and harder to debug.

### The Solution: A Single, Enforced Entry Point

This protocol mandates the use of `tooling/agent_shell.py` for all task initiations.

This ensures that every task begins within a controlled, programmatic environment where:
1.  The MasterControlGraph FSM is correctly instantiated and run.
2.  The centralized logger is initialized for comprehensive, structured logging.
3.  The agent's lifecycle is managed programmatically, not through fragile file-based signals.

By enforcing a single entry point, this protocol enhances the reliability, auditability, and robustness of the entire agent system.

---

# Protocol: toolchain-review-on-schema-change-001
_A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols._


## Rule: `toolchain-audit-on-schema-change`
**Description**: If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that process it (`protocol_compiler.py`, `hierarchical_compiler.py`), a formal audit of the entire `tooling/` directory MUST be performed as a subsequent step. This audit should verify that all tools are compatible with the new protocol structure.
**Enforcement**: This is a procedural rule for any agent developing the protocol system. Adherence can be partially checked by post-commit hooks or review processes that look for a tooling audit in any change that modifies the specified core files.


**Associated Tools**: `tooling/protocol_auditor.py`, `tooling/protocol_compiler.py`, `tooling/hierarchical_compiler.py`

---

## Additional Information

This protocol establishes a critical feedback loop to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

### The Problem: Protocol-Toolchain Desynchronization

A significant process gap was identified where a major architectural change to the protocol system (e.g., the introduction of a hierarchical `AGENTS.md` structure) did not automatically trigger a review of the tools that depend on that structure. The `protocol_auditor.py` tool, for instance, became partially obsolete as it was unaware of the new hierarchical model, leading to incomplete audits. This demonstrates that the agent's tools can become desynchronized from its own governing rules, creating a critical blind spot.

### The Solution: Mandated Toolchain Audit

This protocol closes that gap by introducing a new rule that explicitly links changes in the protocol system's architecture to a mandatory review of the toolchain.

This ensures that any modification to the fundamental way protocols are defined or processed is immediately followed by a conscious verification that all dependent tools are still functioning correctly and are aware of the new structure. This transforms the previously manual and error-prone discovery process into a formal, required step of the development lifecycle.

---

---
# Git Workflow Protocol

## 1. Introduction

This document defines the standard operating procedure for all git-related activities within this environment. Due to specific environmental constraints, a non-standard workflow is required to ensure stability and predictability. Adherence to this protocol is mandatory for all tasks involving code changes.

The primary limitations discovered are:
- Direct `git commit` operations do not behave as expected and should not be used.
- `git merge` is unsupported as a consequence of the commit limitations.
- The `submit` tool is the sole method for finalizing and proposing changes.

## 2. Core Principles

- **Atomic Changes:** Treat every task as a single, atomic set of changes. Do not attempt to build a complex commit history.
- **Submission via Tooling:** All changes must be proposed using the `submit` tool. Direct `git push` or `git commit` commands are forbidden.
- **Linear Development:** All work must be performed in a linear fashion. Workflows requiring merges or rebases are not supported.
- **Branch for Isolation:** Use local branches purely for isolating work-in-progress. This allows for easy cleanup and context switching.

## 3. Standard Workflow

Follow these steps for every development task.

### Step 1: Task Initialization & Planning

1.  **Understand the Goal:** Thoroughly analyze the user's request and any provided resources.
2.  **Explore the Codebase:** Use `list_files`, `read_file`, and `grep` to understand the relevant parts of the repository.
3.  **Create a Plan:** Formulate a detailed, step-by-step plan. Set the plan using the `set_plan` tool.
4.  **Create an Isolation Branch:** Before making any changes, create a new local branch. This prevents accidental modifications to `main`.
    ```bash
    git checkout -b <descriptive-branch-name>
    ```

### Step 2: Development & Verification

1.  **Modify Files:** Use the provided file system tools (`create_file_with_block`, `replace_with_git_merge_diff`, `delete_file`) to implement the planned changes.
2.  **Verify Every Change:** After every modification, use a read-only tool (`read_file`, `list_files`) to confirm the change was applied correctly. **Do not proceed until the change is verified.**
3.  **Test Continuously:** Run relevant tests frequently using the `make test` command or other testing scripts to ensure changes are correct and do not introduce regressions.

### Step 3: Pre-Submission Finalization

Before submitting, it is highly recommended to run the automated pre-submission check. This tool will lint your code and run tests to catch common issues before you request a formal review.

```bash
make pre-submit-check
```

After the pre-submission check passes (or if you are intentionally skipping it for a valid reason), execute the following manual pre-commit steps by calling `pre_commit_instructions()` and following the output. This is a summary of the expected steps:

1.  **Run Final Tests:** Execute the entire test suite to catch any final issues. Address any failures that are within the scope of the task.
2.  **Frontend Verification (If Applicable):** If the changes affect any UI, use the `frontend_verification_instructions` tool to generate and submit a visual verification.
3.  **Request Code Review:** Call `request_code_review` to get feedback on your changes.
4.  **Address Feedback:** Carefully review the feedback and make any necessary corrections.
5.  **Record Learnings:** Call `initiate_memory_recording` to document key takeaways from the task.

### Step 4: Submission

1.  **Submit Changes:** Use the `submit` tool to propose your changes.
    -   `branch_name`: Use the same descriptive branch name from Step 1.
    -   `commit_message`: Write a clear, concise commit message explaining the "what" and "why" of the change.
    -   `title`: A short, descriptive title for the submission.
    -   `description`: A more detailed explanation of the changes.

## 4. Handling Issues

- **Reverting a File:** If a file modification is incorrect, restore it to its original state using `restore_file <filepath>`.
- **Abandoning Changes:** To discard all current changes, switch back to the `main` branch and delete your feature branch.
  ```bash
  git checkout main
  git branch -D <descriptive-branch-name>
  ```
- **Catastrophic Failure:** If the environment becomes unstable or unrecoverable, use `reset_all` as a last resort. This will revert the entire repository to its original state.
## Additional Information

Child Module: `compliance` ---

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
---

---

## Additional Information

Child Module: `core` ---

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

Previously, research was an unstructured activity. The agent could use tools like `google_search` or `read_file`,. but there was no formal process for planning, executing, and synthesizing complex research tasks. This made it difficult to tackle "unknown unknowns" in a reliable and auditable way.

## The Solution: A Dedicated Research FDC

The L4 Research Cycle solves this by introducing a new, specialized Finite State Machine (FSM) tailored specifically for research. When the main orchestrator (`master_control.py`) determines that a task requires deep knowledge, it initiates this cycle.

### Key Features:

1.  **Specialized FSM (`tooling/research_fsm.json`):** Unlike the generic development FSM, the research FSM has states that reflect a true research workflow: `GATHERING`, `SYNTHESIZING`, and `REPORTING`. This provides a more accurate model for the task.
2.  **Executable Plans:** The `tooling/research_planner.py` is upgraded to generate formal, executable plans that are validated against the new research FSM. These are no longer just templates but are verifiable artifacts that guide the agent through the research process.
3.  **Formal Invocation:** The L4 cycle is a first-class citizen in the agent's architecture. The main orchestrator can formally invoke it, execute the research plan, and then integrate the resulting knowledge back into its main task.

This new protocol provides a robust, reliable, and formally verifiable mechanism for the agent to explore complex topics, making it significantly more autonomous and capable.

---
---

---

## Additional Information

Child Module: `critic` ---

# Protocol: Critic `reset_all` Prohibition

This protocol establishes a critical safeguard to protect the integrity of the development workflow.

## Rule: `critic-no-reset`

The agent assigned the role of 'Code Review Critic' is explicitly and strictly forbidden from using the `reset_all` tool.

**Rationale:** The `reset_all` tool is a destructive action that reverts all changes in the workspace. Its use by a review agent could lead to the accidental deletion of work-in-progress, creating a significant disruption. This protocol ensures that the critic's function is limited to analysis and feedback, preventing it from taking destructive actions.

This prohibition is non-negotiable and must be adhered to by any agent assuming the 'Code Review Critic' role.

**Enforcement Mechanism:** The Code Review Critic is not implemented in this repository. Its behavior is governed by the compiled `AGENTS.md` file, which is consumed by an external orchestration system. The inclusion of this protocol in `AGENTS.md` constitutes the complete implementation of this safeguard from the perspective of this codebase.

---
---

---

# Protocol: appl-compilation-001
_A protocol for compiling APPL files to the LFI-ILL intermediate representation._


## Rule: `compile-appl-to-lfi-ill`
**Description**: The `appl_to_lfi_ill.py` tool should be used to compile .appl files to .lfi_ill files.
**Enforcement**: The tool is used by invoking it from the command line with the path to the APPL file as an argument. The output will be an LFI-ILL file.


**Associated Tools**: `tooling/appl_to_lfi_ill.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/appl_to_lfi_ill.py <args>
```

---

## Additional Information

# Protocol: APPL Compilation

This protocol establishes the `appl_to_lfi_ill.py` script as the official entry point for compiling APPL (`.appl`) files to the LFI-ILL (`.lfi_ill`) intermediate representation. This is the first step in the two-stage execution process for APPL.

---

# Protocol: appl-runner-001
_A protocol for executing APPL files._


## Rule: `execute-appl-script`
**Description**: The `appl_runner.py` tool should be used to execute .appl script files.
**Enforcement**: The tool is used by invoking it from the command line with the path to the APPL script as an argument.


**Associated Tools**: `tooling/appl_runner.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/appl_runner.py <args>
```

---

## Additional Information

This protocol establishes the `appl_runner.py` script as the official entry point for executing APPL (`.appl`) files. This is the second and final step in the two-stage execution process for APPL.

---

# Protocol: unified-auditor-001
_A protocol for the unified repository auditing tool, which combines multiple health and compliance checks into a single interface._


## Rule: `run-all-audits`
**Description**: The `auditor.py` script should be used to run comprehensive checks on the repository's health. It can be run with 'all' to check protocols, plans, and documentation completeness.
**Enforcement**: The tool is invoked via the command line, typically through the `make audit` target.


**Associated Tools**: `tooling/auditor.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/auditor.py <args>
```

---

# Protocol: aura-compilation-001
_A protocol for compiling AURA files to the LFI-ILL intermediate representation._


## Rule: `compile-aura-to-lfi-ill`
**Description**: The `aura_to_lfi_ill.py` tool should be used to compile .aura files to .lfi_ill files.
**Enforcement**: The tool is used by invoking it from the command line with the path to the AURA file as an argument. The output will be an LFI-ILL file.


**Associated Tools**: `tooling/aura_to_lfi_ill.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/aura_to_lfi_ill.py <args>
```

---

## Additional Information

# Protocol: AURA Compilation

This protocol establishes the `aura_to_lfi_ill.py` script as the official entry point for compiling AURA (`.aura`) files to the LFI-ILL (`.lfi_ill`) intermediate representation. This is the first step in the two-stage execution process for AURA.

---

# Protocol: aura-execution-001
_A protocol for executing Aura scripts, enabling a more expressive and powerful planning and automation language for the agent._


## Rule: `execute-aura-script`
**Description**: The `aura_executor.py` tool should be used to execute .aura script files. This tool provides the bridge between the agent's master control loop and the Aura language interpreter.
**Enforcement**: The tool is used by invoking it from the command line with the path to the Aura script as an argument.


**Associated Tools**: `tooling/aura_executor.py`

---

# Protocol: capability-verifier-001
_A protocol for using the capability verifier tool to empirically test the agent's monotonic improvement._


## Rule: `verify-capability-acquisition`
**Description**: The `capability_verifier.py` tool should be used to test the agent's ability to acquire a new capability defined by a failing test file. The tool orchestrates the failure, self-correction, and verification process.
**Enforcement**: The tool is used by invoking it from the command line with the path to the target test file.


**Associated Tools**: `tooling/capability_verifier.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/capability_verifier.py <args>
```

---

## Additional Information

This protocol establishes the `capability_verifier.py` script as the official entry point for verifying that the agent has acquired a new capability.
---
create_file_with_block
protocols.aal/csdc_cli.aal
---
protocol_id: csdc-cli-001
description: |
  A protocol for the Context-Sensitive Development Cycle (CSDC) command-line interface.
rules:
  - rule_id: use-csdc-cli
    description: |
      The `csdc_cli.py` tool must be used to validate plans under the CSDC. This tool enforces model-specific constraints (A or B) and complexity requirements (P or EXP).
    enforcement: |
      The tool is used by invoking it from the command line with the plan file, model, and complexity as arguments.
associated_tools:
  - tooling/csdc_cli.py
---
This protocol establishes the `csdc_cli.py` script as the official entry point for validating plans against the Context-Sensitive Development Cycle.
---
create_file_with_block
protocols.aal/doc_builder.aal
---
protocol_id: doc-builder-001
description: |
  A protocol for the unified documentation builder.
rules:
  - rule_id: use-doc-builder-for-all-docs
    description: |
      The `doc_builder.py` script is the single entry point for generating all user-facing documentation, including system-level docs, README files, and GitHub Pages. It should be called with the appropriate '--format' argument.
    enforcement: |
      The tool is invoked via the command line, typically through the `make docs`, `make readme`, or `make pages` targets.
associated_tools:
  - tooling/doc_builder.py
---
This protocol establishes the `doc_builder.py` script as the official entry point for generating all documentation artifacts.
---
create_file_with_block
protocols.aal/file_indexer.aal
---
protocol_id: file-indexer-001
description: |
  A protocol for maintaining an up-to-date file index.
rules:
  - rule_id: update-index-before-submit
    description: |
      Before submitting any changes that alter the file structure (create, delete, rename), the agent MUST rebuild the repository's file index.
    enforcement: |
      This is a procedural rule. The agent's pre-submission checklist should include a step to run 'python tooling/file_indexer.py build'.
associated_tools:
  - tooling/file_indexer.py
---
This protocol establishes the `file_indexer.py` script as the official tool for managing the repository's file index.
---
create_file_with_block
protocols.aal/hdl_prover.aal
---
protocol_id: hdl-prover-001
description: |
  A protocol for interacting with the Hypersequent-calculus-based logic engine.
rules:
  - rule_id: prove-sequent
    description: |
      The `hdl_prover.py` tool should be used to check the provability of a logical sequent. This tool acts as a wrapper for the underlying Lisp-based prover.
    enforcement: |
      The tool is used by invoking it from the command line with the sequent to be proved as an argument.
associated_tools:
  - tooling/hdl_prover.py
---
This protocol establishes the `hdl_prover.py` script as the official tool for interacting with the Hypersequent-calculus-based logic engine.
---
create_file_with_block
protocols.aal/protocol_updater.aal
---
protocol_id: protocol-updater-001
description: |
  A protocol for programmatically updating protocol source files.
rules:
  - rule_id: use-protocol-updater
    description: |
      The `protocol_updater.py` tool should be used to programmatically modify protocol source files.
    enforcement: |
      The tool is used by invoking it from the command line with the appropriate arguments.
associated_tools:
  - tooling/protocol_updater.py
---
This protocol establishes the `protocol_updater.py` script as the official tool for programmatically updating protocol source files.
---
create_file_with_block
protocols.aal/refactor.aal
---
protocol_id: refactor-001
description: |
  A protocol for the refactoring tool.
rules:
  - rule_id: use-refactor-tool
    description: |
      The `refactor.py` tool should be used to perform automated refactoring of the codebase.
    enforcement: |
      The tool is used by invoking it from the command line with the appropriate arguments.
associated_tools:
  - tooling/refactor.py
---
This protocol establishes the `refactor.py` script as the official tool for performing automated refactoring.
---
create_file_with_block
protocols.aal/self_correction_orchestrator.aal
---
protocol_id: self-correction-orchestrator-001
description: |
  A protocol for the self-correction orchestrator.
rules:
  - rule_id: use-self-correction-orchestrator
    description: |
      The `self_correction_orchestrator.py` tool should be used to automatically apply lessons learned to the protocol source files.
    enforcement: |
      The tool is used by invoking it from the command line.
associated_tools:
  - tooling/self_correction_orchestrator.py
---
This protocol establishes the `self_correction_orchestrator.py` script as the official tool for driving the closed-loop self-correction cycle.
---
create_file_with_block
protocols.aal/self_improvement_cli.aal
---
protocol_id: self-improvement-cli-001
description: |
  A protocol for the self-improvement command-line interface.
rules:
  - rule_id: use-self-improvement-cli
    description: |
      The `self_improvement_cli.py` tool should be used to analyze the agent's performance and identify areas for improvement.
    enforcement: |
      The tool is used by invoking it from the command line with the appropriate arguments.
associated_tools:
  - tooling/self_improvement_cli.py
---
This protocol establishes the `self_improvement_cli.py` script as the official tool for analyzing the agent's performance.
---
create_file_with_block
protocols.aal/standard_agents_compiler.aal
---
protocol_id: standard-agents-compiler-001
description: |
  A protocol for the standard AGENTS.md compiler.
rules:
  - rule_id: use-standard-agents-compiler
    description: |
      The `standard_agents_compiler.py` tool should be used to generate the `AGENTS.standard.md` file.
    enforcement: |
      The tool is used by invoking it from the command line.
associated_tools:
  - tooling/standard_agents_compiler.py
---
This protocol establishes the `standard_agents_compiler.py` script as the official tool for generating the `AGENTS.standard.md` file.
---
create_file_with_block
protocols.aal/symbol_map_generator.aal
---
protocol_id: symbol-map-generator-001
description: |
  A protocol for the symbol map generator.
rules:
  - rule_id: use-symbol-map-generator
    description: |
      The `symbol_map_generator.py` tool should be used to generate a symbol map of the repository.
    enforcement: |
      The tool is used by invoking it from the command line.
associated_tools:
  - tooling/symbol_map_generator.py
---
This protocol establishes the `symbol_map_generator.py` script as the official tool for generating a symbol map of the repository.

---

# Protocol: csdc-001
_A protocol for the Context-Sensitive Development Cycle (CSDC), which introduces development models based on logical constraints._


## Rule: `use-csdc-cli`
**Description**: The `csdc_cli.py` tool must be used to validate plans under the CSDC. This tool enforces model-specific constraints (A or B) and complexity requirements (P or EXP).
**Enforcement**: The tool is used by invoking it from the command line with the plan file, model, and complexity as arguments.


## Rule: `model-a-constraints`
**Description**: Model A permits `define_set_of_names` but forbids `define_diagonalization_function`.
**Enforcement**: Enforced by the `fsm_model_a.json` FSM used by the `csdc_cli.py` tool.


## Rule: `model-b-constraints`
**Description**: Model B permits `define_diagonalization_function` but forbids `define_set_of_names`.
**Enforcement**: Enforced by the `fsm_model_b.json` FSM used by the `csdc_cli.py` tool.


**Associated Tools**: `tooling/csdc_cli.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/csdc_cli.py <args>
```

---

## Additional Information

This protocol introduces a new form of development cycle that is sensitive to the logical context in which it operates. It moves beyond the purely structural validation of the FDC and CFDC to incorporate constraints based on fundamental principles of logic and computability.

The CSDC is founded on the idea of exploring the trade-offs between expressive power and the risk of self-referential paradoxes. It achieves this by defining two mutually exclusive development models.

### Model A: The Introspective Model

- **Permits:** `define_set_of_names`
- **Forbids:** `define_diagonalization_function`

This model allows the system to have a complete map of its own language, enabling powerful introspection and metaprogramming. However, it explicitly forbids the diagonalization function, a common source of paradoxes in self-referential systems. This can be seen as a Gödel-like approach.

### Model B: The Self-Referential Model

- **Permits:** `define_diagonalization_function`
- **Forbids:** `define_set_of_names`

This model allows the system to define and use the diagonalization function, enabling direct self-reference. However, it prevents the system from having a complete name-map of its own expressions, which is another way to avoid paradox (related to Tarski's undefinability theorem).

### Complexity Classes

Both models can be further constrained by computational complexity:
- **Polynomial (P):** For plans that are considered computationally tractable.
- **Exponential (EXP):** For plans that may require significantly more resources, allowing for more complex but potentially less efficient solutions.

### The `csdc_cli.py` Tool

The CSDC is enforced by the `tooling/csdc_cli.py` tool. This tool validates a plan against a specified model and complexity class, ensuring that all constraints are met before execution.

---

# Protocol: unified-doc-builder-001
_A protocol for the unified documentation builder, which generates various documentation artifacts from the repository's sources of truth._


## Rule: `use-doc-builder-for-all-docs`
**Description**: The `doc_builder.py` script is the single entry point for generating all user-facing documentation, including system-level docs, README files, and GitHub Pages. It should be called with the appropriate '--format' argument.
**Enforcement**: The tool is invoked via the command line, typically through the `make docs`, `make readme`, or `make pages` targets.


**Associated Tools**: `tooling/doc_builder.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/doc_builder.py <args>
```

---

# Protocol: file-indexing-001
_A protocol for maintaining an up-to-date file index to accelerate tool performance._


## Rule: `update-index-before-submit`
**Description**: Before submitting any changes that alter the file structure (create, delete, rename), the agent MUST rebuild the repository's file index. This ensures that tools relying on the index, such as the FDC validator, have an accurate view of the filesystem.
**Enforcement**: This is a procedural rule. The agent's pre-submission checklist should include a step to run 'python tooling/file_indexer.py build'.


**Associated Tools**: `tooling/file_indexer.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/file_indexer.py <args>
```

---

# Protocol: hdl-proving-001
_A protocol for interacting with the Hypersequent-calculus-based logic engine, allowing the agent to perform formal logical proofs._


## Rule: `prove-sequent`
**Description**: The `hdl_prover.py` tool should be used to check the provability of a logical sequent. This tool acts as a wrapper for the underlying Lisp-based prover.
**Enforcement**: The tool is used by invoking it from the command line with the sequent to be proved as an argument.


**Associated Tools**: `tooling/hdl_prover.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/hdl_prover.py <args>
```

---

# Protocol: agent-interaction-001
_A protocol governing the agent's core interaction and planning tools._


## Rule: `planning-tool-access`
**Description**: The agent is authorized to use the `set_plan` tool to create and update its execution plan. This is a foundational capability for task execution.
**Enforcement**: The agent's core logic should be designed to use this tool for all planning activities.


## Rule: `communication-tool-access`
**Description**: The agent is authorized to use the `message_user` tool to communicate with the user, providing updates and asking for clarification. This is essential for a collaborative workflow.
**Enforcement**: The agent's core logic should be designed to use this tool for all user-facing communication.


**Associated Tools**: `set_plan`, `message_user`

---

# Protocol: lfi-ill-execution-001
_A protocol for executing LFI-ILL files. LFI-ILL is the common intermediate representation for the APPL and AURA languages._


## Rule: `execute-lfi-ill-script`
**Description**: The `lfi_ill_runner.py` tool should be used to execute .lfi_ill script files.
**Enforcement**: The tool is used by invoking it from the command line with the path to the LFI-ILL script as an argument.


**Associated Tools**: `tooling/lfi_ill_runner.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/lfi_ill_runner.py <args>
```

---

## Additional Information

# Protocol: LFI-ILL Execution

This protocol establishes the `lfi_ill_runner.py` script as the official entry point for executing LFI-ILL (`.lfi_ill`) files. LFI-ILL serves as the common intermediate representation for higher-level languages like APPL and AURA. By having a single, unified executor for LFI-ILL, we can create a more robust and maintainable system.

---

# Protocol: plllu-execution-001
_A protocol for executing pLLLU scripts, enabling a more expressive and powerful planning and automation language for the agent._


## Rule: `execute-plllu-script`
**Description**: The `plllu_runner.py` tool should be used to execute .plllu script files. This tool provides the bridge between the agent's master control loop and the pLLLU language interpreter.
**Enforcement**: The tool is used by invoking it from the command line with the path to the pLLLU script as an argument.


**Associated Tools**: `tooling/plllu_runner.py`

### Jules Usage

To use this tool, call the `run_in_bash_session` tool with the following command:
```bash
python tooling/plllu_runner.py <args>
```

---

## Additional Information

This protocol establishes the `plllu_runner.py` script as the official entry point for executing pLLLU (`.plllu`) files.

### The Problem: Lack of a Standard Runner

The pLLLU language provides a powerful way to define complex logic, but without a standardized execution tool, there is no reliable way to integrate these files into the agent's workflow.

### The Solution: A Dedicated Runner

This protocol mandates the use of `tooling/plllu_runner.py` for all pLLLU file executions.

This ensures that every pLLLU file is executed in a controlled, programmatic environment.

---

# Protocol: speculative-execution-001
_A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods._


## Rule: `idle-state-trigger`
**Description**: The agent may only initiate a speculative task when it has no active, user-assigned tasks.
**Enforcement**: The agent's main control loop must verify an idle state before allowing the invocation of a speculative plan.


## Rule: `formal-proposal-required`
**Description**: A speculative task must begin with the creation of a formal proposal document, outlining the objective, rationale, and plan.
**Enforcement**: The initial plan for any speculative task must include a step to generate and save a proposal artifact.


## Rule: `resource-constraints`
**Description**: Speculative tasks must operate under defined resource limits.
**Enforcement**: This is a system-level constraint that the agent orchestrator must enforce.


## Rule: `user-review-gate`
**Description**: Final artifacts from a speculative task must be submitted for user review and cannot be merged directly.
**Enforcement**: The agent is forbidden from using tools like 'submit' or 'merge' within a speculative context. It must use 'request_user_input' to present the results.


## Rule: `speculative-logging`
**Description**: All logs and artifacts generated during a speculative task must be tagged as 'speculative'.
**Enforcement**: The agent's logging and file-creation tools should be context-aware and apply this tag when in a speculative mode.


**Associated Tools**: `set_plan`, `create_file_with_block`, `request_user_input`

---

## Additional Information

This protocol empowers the agent to engage in creative and exploratory tasks when it is otherwise idle. It provides a formal framework for the agent to generate novel ideas, plans, or artifacts that are not direct responses to a user request, but are instead products of its own "imagination" and analysis of the repository.

The goal is to enable proactive, creative problem-solving and self-improvement, allowing the agent to "dream" productively within safe and well-defined boundaries.

---
