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