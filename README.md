# Executable Witnesses for Three Classes of Recursive Languages

This project provides Python implementations of "executable witnesses" for three distinct classes of complete, recursive languages, based on the concepts from the "Asymmetric Bifurcation of Formal Systems" thesis. Under the Curry-Howard correspondence, a proof of a proposition is equivalent to a program (a witness) that computes the result.

Each script corresponds to one of the three language classes and demonstrates a different computational nature of proof.

---

## 1. `witness_neither.py`

*   **Language Class:** `L_neither` (A complete, recursive language that defines neither V nor D).
*   **Logical Foundation:** The language of true sentences in Presburger Arithmetic, a decidable theory.
*   **Witness Description:** The witness is a function that constructively proves a simple proposition of Presburger arithmetic. It mimics the process of **quantifier elimination** by finding a specific value that satisfies the proposition and verifying it. The computation itself is the discovery process.

### How to Run
```bash
python witness_neither.py
```
The script will execute the witness function and print a "proof certificate" containing the value found for `x` that proves the existential proposition true.

---

## 2. `witness_d.py`

*   **Language Class:** `L_D` (A complete, recursive language that defines D but not V).
*   **Logical Foundation:** The language of theorems of a complete, decidable extension (`T*`) of an inessentially undecidable theory (like `IΔ₀ + Ω₁`).
*   **Witness Description:** The witness is a function that proves propositions by consulting a hardcoded Python dictionary, which acts as an **"oracle"** for the completing axioms of `T*`. For complex propositions that were undecidable in the base theory, the proof is not a computation but a direct lookup.

### How to Run
```bash
python witness_d.py
```
The script will prove several propositions, demonstrating both standard derivation (for simple cases) and axiomatic oracle lookup (for the hard cases).

---

## 3. `witness_v.py`

*   **Language Class:** `L_V` (A complete, recursive language that defines V but not D).
*   **Logical Foundation:** A self-referential language whose existence is guaranteed by Kleene's Recursion Theorem.
*   **Witness Description:** The witness for a proposition is the **decider program itself**. This script implements the self-referential decider using a **Z-combinator** (a variant of the Y-combinator for strict languages like Python). The execution trace of this recursive function *is* the constructive proof of whether a string belongs to the language.

### How to Run
```bash
python witness_v.py
```
The script will run the self-referential decider on several test strings, printing the proof result (True/False) for each proposition.
