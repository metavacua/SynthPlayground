# Architecture: A Dichotomy of Definability

## Core Principle: The Robinson-Tarski Trade-off

This architecture is designed to demonstrate a fundamental trade-off inspired by the implications of Tarski's undefinability theorem. The core idea is that a formal system cannot have it all: there is an inherent conflict between being able to fully describe its own state (its "set of names") and being able to generate novel elements that are guaranteed to be outside that state (the "diagonalization function").

This leads to a dichotomy, which is modeled here by two mutually exclusive and independent systems:

1.  **System A:** The set of names is **undefinable** from within, but the diagonalization function is **definable**.
2.  **System B:** The diagonalization function is **undefinable** from within, but the set of names is **definable**.

These two systems are not meant to interact. They are parallel universes, each illustrating one side of this fundamental logical limitation. Their consistency is guaranteed by what they *exclude*.

---

## System A: The Creator Who Cannot Know Itself

*   **Directory:** `system_a/`
*   **Principle:** This system has a clear, well-defined internal process for creating new expressions (a definable diagonalization function).
*   **Limitation:** It is fundamentally **stateless**. It logs its output to a history file, but it has no internal mechanism to read or comprehend that history. Therefore, its complete "set of names" (its own historical output) is **undefinable** from within the system's own logic. It can always create, but it can never be self-aware of the totality of its creations.

---

## System B: The Curator Who Cannot Create

*   **Directory:** `system_b/`
*   **Principle:** This system has a perfect, well-defined understanding of its own state. It maintains a `state.json` file which it can read, write, and validate against. Its "set of names" is **definable**.
*   **Limitation:** It has no internal function for creating new elements. The diagonalization function is **undefinable** from within the system. To introduce a new element, a user must provide one externally (e.g., via a command-line argument). The system can only curate—it can check if the new element is truly novel and then add it to its state, but it cannot innovate on its own.