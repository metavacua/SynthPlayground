---
## Meta-Protocol: Decidability and Computational Constraints

**This protocol ensures that all development processes are formally decidable and computationally tractable.**

1.  **Non-Turing Completeness:** The agent's planning and execution language is, by design, not Turing-complete. This is a fundamental constraint to guarantee that all processes will terminate.
2.  **Strictly Bounded Recursion:** The agent MUST NOT generate plans that involve recursion or self-invocation. A plan cannot trigger another FDC or a sub-plan. The only exception is the pre-defined "Deep Research Cycle" (L4 Orientation), which is a formally bounded, read-only analysis process.
3.  **FSM Adherence:** All plans must be valid strings in the language defined by the `tooling/fdc_fsm.json` Finite State Machine. This ensures a predictable, linear progression of states. The `lint` command in the `fdc_cli.py` tool is the final arbiter of plan validity.

This protocol prevents computational explosions and ensures that the agent's behavior remains predictable and verifiable.