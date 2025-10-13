# Module Documentation

## Overview

This document provides a human-readable summary of the protocols and key
components defined within this module. It is automatically generated from the
corresponding `AGENTS.md` file and the source code docstrings.

## Core Protocols

This module is governed by a series of machine-readable protocols defined in `AGENTS.md`. These protocols are the source of truth for the agent's behavior within this scope. The key protocols are:

- **`meta-protocol-001`**: A meta-protocol governing the agent's awareness and maintenance of its own core protocol files.
- **`non-compliance-protocol-001`**: A protocol that defines non-compliance with AGENTS.md and specifies corrective actions.
- **`pre-commit-protocol-001`**: Defines the mandatory pre-commit checks to ensure code quality, correctness, and readiness for submission.
- **`reset-all-authorization-001`**: Requires explicit user authorization via a token file for the use of the destructive `reset_all` tool.
- **`reset-all-prohibition-001`**: A high-priority protocol that unconditionally forbids the use of the `reset_all` tool.
- **`protocol-reset-all-pre-check-001`**: A protocol that mandates a pre-execution check for the `reset_all` tool to prevent unauthorized use.

## Key Components

_No `tooling/` directory found in this module._