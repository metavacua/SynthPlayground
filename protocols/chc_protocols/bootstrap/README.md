# Proposition: `AGENT-BOOTSTRAP-001`

This document defines the formal proposition for the `AGENT-BOOTSTRAP-001` protocol. In the Curry-Howard Correspondence, this proposition is a type, and any program that inhabits this type is a constructive proof of its truth.

## Type Signature

The type of the bootstrap protocol is a function that takes an initial, un-contextualized agent state and transforms it into a contextualized state, ready for task execution.

```
Bootstrap :: Un-contextualizedAgentState -> ContextualizedAgentState
```

## Preconditions (Antecedent)

For the bootstrap process to be valid, the following preconditions must hold:

1.  **Existence of `AGENTS.md`**: The repository root must contain a file named `AGENTS.md`.
    -   `exists(file: "AGENTS.md")`
2.  **Agent is in an initial state**: The agent must not have loaded any protocols or performed any actions related to the current task.
    -   `agent.state == "initial"`

## Postconditions (Succedent)

A successful execution of the bootstrap protocol (a valid proof) will result in a state where:

1.  **`AGENTS.md` is loaded**: The content of `AGENTS.md` has been read and loaded into the agent's active memory.
    -   `agent.protocols.is_loaded("AGENTS.md")`
2.  **Agent is in a contextualized state**: The agent's state has transitioned from "initial" to "contextualized".
    -   `agent.state == "contextualized"`
3.  **The plan is empty**: No plan has been formulated yet. Planning must occur *after* bootstrapping.
    -   `agent.plan.is_empty()`

## Invariants

Throughout the bootstrap process, the following invariants must be maintained:

1.  **No file modifications**: The bootstrap process is a read-only operation. No files in the repository may be modified, created, or deleted.
    -   `forall(file in repository) file.is_unmodified()`

## Proof

The constructive proof of this proposition is a program that, given an agent in the `Un-contextualizedAgentState`, demonstrably produces an agent in the `ContextualizedAgentState` while respecting all preconditions, postconditions, and invariants. The `proof.py` script in this directory is a candidate for this proof. The `check.py` script is the proof checker.
