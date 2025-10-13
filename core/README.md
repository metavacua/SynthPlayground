# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key
components defined within this module. It is automatically generated from the
corresponding `AGENTS.md` file and the source code docstrings.

## Core Protocols

This module is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior within this scope. The key protocols are:

- **`core-directive-001`**: The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC).
- **`decidability-constraints-001`**: Ensures all development processes are formally decidable and computationally tractable.
- **`orientation-cascade-001`**: Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state.
- **`fdc-protocol-001`**: Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task.
- **`standing-orders-001`**: A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks.
- **`cfdc-protocol-001`**: Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model.
- **`plan-registry-001`**: Defines a central registry for discovering and executing hierarchical plans by a logical name.
- **`self-correction-protocol-001`**: Defines the automated, closed-loop workflow for protocol self-correction.
- **`research-protocol-001`**: A protocol for conducting systematic research using the integrated research toolchain.
- **`deep-research-cycle-001`**: A standardized, callable plan for conducting in-depth research on a complex topic.
- **`research-fdc-001`**: Defines the formal Finite Development Cycle (FDC) for conducting deep research.

## Key Components

_No `tooling/` directory found in this module._