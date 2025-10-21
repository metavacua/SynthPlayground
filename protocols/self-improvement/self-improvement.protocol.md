# Protocol: Self-Improvement

This protocol governs the agent's ability to modify its own core protocols and tools. It is a meta-protocol that ensures all self-modification is done in a structured, auditable, and safe manner.

## Rules

- **SIP-001: Formal Proposal Process:** All self-improvement initiatives must begin with a formal proposal created using the `self_improvement_cli.py` tool. This ensures that every proposed change is documented and tracked.
- **SIP-002: Structured Proposals:** Proposals must follow a strict template, including a problem statement, a detailed solution, success criteria, and an analysis of potential impacts. This enforces clarity and rigor in the planning process.
- **SIP-003: Source-Only Modification:** Changes must be made to the protocol source files (e.g., `.protocol.md` or `.protocol.json` files), not the compiled `AGENTS.md` files. This maintains the integrity of the build system.
- **SIP-004: Mandatory Re-compilation:** After any change to a protocol source, the `protocol_compiler.py` must be run to ensure the changes are valid and to propagate them to the rest of the system.
- **SIP-005: Verification Requirement:** The success of any improvement must be empirically verified through testing. The proposal must specify how the improvement will be tested and validated.
