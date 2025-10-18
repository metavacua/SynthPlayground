# Meta-Protocol: Toolchain Review on Schema Change

This protocol establishes a critical feedback loop to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

## The Problem: Protocol-Toolchain Desynchronization

A significant process gap was identified where a major architectural change to the protocol system (e.g., the introduction of a hierarchical `AGENTS.md` structure) did not automatically trigger a review of the tools that depend on that structure. The `protocol_auditor.py` tool, for instance, became partially obsolete as it was unaware of the new hierarchical model, leading to incomplete audits. This demonstrates that the agent's tools can become desynchronized from its own governing rules, creating a critical blind spot.

## The Solution: Mandated Toolchain Audit

This protocol closes that gap by introducing a new rule that explicitly links changes in the protocol system's architecture to a mandatory review of the toolchain.

**Rule `toolchain-audit-on-schema-change`**: If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that process it (`protocol_compiler.py`, `hierarchical_compiler.py`), a formal audit of the entire `tooling/` directory **must** be performed as a subsequent step.

This ensures that any modification to the fundamental way protocols are defined or processed is immediately followed by a conscious verification that all dependent tools are still functioning correctly and are aware of the new structure. This transforms the previously manual and error-prone discovery process into a formal, required step of the development lifecycle.