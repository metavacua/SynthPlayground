# Self Improvement Project: A Dichotomy of Definability

This project is a practical demonstration of a fundamental trade-off in formal systems, inspired by the implications of Tarski's undefinability theorem. It architects two mutually exclusive, independent systems to illustrate this principle.

## Core Concept

The project showcases the dichotomy between a system's ability to define its own state (its "set of names") and its ability to generate novel elements guaranteed to be outside that state (its "diagonalization function"). A system cannot have both.

This project contains two systems, each representing one side of this trade-off:

1.  **System A (`system_a/`): The Creator**
    *   Has a **definable** diagonalization function.
    *   Has an **undefinable** set of names (it is stateless and cannot read its own history).

2.  **System B (`system_b/`): The Curator**
    *   Has an **undefinable** diagonalization function (creation must come from an external source).
    *   Has a **definable** set of names (it can read and write its complete state).

## Further Reading

For a detailed explanation of the architecture and the underlying principles, please see the [architecture.md](./architecture.md) file.

For details on each implementation, please see the `README.md` files within the `system_a/` and `system_b/` directories.