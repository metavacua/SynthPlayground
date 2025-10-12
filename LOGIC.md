# Documentation for the Prover and Refuter Systems

This document explains the functionality and relationship of the `prover.py` and `refuter.py` modules. These systems implement a non-classical, additive, linear-like logic.

## System Overview

The core of this logical framework consists of two distinct but symmetric systems:

1.  **The Prover (`prover.py`):** A system designed to find proofs for formulas. A successful output from the prover indicates that a formula is a **theorem** of the system.
2.  **The Refuter (`refuter.py`):** A system designed to find refutations for formulas. A successful output from the refuter indicates that a formula is an **antitheorem** of the system.

Both systems are designed as **non-recursive, fixed-chain dispatchers**. This architecture guarantees that any operation will terminate, as it simply checks a formula against a finite set of rules in a fixed order. This design is intentional and reflects the minimalistic, decidable nature of the logic.

It is critical to understand that these systems are not simple negations of each other. A formula that is not a theorem is not necessarily an antitheorem. A formula can be independent of both systems.

### Formula Representation

Formulas are represented as Python tuples. The first element of the tuple is the operator, and the subsequent elements are the arguments.

- **`('con',)`**: An atomic provable constant.
- **`('incon',)`**: An atomic refutable constant.
- **`('dep', formula1, formula2)`**: A "dependence" junction.
- **`('ind', formula1, formula2)`**: An "independence" junction.

---

## The Prover (`prover.py`)

The prover attempts to find a constructive proof for a given formula.

### How It Works: Step-by-Step

The `run_prover` function implements the non-recursive, fixed-chain dispatch.

1.  **Input:** The `run_prover` function takes a formula tuple as input.
2.  **Axiom Check:** It first checks if the formula matches the `axiom_conr`.
    - **Axiom ConR:** A formula of the form `('dep', A, A)` is axiomatically a theorem. If the axiom applies, the prover successfully terminates, returning the sub-formula `A`.
3.  **Rule Chain:** If the axiom does not apply, the function proceeds down a fixed chain of rules.
    - **Rule `dependence-r`:** It checks if the formula is `('dep', A, B)`. If so, it calls `run_prover` on `A` **AND** `B`. Both sub-proofs must succeed.
    - **Rule `independence-r`:** If the first rule did not apply or return, it checks if the formula is `('ind', A, B)`. If so, it calls `run_prover` on `A` **OR** `B`. Only one sub-proof needs to succeed.
4.  **Output:**
    - **On Success:** If the axiom or any rule succeeds, the prover returns the proven formula (or sub-formula).
    - **On Failure:** If the end of the rule chain is reached and no proof is found, the prover returns `None`.

---

## The Refuter (`refuter.py`)

The refuter is architecturally symmetric to the prover and attempts to find a constructive refutation for a given formula.

### How It Works: Step-by-Step

The `run_refuter` function implements the non-recursive, fixed-chain dispatch.

1.  **Input:** The `run_refuter` function takes a formula tuple as input.
2.  **Axiom Check:** It first checks if the `axiom_inconl` applies.
    - **Axiom InconL:** A formula is an antitheorem if it is `('incon',)` or has the form `('ind', A, A)`.
3.  **Rule Chain:** If the axiom does not apply, the function proceeds down a fixed chain of rules.
    - **Rule `independence-l`:** It checks if the formula is `('ind', A, B)`. If so, it calls `run_refuter` on `A` **OR** `B`.
    - **Rule `dependence-l`:** If the first rule did not apply or return, it checks if the formula is `('dep', A, B)`. If so, it calls `run_refuter` on `A` **AND** `B`.
4.  **Output:**
    - **On Success:** If the axiom or any rule succeeds, the refuter returns the refuted formula.
    - **On Failure:** If the end of the rule chain is reached, it returns `None`.

---

## Relationality and Duality

The Prover and the Refuter are **dual** systems, but this duality is a deep, conceptual one, not a simple logical NOT.

- **Separate Worlds:** A formula's failure to be a theorem does not imply it is an antitheorem.
- **The Meta-System:** The true relationship is captured at a meta-level. The `MetaV0.lisp` file defines a `dual-transform` operation. The fundamental theorem of this meta-system is **`refute(F) <=> prove(dual(F))`**. This shows that refutation is not negation, but rather proof in a transformed, dual space. This provides a powerful way to reason about the relationship between the two systems without conflating them. The key transformations are:
  - `dual(con)` becomes `incon`
  - `dual(incon)` becomes `con`
  - `dual(dep A B)` becomes `ind (dual A) (dual B)`
  - `dual(ind A B)` becomes `dep (dual A) (dual B)`

This separation of concerns—keeping the object-level provers and refuters distinct from the meta-level duality transformation—is the core architectural principle of this logical framework.