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

This new protocol provides a robust, reliable, and formally verifiable mechanism for the agent to explore complex topics, making it significantly more autonomous and capable.# Protocol: Deep Research Cycle

This protocol defines a standardized, multi-step plan for conducting in-depth research on a complex topic. It is designed to be a reusable, callable plan that ensures a systematic and thorough investigation.

The cycle consists of five main phases:
1.  **Review Scanned Documents:** The agent first reviews the content of documents found in the repository during the initial scan. This provides immediate, project-specific context.
2.  **Initial Scoping & Keyword Generation:** Based on the initial topic and the information from scanned documents, the agent generates a set of search keywords.
3.  **Broad Information Gathering:** The agent uses the keywords to perform broad web searches and collect a list of relevant URLs.
4.  **Targeted Information Extraction:** The agent visits the most promising URLs to extract detailed information.
5.  **Synthesis & Summary:** The agent synthesizes the gathered information into a coherent summary, which is saved to a research report file.

This structured approach ensures that research is not ad-hoc but is instead a repeatable and verifiable process.