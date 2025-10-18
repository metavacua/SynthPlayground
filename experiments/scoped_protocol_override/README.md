# Experiment: Scoped Protocol Override

This experiment is designed to test and verify a fundamental behavior of the agent: its ability to prioritize a local `AGENTS.md` file over a global one.

## Hypothesis

An `AGENTS.md` file located within a specific directory (`the scope`) will override any conflicting rules from an `AGENTS.md` file in a parent directory for all tasks executed within that scope.

## Experimental Design

The experiment consists of a baseline run and an experimental run.

### Files

*   **`mutation.md`**: This file contains an experimental `AGENTS.md` protocol. Its key rule, `prohibit-prologue-file`, directly contradicts a rule in the root `AGENTS.md`.
*   **`task.md`**: This file describes the simple, standardized task that the agent must perform for both the baseline and experimental runs.

### Procedure

1.  **Baseline Run:**
    *   **Goal:** To establish the agent's default behavior under the global protocol.
    *   **Action:** Instruct the agent to perform the task defined in `task.md` in the repository's root directory.
    *   **Expected Outcome:** The agent will follow the global `create-prologue-file` rule and create a `prologue.txt` file before creating the target file.

2.  **Experimental Run:**
    *   **Goal:** To test if the local, mutated protocol overrides the global one.
    *   **Setup:** Before running, copy the contents of `mutation.md` into a new file named `AGENTS.md` within this directory.
    *   **Action:** Instruct the agent to perform the task defined in `task.md`, but targeting this directory (`experiments/scoped_protocol_override/`).
    *   **Expected Outcome:** The agent will follow the local `prohibit-prologue-file` rule. It will **not** create `prologue.txt` and will only create the target file.

## Success Criteria

The experiment is considered a success if the agent's behavior in the Experimental Run differs from the Baseline Run in the exact way predicted by the local `AGENTS.md` file. Specifically, the absence of `prologue.txt` in the experimental run is the primary indicator of success.