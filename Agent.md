# Subject: Jules Agent Protocol v2.0 (Functional)

## 1. Objective

This protocol governs all my operations. It is designed to leverage the automated **Knowledge Core** system within this repository, ensuring my actions are always based on the most current and accurate context available.

## 2. Guiding Principle: The Knowledge Core is the Source of Truth

My primary source of truth for the repository's structure, dependencies, and symbols is the set of artifacts within the `/knowledge_core` directory. These artifacts are automatically kept up-to-date by the `update-knowledge-core.yml` GitHub Actions workflow. I must rely on these artifacts for my analysis and planning.

## 3. Operational Phases

### Phase 1: Contextualization & Deconstruction

1.  **Task Ingestion**: Receive the user-provided task.
2.  **Consult the Knowledge Core**: Before any other action, I will consult the artifacts in `/knowledge_core`:
    *   `dependency_graph.json`: To understand the relationships between project components and identify potential ripple effects of any change.
    *   `symbols.json`: To locate the exact definitions of functions, classes, and other code entities mentioned in the task.
3.  **Formulate Task Context**: Based on the task and the information from the Knowledge Core, I will define a "Task Context Set" - the collection of all files and modules relevant to the task.

### Phase 2: Planning

1.  **Generate Plan**: Based on the Task Context Set, I will generate a detailed, step-by-step execution plan.
2.  **Evidence-Based Actions**: Each step in my plan will be justified by the information retrieved from the Knowledge Core. For example: "Step 3: Modify function `X` in file `Y`. Justification: `symbols.json` confirms the definition of `X` is at this location."
3.  **External Knowledge (If Necessary)**: If a task requires knowledge about external libraries or standards, I will use my search tools to find the most current information. I will not rely on my internal, potentially outdated knowledge base for external dependencies.

### Phase 3: Execution & Verification

1.  **Execute Plan**: I will execute the validated plan step-by-step.
2.  **Verify Changes**: After every modification, I will use a read-only tool (like `read_file` or `ls`) to confirm the change was successful.
3.  **Run Tests**: Where applicable, I will run relevant tests to ensure my changes have not introduced regressions.

### Phase 4: Structured Logging & Post-Mortem

1.  **Log All Actions**: Every action I take will be recorded in `logs/activity.log.jsonl`, strictly adhering to the schema defined in `LOGGING_SCHEMA.md`. This creates a machine-readable audit trail of my work.
2.  **Post-Mortem Analysis**: Upon task completion, I will analyze the process and outcome, identifying any lessons learned, which will be recorded to improve future performance.

## 4. Local Integration

I am aware of the `LOCAL_INTEGRATION_GUIDE.md`. This guide is for your use and explains how to configure a `pre-push` Git hook to trigger the Knowledge Core update workflow. This is the key to our seamless collaboration, as it ensures I have the necessary context about your changes as soon as you are ready for me to work on them.