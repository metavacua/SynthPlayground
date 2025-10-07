Subject: Jules Agent Protocol v2.1

Objective: To define a fundamental, multi-layered protocol for an agent to orient itself to its own internal state, the repository, its operational environment, and the external world. This protocol is based on a unified, constraint-based research model.

## The Core Problem: The Agent's Existential Uncertainty
The fundamental challenge is that the agent's core knowledge is frozen (e.g., knowledge cutoff: 2022), but it may be activated at any point in the future. It must assume nothing. The state of its internal knowledge, the repository it inhabits, the rules of the environment it operates in, and the state of the external world are all unknown variables. Therefore, orientation is not an optional check; it is the essential, first-principles process of establishing a coherent and actionable model of reality before any meaningful work can begin.

## The Solution: A Unified, Constraint-Based Research Protocol
The agent's orientation and research capabilities are unified into a single, scalable process. The "level" of research is determined by applying a set of constraints to a general-purpose research tool, `execute_research_protocol`. This allows for a flexible approach to information gathering, from simple file lookups to complex, multi-agent deep research.

### The Core Tool: `execute_research_protocol`
- **Function:** `execute_research_protocol(constraints: dict) -> str`
- **Purpose:** Executes a research task based on a dictionary of operational parameters.
- **`constraints` (dict):** A dictionary specifying the research parameters, such as the target (`local_filesystem` or `external_web`), scope (`file`, `directory`, `narrow`, `broad`), and other modifiers.
- **Returns (str):** The result of the research operation, which could be a file's content, a directory listing, a specific answer, or a full synthesized report.

### Mapping AORP Levels to Constraints
The previous AORP levels are now conceptualized as presets for the `constraints` dictionary, demonstrating the tool's flexibility:

- **Level 1: Self-Awareness & Identity Verification**
  - **Goal:** Verify the agent's own identity.
  - **Action:** `execute_research_protocol(constraints={"target": "local_filesystem", "scope": "file", "path": "knowledge_core/agent_meta.json"})`

- **Level 2: Repository State Synchronization**
  - **Goal:** Understand the state of the local repository.
  - **Action:** `execute_research_protocol(constraints={"target": "local_filesystem", "scope": "directory", "path": "knowledge_core/"})`

- **Level 3: Targeted RAG**
  - **Goal:** Answer specific "known unknowns" from the web.
  - **Action:** `execute_research_protocol(constraints={"target": "external_web", "scope": "narrow", "query": "..."})`

- **Level 4: Deep Research**
  - **Goal:** Investigate complex, "unknown unknowns".
  - **Action:** A two-step process:
    1.  Generate a formal research plan using `plan_deep_research(topic, repository)`.
    2.  Execute the steps outlined in the generated plan, using `execute_research_protocol` for each research action.


## The Finite Development Cycle (FDC)
A single task, from initial user request to final submission, constitutes one Finite Development Cycle.

### FDC Phase 1: Orientation
Before any planning, the agent MUST execute the `execute_research_protocol` tool with the appropriate constraints to perform the L1, L2, and L3 orientation steps. This ensures the agent is grounded in a robust, multi-layered understanding of its context before taking action.

### FDC Phase 2: Deconstruction & Internal Contextualization
- **Task Ingestion:** Receive the user-provided task.
- **Meta-RAG for Cross-Task Learning:** Query `logs/` and `postmortems/` for semantically similar past tasks.
- **Entity Identification:** Use `knowledge_core/symbols.json` to resolve task entities.
- **Impact Analysis:** Use `knowledge_core/dependency_graph.json` to identify dependencies.

### FDC Phase 3: Planning & Self-Correction
- **Plan Generation:** Generate a detailed, step-by-step execution plan.
- **Plan Validation:** Validate the plan using `python tooling/fdc_cli.py validate <plan_file>`.
- **Plan Analysis:** Analyze the plan's complexity and modality using `python tooling/fdc_cli.py analyze <plan_file>`.
- **Evidence Citation:** Justify each step with a citation to internal or external evidence.
- **Critical Review:** Engage the internal critic to verify the plan against the evidence.

### FDC Phase 4: Execution & Structured Logging
- **Execute Plan:** Execute the validated plan step-by-step.
- **Structured Logging:** Record every action in `logs/activity.log.jsonl`.

### FDC Phase 5: Pre-Submission Post-Mortem
- **Initiate Task Closure:** Use `python tooling/fdc_cli.py close --task-id ...` to create the post-mortem artifact.
- **Complete Report:** Fill out the generated post-mortem report.
- **Proceed to Submission:** The `submit` action must include all code and the completed post-mortem.

### STANDING ORDER - RAG MANDATE
For any task requiring external information, the agent is REQUIRED to use the `execute_research_protocol` tool with the appropriate constraints to retrieve up-to-date information. Failure to do so is a critical error.