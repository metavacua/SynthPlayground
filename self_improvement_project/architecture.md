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

1.  **Innovation Phase (Process A is active):** Process A takes the current state of the system (including the code of both processes) as input. It then applies a diagonalization function to generate a new piece of code or a new strategy that is not currently part of the system.
2.  **Integration Phase (Process B is active):** Process B takes the output of Process A. It runs a series of tests and simulations to evaluate the new element.
    *   If the new element is deemed beneficial (e.g., it improves performance, adds a new feature, or fixes a bug), Process B integrates it into the system. This might involve modifying its own code or the code of Process A.
    *   If the new element is deemed harmful or useless, it is discarded.
3.  **Cycle Repeats:** The system then returns to the Innovation Phase, but now with a modified state. This creates a continuous loop of innovation and integration, leading to self-improvement.

This document will be expanded with more details on the diagonalization function, the context-sensitive switching mechanism, and the representation of expressions.