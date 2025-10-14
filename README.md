# A Demonstration of a Resource-Sensitive Logic and its Extensions

This project provides a definitive implementation of a minimal, paraconsistent, and non-commutative core logic. The key feature of this logic is its strict adherence to resource sensitivity, meaning it does not have any structural rules like weakening (discarding information), contraction (duplicating information), or exchange (reordering information).

Provability in this system is determined by a recursive proof search based on a sequent calculus. A sequent is only provable if it can be reduced to an axiom of the form `A ⊢ A`.

## Project Structure

-   `logic.py`: A library containing the core components of the language:
    -   Data structures for propositions (`Atom`, `With`, `Plus`, etc.).
    -   A `prove(Γ, Δ)` function that implements the recursive proof search.

-   `base_interpreter.py`: The executable for the core logic, where sequents are of the form `A ⊢ B`.

-   `ci_interpreter.py`: An executable for a **Counter-Intuitionistic** fragment, where sequents are of the form `A ⊢ Γ`.

-   `i_interpreter.py`: An executable for an **Intuitionistic** fragment, where sequents are of the form `Γ ⊢ A`.

-   Example files (`*.pll`) are provided to demonstrate both provable and unprovable sequents.

## How to Run

Each interpreter can be run from the command line on an example file:

```bash
# Run the base logic interpreter
python3 base_interpreter.py provable_base.pll

# Run the counter-intuitionistic interpreter
python3 ci_interpreter.py provable_ci.pll

# Run the intuitionistic interpreter
python3 i_interpreter.py provable_i.pll

# Test an unprovable case
python3 i_interpreter.py unprovable_weakening.pll
```

## Key Logical Properties

The interpreters correctly demonstrate that sequents requiring structural rules are unprovable. This is the central feature of the language's design.

### Additive Connectives and Shared Contexts

The additive connectives (`&`, `⊕`) operate by sharing the context. For example, to prove `Γ, A&B, Δ ⊢ Θ`, the prover attempts to prove *either* `Γ, A, Δ ⊢ Θ` or `Γ, B, Δ ⊢ Θ`. This is why a sequent like `A&B |- A` is **provable**. The `(&L)` rule allows the choice of `A`, and the proof reduces to `A ⊢ A`. The `B` is not discarded by weakening; it is simply not selected in that branch of the proof.

### The Absence of Weakening

A sequent like `A, B |- A` is correctly identified as **unprovable**. To prove this, one would need to discard the `B` from the antecedent, which is precisely the weakening structural rule. Since the logic does not have this rule, no proof can be found.

This demonstrates the strict, resource-sensitive nature of the implemented logic. The system cannot invent or discard resources to make a proof succeed.