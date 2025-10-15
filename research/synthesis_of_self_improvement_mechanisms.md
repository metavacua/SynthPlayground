# Synthesis of Agentic Self-Improvement Mechanisms

This document provides a preliminary synthesis of the core self-improvement mechanisms as described in the `AGENTS.md` protocols. The goal is to establish a conceptual baseline for the development of a formal theory of agentic self-improvement.

## 1. The Closed-Loop Self-Correction Cycle (PDSC)

- **Core Idea:** Transforms learning from a passive, documentation-based activity into an active, automated process. It closes the loop between identifying a problem and correcting the agent's governing protocols.
- **Mechanism:**
    1.  **Structured Lessons:** Post-mortem analysis generates structured `lessons.jsonl` entries, not free-form text. Crucially, these lessons contain an `action` field with a specific, machine-executable command.
    2.  **Protocol Updater Tool:** A dedicated tool (`tooling/protocol_updater.py`) exists to programmatically modify the source protocol files (`*.protocol.json`).
    3.  **Orchestrator:** A script (`tooling/self_correction_orchestrator.py`) reads the lessons, executes the embedded actions using the updater tool, and then recompiles the `AGENTS.md` file.
- **Implication:** This cycle represents a direct, explicit mechanism for self-improvement. The agent can modify its own "source code" (its protocols) in a verifiable and audited manner. This is a foundational element of any formal theory.

## 2. The Context-Free Development Cycle (CFDC)

- **Core Idea:** Moves the agent's planning and execution model from a simple Finite State Machine (FSM) to a Pushdown Automaton. This enables hierarchical and modular planning.
- **Mechanism:**
    1.  **Plan Stack:** The system maintains a stack of executing plans.
    2.  **`call_plan` Directive:** A plan can call another plan as a sub-routine. The current plan's state is pushed onto the stack, the sub-plan executes, and then the parent plan is popped and resumed.
    3.  **Decidability:** A `MAX_RECURSION_DEPTH` is strictly enforced to ensure the process always halts, making it a decidable system, not a Turing-complete one.
- **Implication:** The CFDC provides the agent with the ability to manage complexity. It can break down large problems into smaller, reusable sub-problems (plans). This modularity is a prerequisite for tackling complex self-improvement tasks. An improvement in a sub-plan automatically benefits all larger plans that call it.

## 3. Speculative Execution

- **Core Idea:** Empowers the agent to engage in creative, self-directed, and exploratory work when it is idle. This is the agent's "imagination."
- **Mechanism:**
    1.  **Idle-State Trigger:** Can only be invoked when no user-assigned task is active.
    2.  **Formal Proposal:** Must begin by generating a proposal document outlining the goal and plan.
    3.  **Resource Constraints:** Operates under strict resource limits.
    4.  **User Review Gate:** The final output cannot be integrated directly; it must be presented to the user for approval.
- **Implication:** This protocol allows for non-deterministic, creative leaps. While the other cycles are about directed correction or execution, this is about generating novel ideas and artifacts. It's a source of new hypotheses for the agent to test and potentially integrate through its other self-improvement mechanisms.

## 4. The Formal Research Cycle (L4)

- **Core Idea:** Elevates research from an ad-hoc tool call to a formal, verifiable, multi-step process.
- **Mechanism:**
    1.  **Specialized FSM:** Uses a dedicated FSM for research with states like `GATHERING`, `SYNTHESIZING`, and `REPORTING`.
    2.  **Executable Plans:** Generates formal, executable research plans.
    3.  **Formal Invocation:** The main agent orchestrator can formally invoke this cycle to acquire knowledge needed for a task.
- **Implication:** This provides the agent with a robust mechanism for increasing its knowledge base in a structured way. Since knowledge is a key component of capability, this is a fundamental pillar of self-improvement. It is the process by which the agent learns about the world and itself.

## Overall Synthesis

These four protocols form a comprehensive system for agentic self-improvement:
- **The Research Cycle** gathers new knowledge.
- **Speculative Execution** generates novel hypotheses and plans.
- **The CFDC** allows the agent to execute complex, hierarchical plans based on this knowledge.
- **The Self-Correction Cycle** allows the agent to integrate what it has learned directly into its core operational rules.

Together, they create a feedback loop: The agent can research a topic, speculate on a better way to operate, formulate a complex plan to implement that change, and then formally update its own protocols to make that change permanent. This is the foundation upon which a formal theory can be built.