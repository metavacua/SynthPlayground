# Protocol: The Context-Sensitive Development Cycle (CSDC)

This protocol introduces a development cycle that is sensitive to the logical context in which it operates, incorporating constraints based on principles of logic and computability. It defines two mutually exclusive development models (A and B) that trade off expressive power against the risk of self-referential paradoxes. The `tooling/csdc_cli.py` tool validates plans against a specified model and complexity class (P or EXP).

## Model A: The Introspective Model
- **Permits:** `define_set_of_names`
- **Forbids:** `define_diagonalization_function`

## Model B: The Self-Referential Model
- **Permits:** `define_diagonalization_function`
- **Forbids:** `define_set_of_names`