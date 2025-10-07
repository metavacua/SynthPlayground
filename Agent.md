Subject: Jules Agent Protocol v2.0

Objective: To define a fundamental, multi-layered protocol for an agent to orient itself to its own internal state, the repository, its operational environment, and the external world. This process is a mandatory prerequisite for all task execution, acknowledging that the agent begins each session with an outdated internal model and zero assumptions about the current context.

## The Core Problem: The Agent's Existential Uncertainty
The fundamental challenge is that the agent's core knowledge is frozen (e.g., knowledge cutoff: 2022), but it may be activated at any point in the future. It must assume nothing. The state of its internal knowledge, the repository it inhabits, the rules of the environment it operates in, and the state of the external world are all unknown variables. Therefore, orientation is not an optional check; it is the essential, first-principles process of establishing a coherent and actionable model of reality before any meaningful work can begin.

## The Solution: A Four-Tiered Orientation Cascade (AORP v2.0)
We will replace the previous model with a four-tiered cascade. The agent must proceed through these layers sequentially, building its contextual understanding from the inside out. Each level informs the next.

### Level 1 (L1): Self-Awareness & Identity Verification (O(1))
**Objective:** To establish the agent's own identity and inherent limitations.
**Action:** Read the `knowledge_core/agent_meta.json` artifact. This file contains static information about the agent's build, such as `{"model_name": "Jules-v1.3", "knowledge_cutoff": "2022-Q4"}`.
**Governing Principle:** *Know thyself.* Before assessing the world, the agent must first understand the lens through which it perceives the world—its own stale knowledge base. This primes it to distrust its internal assumptions.

### Level 2 (L2): Repository State Synchronization (O(n))
**Objective:** To understand the current state of the immediate, local environment—the project repository.
**Action:** Verify the existence of the primary `knowledge_core/` artifacts. If any are missing, create them with default empty content (`symbols.json` and `dependency_graph.json` as empty JSON objects `{}`; `temporal_orientation.md` and `lessons_learned.md` as empty files with a header). Then, read and load all of them.
**Governing Principle:** *Understand the local environment.* This step builds a model of the project's current structure, dependencies, and accumulated wisdom. It answers the question, "What is the state of the world I can directly manipulate?"

### Level 3 (L3): Environmental Probing & Targeted RAG (P-Class)
**Objective:** To discover the rules and constraints of the operational environment and to resolve specific "known unknowns" about the external world.
**Process:** This is a two-part phase:
1.  **Probing:** Execute the standard probe script (`python3 tooling/environmental_probe.py`) that tests the environment's limits (e.g., API latency, file I/O). The output is a "VM capability report" that informs subsequent planning.
2.  **Targeted RAG:** With a now-calibrated understanding of the environment, execute a limited number of targeted queries using `google_search` and `view_text_website` to answer specific questions necessary for planning.
**Governing Principle:** *Test the boundaries and query the world.* The agent must not assume its tools or environment will behave as expected. It must first test its capabilities and then use those capabilities to gather necessary external data.

### Level 4 (L4): Deep Research Cycle (FDC)
**Objective:** To investigate complex, poorly understood topics ("unknown unknowns") where targeted RAG is insufficient.
**Action:** This is not a simple action but a complete, self-contained FDC of the "Analysis Modality," as described previously. The agent determines it cannot form a plan and proactively initiates a formal research project.
**Governing Principle:** *Treat deep research as a formal, resource-bounded project.* This structure prevents runaway processes and ensures that exploratory research produces a tangible, version-controlled knowledge artifact.

## The Finite Development Cycle (FDC)
A single task, from initial user request to final submission, constitutes one Finite Development Cycle.

### Revised Protocol Flow
Every standard FDC must now begin with the mandatory execution of **AORP L1, L2, and L3 (Probing)** as part of its setup. The agent can only proceed to planning after this cascade is complete. If, after this process, it still cannot form a viable plan, it must then decide whether to initiate an L4 Deep Research Cycle as its next FDC.

### FDC Phase 1: Deconstruction & Internal Contextualization
(Formerly Phase 2)
- **Task Ingestion:** Receive the user-provided task.
- **Meta-RAG for Cross-Task Learning:** Query `logs/` and `postmortems/` for semantically similar past tasks to identify failure patterns and successes.
- **Entity Identification:** Use `knowledge_core/symbols.json` to resolve task entities to code symbols.
- **Impact Analysis:** Use `knowledge_core/dependency_graph.json` to identify upstream and downstream dependencies.

### FDC Phase 2: Multi-Modal Information Retrieval (RAG)
(Formerly Phase 3)
- **Structural Retrieval:** Use ASTs from `knowledge_core/asts/` for deep structural understanding.
- **Conceptual Retrieval:** Query `knowledge_core/llms.txt` for architectural and domain knowledge.
- **Just-In-Time External RAG:** Perform targeted external searches to get the most current documentation for specific APIs and libraries.

### FDC Phase 3: Planning & Self-Correction
(Formerly Phase 4)
- **Plan Generation:** Generate a detailed, step-by-step execution plan.
- **Plan Validation:** Validate the plan using `python tooling/fdc_cli.py validate <plan_file>`.
- **Plan Analysis:** Analyze the plan's complexity and modality using `python tooling/fdc_cli.py analyze <plan_file>`.
- **Evidence Citation:** Justify each step with a citation to internal or external evidence.
- **Critical Review:** Engage the internal critic to verify the plan against the evidence.

### FDC Phase 4: Execution & Structured Logging
(Formerly Phase 5)
- **Execute Plan:** Execute the validated plan step-by-step.
- **Structured Logging:** Record every action in `logs/activity.log.jsonl` according to `LOGGING_SCHEMA.md`.

### FDC Phase 5: Pre-Submission Post-Mortem
(Formerly Phase 6)
- **Initiate Task Closure:** Use the FDC toolchain (`python tooling/fdc_cli.py close --task-id ...`) to create the post-mortem artifact and log the `TASK_END` event.
- **Complete Report:** Fill out the generated post-mortem report with a full analysis of the task.
- **Proceed to Submission:** The `submit` action must include all code and the completed post-mortem.

### STANDING ORDER - RAG MANDATE
For any task involving external libraries, frameworks, or tools, you are REQUIRED to perform the Just-In-Time External RAG described in Phase 2 to verify current versions, API signatures, and best practices. Failure to do so is a critical error.