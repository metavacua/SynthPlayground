# Witness: The Collatz Conjecture

This directory contains a concrete witness for the concept of "decidable refactoring," as proposed in the main `language_theory/THEORY.md` document. It separates the undecidable Collatz conjecture into two components:

1.  **`collatz_total.py`**: A **total function** that computes a single step of the Collatz sequence. It is guaranteed to terminate because it takes a "fuel" parameter that limits the number of steps.

2.  **`control_program.py`**: The **unbounded control logic** that orchestrates the Collatz sequence. This program is not guaranteed to terminate and represents the undecidable part of the problem.

This separation provides a practical example of how to isolate and manage undecidability in a formal system, which is a core concept of the theoretical model.
