# Design of a Paraconsistent and Paracomplete Programming Language

This document outlines the design of a minimal, executable programming language based on a non-commutative fragment of additive linear logic. The design goals are:

1.  **Paraconsistency**: The logic does not prove the law of non-contradiction, and `A, A⊥ ⊢ B` (explosion) is not a derivable rule.
2.  **Paracompleteness**: The logic does not prove the law of excluded middle (`⊢ A ⊕ A⊥`).
3.  **Minimalism**: The core is a simple proof searcher for the logic.
4.  **Extensibility**: The design allows for clean extension with non-logical features to become a practical language.
5.  **Non-Commutativity**: The order of assumptions and conclusions matters, reflecting resource sensitivity in sequence.

## 1. The Logical Foundation

The logic is a sequent calculus.

### 1.1. Syntax of Propositions

Propositions (`A`, `B`, etc.) are defined by the following grammar:

```
A ::= P       // Atomic proposition
    | A⊥      // Negation (Linear Negation)
    | A & B   // With (Additive Conjunction)
    | A ⊕ B   // Plus (Additive Disjunction)
    | ⊤       // Top (Unit of &)
    | 0       // Zero (Unit of ⊕)
```

Where `P` is an atomic proposition (e.g., `x`, `y`, `f`). Negation is defined for atoms and extended to all propositions via De Morgan's laws:

-   `(P)⊥⊥` = `P`
-   `(A & B)⊥` = `A⊥ ⊕ B⊥`
-   `(A ⊕ B)⊥` = `A⊥ & B⊥`
-   `⊤⊥` = `0`
-   `0⊥` = `⊤`

### 1.2. Sequents

A sequent is a judgment of the form `Γ ⊢ Δ`, where `Γ` (the antecedent) and `Δ` (the succedent) are sequences of propositions. The interpretation is "from the resources `Γ`, we can produce the resources `Δ`". The non-commutative nature means the order of propositions in `Γ` and `Δ` is significant.

The problem statement specifies "GAMMA and DELTA are empty such that the reflexive axiom schema for the logical language is 'A entails A'". We interpret this to mean that proofs must start from the axiom `A ⊢ A`, not that the contexts are always empty. A program's execution will be the search for a proof of a sequent of the form `⊢ A`, where `A` is the program.

### 1.3. Inference Rules

#### Identity and Structure
**Axiom (Id)**
```
A ⊢ A
```

**Cut Rule**
```
Γ₁ ⊢ Δ₁, A     A, Γ₂ ⊢ Δ₂
--------------------------- (Cut)
    Γ₁, Γ₂ ⊢ Δ₁, Δ₂
```
*(Note: The Cut rule should be admissible, meaning any proof using Cut can be transformed into a proof without it. A well-behaved sequent calculus enjoys Cut-elimination.)*

#### Additive Connectives

**Conjunction (& - "With")**
```
Γ ⊢ A, Δ      Γ ⊢ B, Δ
--------------------------- (&R)
      Γ ⊢ A & B, Δ

Γ, A ⊢ Δ
--------------------------- (&L₁)
    Γ, A & B ⊢ Δ

Γ, B ⊢ Δ
--------------------------- (&L₂)
    Γ, A & B ⊢ Δ
```

**Disjunction (⊕ - "Plus")**
```
Γ ⊢ A, Δ
--------------------------- (⊕R₁)
    Γ ⊢ A ⊕ B, Δ

Γ ⊢ B, Δ
--------------------------- (⊕R₂)
    Γ ⊢ A ⊕ B, Δ

Γ, A ⊢ Δ      Γ, B ⊢ Δ
--------------------------- (⊕L)
    Γ, A ⊕ B ⊢ Δ
```

**Units (⊤ and 0)**
```
---------- (⊤R)
  Γ ⊢ ⊤, Δ

// No left rule for ⊤

// No right rule for 0

---------- (0L)
  Γ, 0 ⊢ Δ
```

### 1.4. Logical Properties

This selection of rules and connectives leads to the desired properties.

#### Paraconsistency
The Law of Non-Contradiction is not provable. We are interested in the sequent `⊢ (A & A⊥)⊥`, which by De Morgan's laws is `⊢ A⊥ ⊕ A`. This is the same as the Law of Excluded Middle. As we will see, this is not provable.

More importantly, the principle of explosion is not derivable. The sequent `A, A⊥ ⊢ B` for an arbitrary atom `B` has no proof. Applying the rules backwards from this goal yields no path to an axiom. This prevents logical contradictions from trivializing the system.

#### Paracompleteness
The Law of Excluded Middle, `⊢ A ⊕ A⊥`, is not provable for an arbitrary atomic proposition `A`.

Let's attempt a proof search (working backwards from the goal):
```
?
------- (⊕R₁)
⊢ A ⊕ A⊥
```
This requires a proof of `⊢ A`. There is no rule that can derive `⊢ A` for an arbitrary atom `A`.

Alternatively:
```
?
------- (⊕R₂)
⊢ A ⊕ A⊥
```
This requires a proof of `⊢ A⊥`. Again, there is no rule that can prove this from an empty antecedent.

Since both potential proofs fail, `⊢ A ⊕ A⊥` is not provable.

#### Double Negation
The rule of double negation introduction (`A ⊢ A⊥⊥`) and elimination (`A⊥⊥ ⊢ A`) are admissible. This can be proven by induction on the structure of `A`. For an atom `P`, `P⊥⊥` is definitionally equivalent to `P`, so the axiom `P ⊢ P` suffices.

## 2. The Minimal Executable

The "executable" is a proof searcher for this logic. A program is a proposition `A`, and "running" the program means searching for a proof of the sequent `⊢ A`.

-   **Input**: A proposition `A` to be proven.
-   **Process**: The executable will implement a recursive function `prove(Γ, Δ)`. It will pattern-match on the structure of the formulas in `Γ` and `Δ` and apply the inference rules in reverse.
-   **Output**: `true` if a proof is found, `false` otherwise.

## 3. Extension to a Programming Language

The core logic provides a sound but limited foundation. Its real power as a programming language is unlocked through extension with "non-logical" axioms that connect the logic to the outside world. This is the maximally compatible interface for extension.

### 3.1. The Extension Mechanism: Theoretical Axioms

An extension is a set of new "theoretical" axioms. These are sequents that the proof searcher is allowed to assume as true without proof. The interpreter would be initialized with a set of these axioms, which define the capabilities of the language's standard library.

When the proof searcher encounters a sequent `Γ ⊢ Δ` that matches a theoretical axiom, it succeeds for that branch of the proof.

### 3.2. Foreign Function Interface (FFI)

The FFI is the primary way to add capabilities. External functions (e.g., from the host OS or a C library) are exposed as atomic propositions.

Let's define a more concrete `print` function. We need to handle data. We can represent a string `s` as an atomic proposition `String_s`.

**Axiom Schema for Printing:**
For any string `s`, we introduce the axiom:
` print, String_s ⊢ ⊤ `

Here, `print` is a generic atom that represents the print operation. `String_s` is the data. The `⊤` indicates that the operation completes successfully, consuming the resources and producing nothing further (a sink).

To use this, a program would need to construct the proposition `String_"Hello"`. The execution of `⊢ print, String_"Hello"` would not be provable logically. Instead, the interpreter, when encountering the atom `print` followed by a `String_s` in the antecedent, would execute the native host function `console.log(s)` and then treat the sequent as proven.

This mechanism allows any language to be linked in. A Python extension could provide an axiom:
` py_eval, String_s ⊢ ⊤ `
...where `py_eval` executes the string `s` using Python's `eval()`.

### 3.3. State Management

The non-commutative nature of the logic is perfect for modeling state. The antecedent `Γ` represents the current state of the world, as a sequence. An operation transforms this state.

**Example: A Simple Counter**
Let the state of a counter with value `n` be the atom `Count_n`.

-   **Initial State:** `Count_0`
-   **Operations:**
    -   `inc` (increment)
    -   `dec` (decrement)

**Axioms for Operations:**
For any integer `n`:
1.  `Count_n, inc ⊢ Count_(n+1)`
2.  `Count_n, dec ⊢ Count_(n-1)`

A program is a sequence of operations that transforms an initial state into a desired final state. To check if we can get to `Count_2` from `Count_0` by incrementing twice, we would ask the interpreter to prove:
` Count_0, inc, inc ⊢ Count_2 `

**Proof Search:**
1.  **Goal:** `Count_0, inc, inc ⊢ Count_2`
2.  The proof searcher must find a way to connect the left and right sides. It can use the `Cut` rule with our axioms.
3.  Apply `Cut` with axiom `Count_1, inc ⊢ Count_2`:
    -   **Subgoal 1:** `Count_0, inc ⊢ Count_1, inc` (This is not quite right, the `inc` is consumed)
    -   Let's reconsider. The proof search would work backwards from the goal `Count_2`. It would see that to get `Count_2`, it needs `Count_1, inc`. So the problem reduces to proving `Count_0, inc ⊢ Count_1`. This again matches an axiom. The proof succeeds.

This demonstrates how computation is proof construction. The sequence of operations is the proof path. The non-commutative context ensures that `inc, Count_0` is not a valid state, enforcing a clear order of operation.