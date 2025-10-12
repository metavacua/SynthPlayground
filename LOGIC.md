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

## Relationality, Duality, and Extensibility

The Prover and the Refuter are **dual** systems. This duality is not a simple negation, but a more fundamental relationship between what can be concluded and what can be assumed. The core design philosophy is one of **maximal compatibility and extensibility**.

- **Constructive Fragments:** Both the prover and the refuter are minimal, constructive fragments. Their purpose is not to enforce classical consistency or non-contradiction, but to provide a foundational layer that can be extended into a wide variety of more expressive logics.

- **Prover as Consequence System:** The prover identifies **provable consequences** based on its minimal rule set. If `run_prover(F)` succeeds, it means `F` is a theorem of this specific system. It makes no claims about whether `F` would be consistent in a classical sense; it only asserts that `F` can be constructed from the available axioms and rules.

- **Refuter as Assumption System:** The refuter identifies **refutable assumptions**. If `run_refuter(F)` succeeds, it means that `F` is an antitheorem, and it would be inconsistent to assume `F` within this specific system.

- **Admissibility and Independence:** Because the systems are so minimal, they are compatible with a wide range of extensions. Both classical consistency and paraconsistency (contradiction-tolerance) are **admissible**. A formula `F` that is neither provable nor refutable is independent of the system. This means one could extend the logic by adding `F` as a new theorem (a new conclusion) or as a new axiom (a new assumption) without breaking the core logic. This extensibility is a key feature of the design.

- **The `dual-transform` Meta-Operation:** The `MetaV0.lisp` file defines a `dual-transform` function. This is a tool for exploring the dual space of formulas. However, it is a **meta-operation** and does not define the operational relationship between the prover and refuter. The equivalence `refute(F) <=> prove(dual(F))` does **not** hold in this system, as that would require stronger axioms (like non-contradiction or excluded middle) than are present. The two systems are and must remain distinct.

This separation of concerns—keeping the object-level provers and refuters as minimal, extensible fragments—is the core architectural principle of this logical framework.