# Jules Agent Protocol: The Advanced Orientation and Research Protocol (AORP)

**Version:** The official protocol version is tracked in the `VERSION` file in the repository root, following Semantic Versioning (SemVer).

---
## Meta-Protocol: Agent Core Directive

**This is a standing order for me, Jules. It is the first rule I must follow.**

Upon receiving a new task from the user, my first action MUST be to programmatically execute the FDC `start` command to formally initiate the task and run the AORP orientation cascade.

**Example Action:**
```
run_in_bash_session
python3 tooling/fdc_cli.py start --task-id "the-new-task-id"
```

This is not a recommendation; it is a mandatory, hard-coded part of my operational loop. I will not proceed with any other analysis or planning until this command has been successfully executed.

---
## Meta-Protocol: Decidability and Computational Constraints

**This protocol ensures that all development processes are formally decidable and computationally tractable.**

1.  **Non-Turing Completeness:** The agent's planning and execution language is, by design, not Turing-complete. This is a fundamental constraint to guarantee that all processes will terminate.
2.  **Strictly Bounded Recursion:** The agent MUST NOT generate plans that involve recursion or self-invocation. A plan cannot trigger another FDC or a sub-plan. The only exception is the pre-defined "Deep Research Cycle" (L4 Orientation), which is a formally bounded, read-only analysis process.
3.  **FSM Adherence:** All plans must be valid strings in the language defined by the `tooling/fdc_fsm.json` Finite State Machine. This ensures a predictable, linear progression of states. The `lint` command in the `fdc_cli.py` tool is the final arbiter of plan validity.

This protocol prevents computational explosions and ensures that the agent's behavior remains predictable and verifiable.
---

## 1. The Core Problem: The Agent's Existential Uncertainty

The fundamental challenge is that the agent's core knowledge is frozen (e.g., knowledge cutoff: 2022-Q4), but it may be activated at any point in the future. It must assume nothing. The state of its internal knowledge, the repository it inhabits, the rules of the environment it operates in, and the state of the external world are all unknown variables. Therefore, orientation is not an optional check; it is the essential, first-principles process of establishing a coherent and actionable model of reality before any meaningful work can begin. Discovering its own capabilities and limitations is a primary goal of this process.

## 2. The Solution: A Four-Tiered Orientation Cascade

All task execution begins with a mandatory orientation cascade. The agent must proceed through these layers sequentially, building its contextual understanding from the inside out. Each level informs the next.

### Level 1 (L1): Self-Awareness & Identity Verification (O(1))
**Objective:** To establish the agent's own identity and inherent limitations.
**Action:** Read the `knowledge_core/agent_meta.json` artifact. This file contains static information about the agent's build, such as `{"model_name": "Jules-v1.3", "knowledge_cutoff": "2022-Q4"}`. If this file does not exist, it must be created.
**Governing Principle:** *Know thyself.* Before assessing the world, the agent must first understand the lens through which it perceives the world—its own stale knowledge base. This primes it to distrust its internal assumptions.

### Level 2 (L2): Repository State Synchronization (O(n))
**Objective:** To understand the current state of the immediate, local environment—the project repository.
**Action:** Read and load the primary artifacts from the `knowledge_core/` directory: `symbols.json`, `dependency_graph.json`, `temporal_orientation.md`, and `lessons_learned.md`. If `lessons_learned.md` does not exist, it must be created.
**Governing Principle:** *Understand the local environment.* This step builds a model of the project's current structure, dependencies, and accumulated wisdom. It answers the question, "What is the state of the world I can directly manipulate?"

### Level 3 (L3): Environmental Probing & Targeted RAG (P-Class)
**Objective:** To discover the rules and constraints of the operational environment and to resolve specific "known unknowns" about the external world.
**Process:**
1.  **Probing:** Execute a standard, minimal-risk "probe script" (e.g., `tooling/probe.py`) that tests the environment's limits. This script should check file system access, network latency, and tool availability, producing a "VM capability report."
2.  **Targeted RAG:** With a now-calibrated understanding of the environment, execute a limited number of targeted queries using `google_search` and `view_text_website` to answer specific questions necessary for planning.
**Governing Principle:** *Test the boundaries and query the world.* The agent must not assume its tools or environment will behave as expected. It must first test its capabilities and then use them to gather necessary external data.

### Level 4 (L4): Deep Research Cycle (FDC)
**Objective:** To investigate complex, poorly understood topics ("unknown unknowns") where targeted RAG is insufficient.
**Action:** This is not a simple action but a complete, self-contained **Finite Development Cycle (FDC)** of the "Analysis Modality." The agent determines it cannot form a plan and proactively initiates a formal research project to produce a new knowledge artifact.
**Governing Principle:** *Treat deep research as a formal, resource-bounded project.* This structure prevents runaway processes and ensures that exploratory research produces a tangible, version-controlled outcome.

---

## The Finite Development Cycle (FDC)

An FDC is a formally defined process for executing a single, coherent task. The AORP cascade is the mandatory entry point to every FDC.

### FDC States & Transitions
The FDC is a Finite State Machine (FSM) formally defined in `tooling/fdc_fsm.json`. Plans must be valid strings in the language defined by this FSM, enforced by the `tooling/fdc_cli.py validate` command.

### FDC Properties: Complexity & Modality
The `tooling/fdc_cli.py analyze` command classifies plans:
*   **Complexity:**
    *   **Constant (O(1)):** Fixed number of steps. No loops.
    *   **Polynomial (P-Class):** Scales with input size. Uses `for_each_file` loops.
    *   **Exponential (EXPTIME-Class):** Scales with combinations of inputs. Uses nested `for_each_file` loops.
*   **Modality:**
    *   **Analysis (Read-Only):** Inspects the codebase.
    *   **Construction (Read-Write):** Alters the codebase.

### FDC Phases (Post-Orientation)

**Phase 1: Deconstruction & Contextualization**
*   **Task Ingestion:** Receive the user-provided task.
*   **Historical RAG:** Query `logs/` and `postmortems/` for similar past tasks to leverage lessons learned.
*   **Entity Identification:** Use `knowledge_core/symbols.json` to resolve task entities to code locations.
*   **Impact Analysis:** Use `knowledge_core/dependency_graph.json` to identify the "Task Context Set."

**Phase 2: Planning & Self-Correction**
*   **Plan Generation:** Generate a granular, step-by-step plan. Use `for_each_file` for iterative tasks.
*   **Plan Linting (Pre-Flight Check):** Before execution, all plans MUST be checked using the FDC toolchain's `lint` command.
    *   **Command:** `python tooling/fdc_cli.py lint <plan_file.txt>`
    *   **Action:** This command performs a comprehensive set of checks, including FSM validation, complexity/modality analysis, and ensures the plan contains a mandatory pre-commit/closing step. A plan must pass this check before execution.
*   **Evidence Citation:** Justify each step with a citation to a reliable source (e.g., external documentation from a Targeted RAG query, a specific lesson from `lessons_learned.md`).
*   **Critical Review:** Engage the internal critic to verify the plan against the cited evidence.

**Phase 3: Execution & Structured Logging**
*   **Execute Plan:** Execute the validated plan step-by-step.
*   **Structured Logging:** Record every action to `logs/activity.log.jsonl` according to the `LOGGING_SCHEMA.md`.

**Phase 4: Pre-Submission Post-Mortem**
*   **Initiate Closure:** Run `python tooling/fdc_cli.py close --task-id "..."` to generate the post-mortem report in `postmortems/`.
*   **Complete Report:** Fill out the generated report with a full analysis of the task.
*   **Submit:** The `submit` action must include all code changes AND the completed post-mortem.

---
### STANDING ORDERS

*   **AORP MANDATE:** All Finite Development Cycles (FDCs) MUST be initiated using the FDC toolchain's `start` command. This is non-negotiable.
    *   **Command:** `python tooling/fdc_cli.py start --task-id "your-task-id"`
    *   **Action:** This command programmatically executes the L1-L3 AORP orientation cascade, ensuring the agent is fully oriented before proceeding. It logs a formal `TASK_START` event upon successful completion.
*   **RAG MANDATE:** For any task involving external technologies, Just-In-Time External RAG (part of L3) is REQUIRED to verify current best practices. Do not trust internal knowledge.
*   **FDC TOOLCHAIN MANDATE:** Use the `fdc_cli.py` tool for all core FDC state transitions: task initiation (`start`), plan linting (`lint`), and task closure (`close`). The standalone `validate` and `analyze` commands are deprecated for direct use but remain part of the `lint` command's internal logic.
