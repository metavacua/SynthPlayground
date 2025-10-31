# Executable Witnesses for Three Classes of Recursive Languages

This project provides Python implementations of 'executable witnesses' for three distinct classes of complete, recursive languages, based on the concepts from the 'Asymmetric Bifurcation of Formal Systems' thesis. Under the Curry-Howard correspondence, a proof of a proposition is equivalent to a program (a witness) that computes the result.

Each script corresponds to one of the three language classes and demonstrates a different computational nature of proof.


---

## `classical_logic_witness.py`

Executable Witness for a Proposition in Classical Propositional Logic.

This script demonstrates the Curry-Howard correspondence for a simple,
decidable theory. The executable witness for a proposition is a function
that computationally demonstrates the proposition's truth.
### How to Run
```bash
python classical_logic_witness.py
```

---

## `presburger_arithmetic_witness.py`

Executable Witness for a Proposition in L_neither (Presburger Arithmetic).

This script demonstrates the Curry-Howard correspondence for a simple,
decidable theory. The executable witness for a proposition is a function
that computationally demonstrates the proposition's truth.
### How to Run
```bash
python presburger_arithmetic_witness.py
```

---

## `skolem_arithmetic_witness.py`

Executable Witness for a Proposition in Skolem Arithmetic.

This script demonstrates the Curry-Howard correspondence for a simple,
decidable theory. The executable witness for a proposition is a function
that computationally demonstrates the proposition's truth.
### How to Run
```bash
python skolem_arithmetic_witness.py
```

---

## `witness_d.py`

Executable Witness for a Proposition in L_D.

L_D corresponds to the theorems of a complete, decidable extension (T*)
of an inessentially undecidable theory like IΔ₀ + Ω₁.

The executable witness for a proposition in this language is a program that
leverages the "oracle-like" completing axioms of the decidable theory.
The proof often reduces to a lookup in this set of hardcoded truths.
### How to Run
```bash
python witness_d.py
```
