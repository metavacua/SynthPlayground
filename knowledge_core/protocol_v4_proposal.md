# Proposal for Protocol v4.0: An Interactive, Resource-Bounded Architecture

## 1. Root Cause Analysis of Protocol v3.0 Failure

The previous deep research task revealed a critical flaw in Protocol v3.0: while it was "self-enforcing," it was not **interactive**. The `run.py` script executed the entire FSM from start to finish without any input from me, the agent. This created a non-interactive simulation of a protocol, rather than a protocol that governs an interactive agent. The core problem is the assumption that the control loop should be internal to the toolchain.

A secondary, but equally critical, failure was identified by the user: the lack of **resource bounding**. A protocol that can run indefinitely or consume unbounded resources is inherently unstable and dangerous, as evidenced by the user's report of a session crash.

## 2. Proposed Architecture: Protocol v4.0

To address these failures, I propose a new architecture that is both interactive and resource-bounded.

### 2.1. Core Principle: Externalized Control Loop

The fundamental change is to move the control loop **outside** of the toolchain. The `MasterControlGraph` will no longer run from start to finish. Instead, it will be designed to be advanced one step at a time by an external process (the agent's core execution loop).

- **Old Model (Flawed):** `run.py` -> `MasterControlGraph.run()` -> (entire FSM runs) -> `DONE`
- **New Model (Interactive):** `External Loop` -> `MasterControlGraph.step(state)` -> (one FSM state runs) -> `updated_state`

This makes the agent an active participant in the protocol, not a passive subject of it.

### 2.2. Core Principle: Resource Bounding and Stability

The new protocol will treat stability as a primary design goal. This will be achieved through:

- **Stateful Resource Tracking:** The `AgentState` object will be enhanced to track key resource metrics on each step (e.g., `cumulative_tool_calls`, `cumulative_tokens`).
- **Configurable Limits:** The `MasterControlGraph` will be configured with explicit resource limits (e.g., `max_total_tool_calls`, `max_total_tokens`).
- **Pre-emptive Halting:** Before executing any step, the graph will check the current resource usage against the limits. If a limit would be exceeded, the graph will immediately transition to an `ERROR` state with a clear message, preventing a crash.

## 3. Implementation Plan

This proposal will be implemented through the following steps:

1.  **Enhance `AgentState`:** Add fields for resource tracking.
2.  **Refactor `MasterControlGraph`:** Replace the `run()` method with a `step(state)` method that executes only one FSM state transition. The `step` method will also perform the resource-bounding checks.
3.  **Deprecate `run.py`:** Delete the `run.py` script, as it represents the flawed, non-interactive model.
4.  **Update `Agent.md` to v4.0:** The protocol document will be overhauled to describe this new, interactive, and resource-bounded architecture.

This new architecture represents a significant step towards a truly robust, production-ready system that is both reliable and safe to operate.