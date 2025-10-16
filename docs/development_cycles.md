# A Generalized View of Development Cycles and Context-Sensitive Protocols

## Introduction

This document provides a comprehensive overview of the formal development cycles that govern the agent's operation. These cycles are not arbitrary workflows; they are rigorously defined processes based on models from formal language theory and computability theory. They provide a robust framework for ensuring that the agent's actions are predictable, verifiable, and guaranteed to terminate.

The architecture has evolved through several stages, each increasing in expressive power and sophistication while carefully managing the risks of paradox and non-termination:
1.  **Finite Development Cycle (FDC):** The foundational layer, ensuring basic decidability.
2.  **Context-Free Development Cycle (CFDC):** An extension that enables modular, hierarchical planning.
3.  **Context-Sensitive Development Cycle (CSDC):** The most advanced layer, which introduces logical constraints and self-awareness.

This document will first explain the fundamental concepts of Finite State Machines and Transducers, then detail each development cycle, and finally generalize the underlying concepts to context-sensitive protocols, toolchains, and the distinction between symmetric and asymmetric cycles.

---

## 1. Fundamental Concepts: FSMs and FSTs

### Finite State Machine (FSM)

A **Finite State Machine (FSM)**, or Finite Automaton, is a mathematical model of computation. It is an abstract machine that can be in exactly one of a finite number of *states* at any given time. The FSM can change from one state to another in response to some inputs; the change from one state to another is called a *transition*. An FSM is defined by a list of its states, its initial state, and the conditions for each transition.

FSMs are fundamental to the agent's design because they are inherently **decidable**. Since they have a finite number of states and no external memory, it is mathematically impossible for a true FSM to enter an infinite loop. This property is crucial for guaranteeing that the agent's core processes will always terminate.

### Finite-State Transducer (FST)

A **Finite-State Transducer (FST)** is a type of finite automaton that produces output. It is similar to an FSM, but with the addition of an output tape. For each transition, the FST can both change state and write to its output tape. This allows an FST to *transduce* an input sequence into an output sequence.

While not as explicitly implemented as FSMs in the core development cycles, the concept of an FST is relevant to understanding how the agent interacts with its environment. For example, the `protocol_compiler.py` can be viewed as an FST: it takes a set of protocol files (`.protocol.json`) as input and produces a compiled `AGENTS.md` file as output.

---

## 2. The Finite Development Cycle (FDC): Guaranteeing Termination

The FDC is the simplest and most fundamental execution model in the system.

-   **Concept:** A linear, sequential workflow designed to execute a flat list of commands. Its primary purpose is to provide an absolute guarantee that any plan will terminate.

-   **Theoretical Model:** **Finite State Machine (FSM)**, also known as a Finite Automaton. An FSM has a finite number of states and no external memory. This inherent limitation is its greatest strength: it is mathematically impossible for a true FSM to enter an infinite loop. This makes the FDC a highly reliable and predictable foundation.

-   **Implementation:**
    -   **FSM Definition:** The FDC is governed by the FSM defined in `tooling/fdc_fsm.json`. This file explicitly lists all possible states (`IDLE`, `PLANNING`, `EXECUTING`, etc.) and the valid transitions between them based on an "alphabet" of actions (`plan_op`, `step_op`, `write_op`, etc.).
    -   **CLI Interface:** The primary interface for this cycle is `tooling/fdc_cli.py`. This tool's `validate` command parses a plan and simulates its execution against the FSM, ensuring every step corresponds to a valid transition. If any command would cause an invalid transition, the entire plan is rejected before execution.

---

## 3. The Context-Free Development Cycle (CFDC): Enabling Modularity

The CFDC evolved from the FDC to overcome its main limitation: the inability to handle nested or reusable logic.

-   **Concept:** A hierarchical planning model that allows one plan to call another as a sub-routine. This enables the creation of complex, modular, and reusable plans.

-   **Theoretical Model:** **Pushdown Automaton**. This model extends the FSM by adding a single stack for memory. This stack is the key mechanism that allows for nested "function calls" (sub-plan executions). When a sub-plan is called, the state of the parent plan is pushed onto the stack. When the sub-plan completes, the parent's state is popped, and execution resumes.

-   **Implementation:**
    -   **`call_plan` Directive:** The core of the CFDC is the `call_plan` command. This directive instructs the execution engine to pause the current plan, execute a different one, and then return.
    -   **Decidability Guarantee:** Unbounded recursion in a Pushdown Automaton could lead to non-termination (if the stack can grow infinitely). To prevent this, the CFDC enforces a `MAX_RECURSION_DEPTH` constant. This hard limit on the stack depth ensures the system remains a **decidable process** that is guaranteed to halt.
    -   **Plan Registry:** To make plans more modular and robust, the `knowledge_core/plan_registry.json` was introduced. This acts as a service locator, mapping logical plan names (e.g., `"run-all-tests"`) to their physical file paths. This decouples the caller from the callee, allowing plans to be moved or updated without breaking all dependencies.

---

## 4. The Context-Sensitive Development Cycle (CSDC): Introducing Logical Constraints

The CSDC represents a significant leap in sophistication. It moves beyond validating the *structure* of a plan to validating its *logical content* within a specific context.

-   **Concept:** A development cycle that operates under different, mutually exclusive sets of logical rules. It is designed to explore the trade-off between expressive power and the risk of self-referential paradoxes (inspired by Gödel's Incompleteness Theorems and Tarski's Undefinability Theorem).

-   **Theoretical Model:** **Linear Bounded Automaton (LBA)**. An LBA is a Turing Machine whose tape is restricted to the length of the input. This model is "context-sensitive" because its transition rules can depend on the entire input (the plan), not just the current state and command. The presence of `tooling/lba_validator.py` confirms this theoretical underpinning.

-   **Implementation:** The CSDC is built around two competing logical models:
    -   **Model A (Introspective):** Permits the agent to have a complete map of its own language (`define_set_of_names`) but forbids the function that enables direct self-reference (`define_diagonalization_function`). This allows for powerful metaprogramming while avoiding paradox.
    -   **Model B (Self-Referential):** Permits the agent to use the self-referential function (`define_diagonalization_function`) but forbids it from having a complete name-map of its own language (`define_set_of_names`). This allows for direct self-reference by preventing the agent from fully describing itself.
    -   **Enforcement:** The `tooling/csdc_cli.py` tool is the gateway for this cycle. It validates a plan against a specified model (`--model A` or `--model B`) and a computational complexity class (`--complexity P` or `--complexity EXP`), ensuring the plan's logic adheres to the chosen context.

---

## 5. Generalization and Advanced Concepts

### Context-Sensitive Protocols and Toolchains

-   **Context-Sensitive Protocols:** These are protocols whose rules depend on the state or properties of the system, rather than being fixed. The CSDC is the primary example, where the validity of a plan is sensitive to the logical "context" (Model A or B). Another example is the `toolchain-audit-on-schema-change` protocol, which is only triggered by the specific context of a change to the core protocol schema.

-   **Context-Sensitive Toolchains:** This refers to a toolchain where the behavior or availability of tools changes based on the operational context. The `csdc_cli.py` is a context-sensitive tool because its validation logic is determined by the `--model` argument. Similarly, the agent's main orchestrator (`master_control.py`) acts in a context-sensitive way when it invokes a specialized FSM, like the `research_fsm.json`, in response to a task that requires deep knowledge acquisition.

### Symmetric vs. Asymmetric Cycles

-   **Symmetric Cycles:** These are cycles where the operational rules are uniform and consistent throughout the process. The basic FDC is largely symmetric; the rules for executing steps do not change from one step to the next.

-   **Asymmetric Cycles:** These are cycles where the rules are not uniform or where constraints change depending on the path taken.
    -   The **CFDC** introduces a fundamental asymmetry with its stack-based `call_plan` (push) and `return` (pop) operations.
    -   The **CSDC** is inherently asymmetric. A plan that is valid in Model A is invalid in Model B. The choice of model at the start establishes an asymmetric set of rules for the entire validation process.
    -   **Speculative Execution** is another example. The rules governing this cycle (e.g., requiring a formal proposal, gating output behind user review) are completely different from the standard development cycle, creating a powerful asymmetry based on the initial context (idle state vs. user request).