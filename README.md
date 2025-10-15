# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key
components defined within this module. It is automatically generated from the
corresponding `AGENTS.md` file and the source code docstrings.

## Core Protocols

This module is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior within this scope. The key protocols are:

- **`agent-bootstrap-001`**: A foundational protocol that dictates the agent's initial actions upon starting any task.
- **`dependency-management-001`**: A protocol for ensuring a reliable execution environment through formal dependency management.
- **`agent-shell-001`**: A protocol governing the use of the interactive agent shell as the primary entry point for all tasks.
- **`toolchain-review-on-schema-change-001`**: A meta-protocol to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.
- **`aura-execution-001`**: A protocol for executing Aura scripts, enabling a more expressive and powerful planning and automation language for the agent.
- **`csdc-001`**: A protocol for the Context-Sensitive Development Cycle (CSDC), which introduces development models based on logical constraints.
- **`doc-audit-001`**: A protocol to ensure the completeness of system documentation.
- **`hdl-proving-001`**: A protocol for interacting with the Hypersequent-calculus-based logic engine, allowing the agent to perform formal logical proofs.
- **`agent-interaction-001`**: A protocol governing the agent's core interaction and planning tools.
- **`plan-registry-audit-001`**: A protocol for using the plan registry auditor tool to ensure the integrity of the plan registry.
- **`refactor-001`**: A protocol for using the refactoring tool.
- **`speculative-execution-001`**: A protocol that governs the agent's ability to initiate and execute self-generated, creative, or exploratory tasks during idle periods.

## Key Components

_No `tooling/` directory found in this module._