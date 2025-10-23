# Phase 2

Deconstruction & Internal Contextualization
Task Ingestion: Receive the user-provided task.

Entity Identification: Identify all candidate code entities (functions, classes, modules, files) relevant to the task description. Perform a direct lookup against the knowledge_core/symbols.json artifact to resolve these candidates to concrete symbols and their exact locations (file path, line number).

Impact Analysis: Using the file paths identified in the previous step as a starting point, construct a dependency impact analysis. Query the knowledge_core/dependency_graph.json artifact to identify all immediate upstream dependents (code that will be affected by changes) and downstream dependencies (code that the target entities rely on). The complete set of all identified files constitutes the "Task Context Set."