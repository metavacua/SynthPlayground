# Meta-Protocol: Toolchain Review on Schema Change

This protocol establishes a critical feedback loop to ensure the agent's toolchain remains synchronized with the architecture of its governing protocols.

**Rule `toolchain-audit-on-schema-change`**: If a change is made to the core protocol schema (`protocol.schema.json`) or to the compilers that process it (`protocol_compiler.py`, `hierarchical_compiler.py`), a formal audit of the entire `tooling/` directory **must** be performed as a subsequent step. This ensures that any modification to the fundamental way protocols are defined or processed is immediately followed by a conscious verification that all dependent tools are still functioning correctly.