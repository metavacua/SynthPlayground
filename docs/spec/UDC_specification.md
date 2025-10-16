# Formal Specification: The Unrestricted Development Cycle (UDC)

**Status:** `speculative`, `draft`
**Version:** 0.1.0
**Author:** Jules

## 1. Abstract

This document provides the formal technical specification for the Unrestricted Development Cycle (UDC), a new agent execution model based on a Turing Machine. It details the conceptual architecture, the syntax and semantics of the UDC plan language, the design of the UDC Orchestrator, and the critical risk mitigation strategies required for its safe operation.

## 2. Introduction

### 2.1. Purpose

The existing development cycles (FDC, CFDC, CSDC) are designed to be decidable and guaranteed to halt. This provides a crucial safety guarantee but fundamentally limits the agent's problem-solving capabilities to tasks within specific complexity classes (Finite, Context-Free, Context-Sensitive).

The purpose of the UDC is to transcend these limits by providing a framework for executing **Turing-complete** plans. This will enable the agent to tackle problems that are not guaranteed to be decidable, such as complex simulations, advanced self-modification, and tasks requiring unbounded algorithmic loops.

### 2.2. Core Concept

The UDC represents a controlled transition from the Linear Bounded Automata of the CSDC to a full, standard Turing Machine. It is not intended to replace the safer, decidable cycles but to exist alongside them as a specialized, high-risk, high-reward option for tasks that demand unrestricted computational power.

## 3. Conceptual Architecture

The UDC is modeled as a standard, single-tape Turing Machine with the following components:

*   **Infinite Tape:** A one-dimensional tape of cells, infinite in both directions. In practice, this is implemented as a dynamically allocated memory buffer (e.g., a Python dictionary or a list that can grow). Each cell can hold a single symbol from a finite alphabet.
*   **Read/Write Head:** A conceptual head that can read a symbol from a tape cell, write a new symbol to it, and move one cell to the left or right at each step.
*   **State Register:** A register holding the current state of the machine. At a minimum, this includes `RUNNING`, `HALTED`, and `ERROR`.
*   **Transition Function:** The "program" of the Turing Machine. It is defined by the UDC plan, which specifies, for a given state and symbol under the head, what symbol to write, what direction to move the head, and what the next state should be.

## 4. UDC Plan Language

UDC plans are text files with a `.udc` extension. The language is a line-based, low-level assembly-like language designed for simplicity and direct mapping to Turing Machine operations.

### 4.1. Syntax

Each line consists of an instruction followed by zero or more arguments, separated by spaces. Comments are denoted by a `#` character.

`INSTRUCTION [ARG1] [ARG2] # This is a comment`

### 4.2. Registers

The UDC provides a small set of general-purpose registers for computation:
*   `R0`, `R1`, `R2`, `R3`: General-purpose registers for storing integer values.
*   `IP`: Instruction Pointer (managed by the orchestrator).
*   `SP`: Stack Pointer (for `CALL` and `RET` instructions).

### 4.3. Core Instructions

*   **Tape Operations:**
    *   `LEFT`: Move the tape head one position to the left.
    *   `RIGHT`: Move the tape head one position to the right.
    *   `READ <reg>`: Read the value from the tape cell at the current head position and store it in `<reg>`.
    *   `WRITE <val>`: Write a value to the tape cell at the current head position. `<val>` can be a literal integer or the value from a register.

*   **Data Movement:**
    *   `MOV <dest_reg> <src>`: Move a value from `<src>` to `<dest_reg>`. `<src>` can be a literal integer or a source register.

*   **Arithmetic:**
    *   `ADD <reg> <val>`: `reg = reg + val`. `<val>` can be a literal or a register.
    *   `SUB <reg> <val>`: `reg = reg - val`. `<val>` can be a literal or a register.
    *   `INC <reg>`: `reg = reg + 1`.
    *   `DEC <reg>`: `reg = reg - 1`.

*   **Control Flow:**
    *   `LABEL <name>`: Defines a target for jump instructions. Does nothing on its own.
    *   `JMP <label>`: Unconditionally jump to the instruction following `<label>`.
    *   `CMP <reg1> <val>`: Compare `<reg1>` with `<val>` (literal or register) and set internal flags for conditional jumps.
    *   `JE <label>`: Jump to `<label>` if the result of the last `CMP` was equal.
    *   `JNE <label>`: Jump to `<label>` if the result of the last `CMP` was not equal.
    *   `JG <label>`: Jump to `<label>` if `reg1` was greater than `val`.
    *   `JL <label>`: Jump to `<label>` if `reg1` was less than `val`.

*   **Execution and External Calls:**
    *   `HALT`: Terminates the UDC plan successfully.
    *   `CALL <tool_name> [args...]`: Make a sandboxed call to a pre-approved, safe agent tool.
    *   `RET`: Return from a `CALL` (for future use if UDC plans can call other UDC plans).

## 5. UDC Orchestrator (`tooling/udc_orchestrator.py`)

The orchestrator is the runtime environment that executes UDC plans. It is the most critical component for ensuring safety.

### 5.1. Responsibilities

1.  **Parsing:** Read a `.udc` file and parse it into an internal instruction list, validating syntax and resolving labels.
2.  **Initialization:** Set up the virtual Turing Machine environment: initialize the tape, registers, and instruction pointer.
3.  **Execution Loop:** Fetch, decode, and execute instructions sequentially, handling state transitions and head movements.
4.  **Lifecycle Management:** Manage the entire execution from start to `HALT`, `ERROR`, or forced termination.

### 5.2. Safety Mechanisms (Non-Negotiable)

The orchestrator **MUST** implement the following safety mechanisms to mitigate the risks of Turing-complete execution:

1.  **Instruction Count Limit:** A configurable limit on the total number of instructions executed. If this limit is exceeded, the orchestrator **MUST** terminate the plan with a `TIMEOUT_INSTRUCTION_LIMIT` error. This is the primary defense against infinite loops.
2.  **Memory Usage Limit:** A configurable limit on the maximum size of the tape buffer (both positive and negative indices). If the plan attempts to `WRITE` to a cell that would exceed this limit, it **MUST** be terminated with a `TIMEOUT_MEMORY_LIMIT` error.
3.  **Wall-Clock Time Limit:** A hard time limit for the entire execution process. If the wall-clock time exceeds this limit, the process **MUST** be terminated.
4.  **Tool Call Sandboxing:** The `CALL` instruction **MUST NOT** have direct access to the agent's full toolset. It must route requests through a sandbox that only permits a pre-approved list of safe, read-only, and computationally inexpensive tools. Any file system or network access is strictly forbidden by default.

## 6. Halting Heuristic Analyzer (`tooling/halting_heuristic_analyzer.py`)

### 6.1. Purpose

Since the Halting Problem is undecidable, we cannot know with certainty if an arbitrary UDC plan will terminate. The Halting Heuristic Analyzer's purpose is to provide a **non-binding, probabilistic risk assessment** *before* execution.

### 6.2. Analysis Techniques

The analyzer will perform static analysis on the UDC plan's source code to identify patterns indicative of non-halting behavior.

1.  **Loop Detection:** Identify all backward jumps, which are the building blocks of loops.
2.  **Loop Exit Condition Analysis:** For each detected loop, analyze the loop's body to find the `CMP` and conditional jump instructions that control its exit. Attempt to determine if the variable being checked is monotonically changed in a way that guarantees the exit condition will eventually be met.
    *   **Example of a "safe" pattern:** A register is initialized to 10, the loop condition is `JNE` on zero, and the register is decremented by 1 on every iteration with no other modifications.
    *   **Example of a "risky" pattern:** The exit condition depends on a value read from the tape or the result of a tool call, which cannot be known statically.
3.  **Unbounded Recursion:** This version of the spec does not include self-calling plans, but this would be a necessary check in future versions.

### 6.3. Output

The analyzer will produce a JSON report with the following fields:
*   `estimated_risk`: A string (`LOW`, `MEDIUM`, `HIGH`, `UNKNOWN`).
*   `reason`: A human-readable explanation for the assessment.
*   `potential_infinite_loops`: A list of detected loops with their start/end lines and the reason they are considered risky.

## 7. Security and Risk Mitigation Summary

The UDC is inherently dangerous. Its use must be treated with extreme caution.
1.  **Primary Defense:** The Orchestrator's hard limits on instructions, memory, and time are the most important safeguards.
2.  **Secondary Defense:** The Halting Heuristic Analyzer provides a pre-execution "smell test" to inform the user or policy engine.
3.  **Tertiary Defense:** Strict sandboxing of tool calls (`CALL`) is essential to prevent a UDC plan from having unintended, destructive side effects on the host system. The UDC must be a "virtual machine" in the truest sense, isolated from its environment.