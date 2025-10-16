# APPL Implementation Deviations Report

This document details the deviations found between the formal specification of the Agentic Plan Programming Language (APPL) and its concrete implementation in this repository.

## 1. Syntactic and Structural Deviations

The implementation introduces several new language features and modifies the syntax of existing ones.

### 1.1. New Language Constructs

*   **General `let` Bindings:**
    *   **Specification:** Only defines `let ... in` for destructuring pairs (`let (x, y) = ...`) and exponential types (`let !x = ...`).
    *   **Implementation:** Adds a general-purpose `let var = e1 in e2` construct. This is a common and convenient feature but is an extension beyond the formal spec.

*   **List Type:**
    *   **Specification:** Does not define any list or collection types.
    *   **Implementation:** Adds a complete, built-in polymorphic list type.
        *   **Type Syntax:** `List(T)` (e.g., `List(Int)`).
        *   **Empty List (Nil):** `Nil(T)` (e.g., `Nil(Int)`).
        *   **Constructor (Cons):** `head :: tail`.

*   **Unit Type:**
    *   **Specification:** Does not define a unit type.
    *   **Implementation:** Adds a `Unit` type with a single value, `unit`. This is used to represent computations that have no other return value.

### 1.2. Modified Syntax

*   **Function Abstraction (`fn`):**
    *   **Specification:** `fn <variable> => <term>` (e.g., `fn x => x`).
    *   **Implementation:** Requires an explicit type annotation for the argument: `fn <variable> : <type> => <term>` (e.g., `fn x : Int => x`).

*   **Sum Type Injection (`inl`, `inr`):**
    *   **Specification:** `inl(<term>)` and `inr(<term>)`.
    *   **Implementation:** Requires an additional type argument specifying the type of the *other*, non-included branch. This is likely to assist the type checker.
        *   **Syntax:** `inl(e, t_right)` and `inr(e, t_left)`. For example, for a value of type `Int + String`, an `Int` would be injected as `inl(3, String)`.

*   **Base Type Naming:**
    *   **Specification:** Uses lowercase names for base types (e.g., `int`, `string`, `bool`).
    *   **Implementation:** Uses capitalized names (e.g., `Int`, `String`, `Bool`).

## 2. Semantic Deviations (Static and Dynamic)

The implementation makes specific choices about how to realize the formal semantics.

### 2.1. Static Semantics (Type Checking)

*   **Linearity Implementation:** The implementation correctly captures the essence of linear logic by using two separate contexts: a `linear_context` for variables that must be used once, and an `unrestricted_context` for reusable variables. This is a faithful realization of the `!` modality.

*   **Linearity of `let`:** The new general `let` binding treats the bound variable as **linear**. This means any value bound with `let x = ...` must be consumed exactly once.

*   **Promotion (`!`) Rule:** The implementation of the `!-intro` rule is sound but more restrictive than the formal specification.
    *   **Specification:** `!Γ ⊢ t : τ / !Γ ⊢ !t : !τ`. This allows promotion if the term `t` only depends on reusable variables from the context `!Γ`.
    *   **Implementation:** Checks that the linear context is completely empty when promoting an expression. This simplification achieves the goal of preventing linear variables from being made reusable, but it may be stricter than necessary.

### 2.2. Dynamic Semantics (Interpretation)

*   **Evaluation of `!`:**
    *   **Specification:** Defines `let !x = !t in t' --> t'[t/x]`. The `!` has a distinct role in the dynamic semantics.
    *   **Implementation:** The interpreter effectively treats `Promote(e)` (the AST node for `!e`) as an identity operation during evaluation (`self.interpret(term.e)`). The dereliction rule `LetBang` (`let !x = ...`) simply evaluates the expression and binds the result. All the logical force of the `!` is handled by the type checker, not the interpreter.

*   **Closures:** The interpreter uses `Closure` objects to correctly handle the lexical scope of functions, which is a standard implementation technique for higher-order functions.

## 3. Pragmatic Extensions for Application

The most significant deviation is the extension of the pure calculus into a practical tool through built-in functions.

*   **Primitive Mechanism:** The interpreter has a `Primitive` class that allows native Python functions to be exposed as functions within the APPL language.

*   **Default Environment:** The type checker and interpreter are initialized with a large, default environment of "primitive" functions that are not part of the formal specification. These functions are all in the `unrestricted_context` (meaning they can be used freely) and provide the core API for using APPL in a planning context. The built-in primitives include:
    *   `create_action(String, List(String), List(String)) -> Action`
    *   `create_goal(String, List(String)) -> Goal`
    *   `create_state(List(String)) -> State`
    *   `apply_action(State, Action) -> State`
    *   `is_goal(State, Goal) -> Bool`
    *   `parse(String) -> Term`
    *   `unparse(Term) -> String`
    *   `eval(Term) -> Term`

These extensions transform APPL from a theoretical calculus into a usable language for defining and executing agent plans.