# Protocol: The Context-Free Development Cycle (CFDC)

This protocol marks a significant evolution from the Finite Development Cycle (FDC), introducing a hierarchical planning model that enables far greater complexity and modularity while preserving the system's core guarantee of decidability.

## From FSM to Pushdown Automaton

The FDC was based on a Finite State Machine (FSM), which provided a strict, linear sequence of operations. While robust, this model was fundamentally limited: it could not handle nested tasks or sub-routines, forcing all plans to be monolithic.

The CFDC upgrades our execution model to a **Pushdown Automaton**. This is achieved by introducing a **plan execution stack**, which allows the system to call other plans as sub-routines. This enables a powerful new paradigm: **Context-Free Development Cycles**.

## The `call_plan` Directive

The core of the CFDC is the new `call_plan` directive. This allows one plan to execute another, effectively creating a parent-child relationship between them.

- **Usage:** `call_plan <path_to_sub_plan.txt>`
- **Function:** When the execution engine encounters this directive, it:
    1.  Pushes the current plan's state (e.g., the current step number) onto the execution stack.
    2.  Begins executing the sub-plan specified in the path.
    3.  Once the sub-plan completes, it pops the parent plan's state from the stack and resumes its execution from where it left off.

## Ensuring Decidability: The Recursion Depth Limit

A system with unbounded recursion is not guaranteed to terminate. To prevent this, the CFDC introduces a non-negotiable, system-wide limit on the depth of the plan execution stack.

**Rule `max-recursion-depth`**: The execution engine MUST enforce a maximum recursion depth, defined by a `MAX_RECURSION_DEPTH` constant. If a `call_plan` directive would cause the stack depth to exceed this limit, the entire process MUST terminate with an error. This hard limit ensures that even with recursive or deeply nested plans, the system remains a **decidable**, non-Turing-complete process that is guaranteed to halt.