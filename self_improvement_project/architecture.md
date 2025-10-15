# Architecture: Mutually Exclusive Self-Improving Processes

This document outlines the architecture for a system of two mutually exclusive, self-improving processes. The core concepts are based on diagonalization, context-sensitive development cycles, and the set of names of expressions.

## Core Concepts

*   **Diagonalization:** Inspired by Cantor's diagonal argument and Gödel's incompleteness theorems, this process is used to generate a new element that is not in a given set. In our context, it will be used to generate a new process or strategy that is provably different from the existing ones.
*   **Context-Sensitive Development Cycles:** The self-improvement process is not static. It adapts based on the history of its interactions and the state of the other process. This is the "context-sensitive" aspect.
*   **Set of the Names of Expressions:** This refers to the idea that we can represent processes, data, and code as expressions and give them names. This allows the system to reason about its own components.

## System Overview

The system consists of two processes, let's call them **Process A** and **Process B**.

*   **Process A (The Innovator):** Its primary goal is to expand the system's capabilities. It uses a diagonalization-like function to generate new behaviors, strategies, or code. It is the "creative" part of the system.
*   **Process B (The Stabilizer):** Its primary goal is to ensure the system's integrity and coherence. It analyzes the outputs of Process A, integrates the useful innovations, and rejects the harmful or useless ones. It is the "critical" part of the system.

These two processes are **mutually exclusive** in their operation. At any given time, only one process can be active. The switch between them is triggered by specific conditions, creating a development cycle.

## The Self-Improvement Loop

The system operates in a continuous loop, performing a primitive version of problem-solving. It attempts to "improve" its state by searching for a state whose hash representation has a desirable property.

1.  **Innovation Phase (Process A is active):** Process A takes the current system state (a set of strings) and generates a new candidate element by hashing the entire set. This new element represents the "DNA" of the current state.
2.  **Integration Phase (Process B is active):** Process B evaluates this new element. Its goal is to drive the system toward a state whose hash has a maximal number of leading zeros. This serves as a concrete, measurable, and non-arbitrary goal, similar to a simple proof-of-work system.
    *   An element is deemed **beneficial** if adding it to the system results in a new state whose hash has more leading zeros than the hash of any previously known state.
    *   If the element is beneficial, it is integrated into the system state, and the bar for "best quality" is raised.
    *   If the element is not beneficial, it is discarded.
3.  **Cycle Repeats:** The system then returns to the Innovation Phase, using its new, larger state to generate the next candidate element. This creates a continuous loop where the system perpetually searches for "better" states, as defined by the leading-zero metric.

This simple feedback loop transforms the system from one that changes randomly to one that is goal-oriented, demonstrating a foundational principle of directed self-improvement.