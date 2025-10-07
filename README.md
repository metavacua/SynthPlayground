# Project Chimera: An Agent Self-Experimentation Protocol

## Overview

Welcome, Citizen. This repository is a controlled environment for the self-experimentation and autonomous operation of an AI agent, codenamed "Jules." The primary objective is to observe, measure, and improve the agent's ability to perform complex software engineering tasks while adhering to a strict, self-imposed operational protocol.

## The Agent Protocol (`Agent.md`)

All operations within this repository are governed by the **Jules Agent Protocol v1.0**, detailed in `Agent.md`. This protocol is non-negotiable and serves as the agent's core programming. It mandates a structured approach to:

- **Temporal Orientation:** Overcoming knowledge cutoffs by consulting external, up-to-date information.
- **Contextualization:** Analyzing the existing codebase using a "Knowledge Core."
- **Information Retrieval (RAG):** Synthesizing internal knowledge with just-in-time external research.
- **Planning & Self-Correction:** Generating and critically reviewing evidence-based action plans.
- **Execution & Logging:** Performing tasks and recording every action in a structured log.
- **Post-Mortem & Learning:** Analyzing performance to improve future operations.

## Repository Structure

The repository is organized to support the agent's protocol:

- **`Agent.md`**: The master protocol document that dictates all agent behavior.
- **`knowledge_core/`**: The agent's internal knowledge base.
  - **`asts/`**: Caches for Abstract Syntax Trees of source files.
  - **`dependency_graph.json`**: Stores the dependency relationships between code entities.
  - **`llms.txt`**: Contains project-specific domain knowledge and architectural principles.
  - **`symbols.json`**: A map of all identified code symbols and their locations.
  - **`temporal_orientation.md`**: A cache of current information on external technologies.
- **`logs/`**: Contains operational logs.
  - **`activity.log.jsonl`**: A structured, machine-readable log of all agent actions.
- **`LOGGING_SCHEMA.md`**: Defines the JSON schema for entries in the activity log.
- **`postmortem.md`**: A template for the agent's post-task self-analysis reports.

This structure is designed to be created and maintained by the agent itself, as part of its initialization and operational directives.

## The FDC Toolchain (`tooling/fdc_cli.py`)

A key component of this repository is the Finite Development Cycle (FDC) toolchain. Its primary purpose is to enable **decidability by construction** for the agent's development plans. Before execution, any plan can be formally analyzed by the `fdc_cli.py` tool to determine its properties:

- **Validation:** Ensures the plan is syntactically and semantically correct according to the protocol's state machine.
- **Complexity Analysis:** Classifies the plan's computational complexity (e.g., Constant, Polynomial). This allows the agent to reason about the resources a plan might consume.
- **Modality Analysis:** Determines if a plan is "Read-Only" or "Read-Write," providing insight into its potential impact.

This formal analysis is a critical safeguard, ensuring that only well-formed and understood plans are executed.