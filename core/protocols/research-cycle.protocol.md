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