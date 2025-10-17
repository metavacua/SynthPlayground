# Self Improvement Project: A Goal-Oriented System

This project demonstrates a foundational concept of self-improvement within a closed computational system. It features two competing processes, an "Innovator" and a "Stabilizer," that work together to evolve the system's state toward a specific, measurable goal.

## Purpose

The goal of this project is to serve as a minimal example of a goal-oriented, self-improving system. The system's "improvement" is defined by its ability to find a state whose hash representation has a maximal number of leading zeros. This turns the abstract idea of "improvement" into a concrete problem, similar to a proof-of-work system.

This project showcases the ability to:

*   Create a self-contained, abstract computational system.
*   Implement a non-arbitrary, goal-oriented feedback loop.
*   Write unit tests to verify the system's logic using mocking.
*   Maintain coherent documentation (`README.md`, `architecture.md`).

## How to run

To run the main program and observe the self-improvement loop:
```bash
python self_improvement_project/main.py
```

To run the tests:
```bash
python self_improvement_project/test_main.py
```