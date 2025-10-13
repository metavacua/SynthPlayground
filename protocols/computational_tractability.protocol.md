# Protocol: Computational Tractability

This protocol introduces a formal checkpoint to ensure that agent-generated plans are not only decidable but also computationally efficient.

## The Problem: The Risk of Inefficient Plans

The agent's execution framework guarantees that all plans will eventually halt (decidability). However, it does not prevent the agent from generating plans that are technically correct but wildly inefficient. For example, a plan might use a `grep` operation inside a `for_each_file` loop, resulting in a high-complexity (e.g., polynomial time) operation that could consume significant resources and time, even though it is guaranteed to terminate.

## The Solution: Mandated Efficiency Analysis

To address this, we introduce a new protocol that mandates the use of the enhanced `analyze` command in the FDC toolchain. This command provides a detailed report on a plan's computational complexity, drawing from a formal knowledge base of tool efficiencies.

By requiring the agent to perform this analysis on any plan that contains loops or other high-complexity patterns, we ensure that "performance" becomes a primary consideration during the planning phase. This allows the agent to self-correct and identify opportunities to refactor its own plans for better efficiency before execution begins, leading to a more robust and performant system.