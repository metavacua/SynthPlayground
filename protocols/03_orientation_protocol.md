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