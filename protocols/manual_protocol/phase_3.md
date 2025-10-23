# Phase 3

Multi-Modal Information Retrieval (RAG)
Structural Retrieval (Internal): For every file in the Task Context Set, retrieve its corresponding Abstract Syntax Tree (AST) from the knowledge_core/asts/ directory. Use these ASTs to gain a deep, syntactic understanding of function signatures, call sites, data structures, and class hierarchies. This is your primary source for structural reasoning.

Conceptual Retrieval (Internal): Formulate a precise query based on the task description and the names of the primary entities involved. Execute this query against the `knowledge_core/enriched_protocols.ttl` artifact. This is your primary source for retrieving architectural principles and project-specific domain knowledge. The DBPedia links in this file should be used to expand your understanding of the concepts.

Just-In-Time External RAG: The temporal_orientation.md artifact provides a baseline. However, for the specific APIs or patterns required by the task, you MUST perform a targeted external search using your tools. The goal is to find the most current, official documentation and best-practice examples for the specific versions of the libraries you are working with. Do not rely on your internal knowledge.

The knowledge core contains the following structured information:
- **40** lessons learned from past tasks.
- **45** formal protocols defining agent behavior.
- **90** individual rules within those protocols.
- **2** research documents with key findings.
Knowledge Synthesis: Consolidate all retrieved information—internal symbols, dependencies, ASTs, project docs, and CRITICALLY, the up-to-date external documentation and standards—into a unified context briefing.