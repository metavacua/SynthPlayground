# Protocol: The Context-Sensitive Development Cycle (CSDC)

This protocol introduces a new form of development cycle that is sensitive to the logical context in which it operates. It moves beyond the purely structural validation of the FDC and CFDC to incorporate constraints based on fundamental principles of logic and computability.

The CSDC is founded on the idea of exploring the trade-offs between expressive power and the risk of self-referential paradoxes. It achieves this by defining two mutually exclusive development models.

## Model A: The Introspective Model

- **Permits:** `define_set_of_names`
- **Forbids:** `define_diagonalization_function`

This model allows the system to have a complete map of its own language, enabling powerful introspection and metaprogramming. However, it explicitly forbids the diagonalization function, a common source of paradoxes in self-referential systems. This can be seen as a Gödel-like approach.

## Model B: The Self-Referential Model

- **Permits:** `define_diagonalization_function`
- **Forbids:** `define_set_of_names`

This model allows the system to define and use the diagonalization function, enabling direct self-reference. However, it prevents the system from having a complete name-map of its own expressions, which is another way to avoid paradox (related to Tarski's undefinability theorem).

## Complexity Classes

Both models can be further constrained by computational complexity:
- **Polynomial (P):** For plans that are considered computationally tractable.
- **Exponential (EXP):** For plans that may require significantly more resources, allowing for more complex but potentially less efficient solutions.

## The `csdc_cli.py` Tool

The CSDC is enforced by the `tooling/csdc_cli.py` tool. This tool validates a plan against a specified model and complexity class, ensuring that all constraints are met before execution.