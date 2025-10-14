# Research Report: Ambiguity in Agent Planning

**Date:** 2025-10-14
**Author:** Jules, AI Software Engineer

## 1. Introduction

This report examines the agent's planning system through the lens of formal language theory, specifically focusing on the distinction between ambiguous and unambiguous context-free grammars. The research was initiated to understand the risks associated with ambiguity in agent plans and to assess how the current system, the Context-Free Development Cycle (CFDC), mitigates these risks.

## 2. Key Concepts

A **context-free grammar (CFG)** is a set of rules used to generate patterns of strings. A grammar is considered **ambiguous** if there is at least one string (in our case, a plan) that can be generated in more than one way, resulting in multiple valid parse trees. In the context of an AI agent, an ambiguous plan could lead to non-deterministic or incorrect behavior, as the agent would have multiple valid ways to interpret the same set of instructions.

An **unambiguous grammar** ensures that every valid string has exactly one parse tree, guaranteeing a single, deterministic interpretation.

## 3. Analysis of the Agent's Planning System

The agent's planning system is a concrete and effective implementation of an unambiguous planning language. It achieves this through two primary mechanisms:

### 3.1. The FSM as a Deterministic Grammar

The core of the system's ability to prevent ambiguity is the Finite State Machine (FSM) defined in `tooling/fsm.json` and enforced by the validator within `tooling/master_control.py`. This FSM acts as a **deterministic grammar** for plans.

- **How it works:** Before execution, every plan is validated against the FSM. Each command in the plan is treated as a token that triggers a state transition. For any given state, a specific command can only lead to one possible next state. For example, from the `EXECUTING` state, the `read_file` command transitions back to the `EXECUTING` state. There is no other valid transition.
- **Effect:** This rigid state model ensures that any valid plan has exactly one sequential interpretation. Any plan that attempts to perform an action from an invalid state (e.g., calling `submit` before `plan_step_complete`) is rejected as syntactically incorrect. This is analogous to a compiler rejecting code that violates the programming language's grammar.

### 3.2. The Pushdown Automaton and Recursion Limit

The CFDC allows for hierarchical plans using the `call_plan` directive, which is managed by a plan stack, making the system a **Pushdown Automaton**. While this adds complexity, the system has a crucial safeguard against the most dangerous form of ambiguity this could introduce: infinite recursion.

- **Potential Risk:** A set of plans could be written to call each other in a circular dependency (e.g., Plan A calls Plan B, and Plan B calls Plan A). This would be a form of ambiguity where the plan's execution path is non-terminating.
- **Mitigation:** The `MAX_RECURSION_DEPTH` constant in `tooling/master_control.py` acts as a hard limit on the depth of the plan stack. If a chain of `call_plan` directives exceeds this limit, the execution is halted with an error. This doesn't detect the cycle beforehand but guarantees that the system will always halt, effectively preventing infinite loops and ensuring the planning language remains decidable.

## 4. Conclusion

The agent's planning system is robustly designed to prevent ambiguity. It does not rely on attempting to solve the undecidable problem of detecting ambiguity in an arbitrary grammar. Instead, it defines a **provably unambiguous subset of plans** through its strict, FSM-based validation.

The combination of a deterministic FSM for sequential plan validation and a hard recursion limit for hierarchical plans ensures that any valid plan has a single, deterministic, and finite execution path. The current architecture is sound and effectively mitigates the risks associated with ambiguity. No changes are recommended at this time.