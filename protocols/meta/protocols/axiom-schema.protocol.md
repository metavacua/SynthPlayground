# Protocol Schema: Reflexive Axiom

This document defines the schema for a "Reflexive Axiom" protocol. In our system, which is modeled after sequent calculi proof trees, these axioms form the foundational, self-evident premises upon which all other agent behaviors are built.

## Purpose

Leaf-level `AGENTS.md` files are considered "axiomatic." They should not derive their logic from child modules but should instead assert fundamental truths or directives that are taken as given. This `axiom-schema` protocol defines the structure that all such axiomatic protocols must follow.

## Structure

An axiomatic protocol is defined in a `.protocol.json` file and must contain:

- **`protocol_id`**: A unique identifier, following the pattern `axiom-<name>`.
- **`description`**: A clear, concise statement of the axiom being asserted.
- **`rules`**: A set of rules that are self-contained and require no external context to be understood. Each rule must specify its own enforcement mechanism.

This protocol definition is itself a reflexive axiom, defining its own structure according to the rules it lays out.