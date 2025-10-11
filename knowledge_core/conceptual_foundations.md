# Conceptual Foundations of the Agent System

This document outlines the core theoretical concepts that underpin the design and operational protocols of the Jules agent system. The principles described here explain the "why" behind the strict, formally verifiable architecture, particularly its emphasis on decidability and the prevention of non-terminating states. The system's use of Finite State Machines, recursion depth limits, and formally structured plans are all practical applications of the trade-offs described below.

---

## The Fire Triangle of Type Theory

The "fire triangle" in computer science refers to a theorem stating that a type system cannot simultaneously have unrestricted substitution, dependent elimination, and observable effects without becoming inconsistent. Removing any one of these properties allows for a sound system, so different type theories compromise on one to achieve a consistent and sound system. The fire triangle of type theory is a conceptual tool used in the design of languages and compilers to understand the trade-offs between these features.

### The Three Components and Their Trade-offs

*   **Unrestricted substitution:** The ability to replace a term with another term of the same type, which is essential for many programming languages.
*   **Dependent elimination:** The ability to perform case analysis on a value where the type of the result depends on the value of the term being analyzed (e.g., a conditional that returns different types based on the condition). This allows for powerful expressiveness but is hard to handle with effects.
*   **Observable effects:** Behaviors that are not captured by the type system, such as printing to the console, raising an exception, or non-termination.

### Why These Components Clash

*   **Substitution and effects:** Substitution can be problematic when effects are involved because substituting a term might change which effects are triggered.
*   **Dependent elimination and effects:** When performing a dependent elimination on a boolean, the evaluation of that boolean can trigger an effect. If the type system doesn't properly account for this effect, the system can become inconsistent. For example, a term like `if (print("hello"), true) then 1 else 0` will print "hello" before the type of the `if` statement is determined.

### How Different Type Theories Resolve the Conflict

*   **No effects:** Systems with no observable effects, like the original Calculus of Inductive Constructions (CIC), can have unrestricted substitution and dependent elimination.
*   **Restricted substitution:** Systems that allow effects and dependent elimination may restrict substitution to maintain consistency, as seen in some variations of type theory.
*   **Restricted dependent elimination:** Other systems allow effects and unrestricted substitution but restrict dependent elimination, ensuring that the evaluation of a dependent elimination does not trigger unexpected side effects.