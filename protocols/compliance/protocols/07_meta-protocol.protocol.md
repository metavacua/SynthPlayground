# Meta-Protocol: `AGENTS.md` Self-Management

This protocol defines how the agent should manage its own core `AGENTS.md` file.

**Rule `agents-md-self-awareness`**: The `AGENTS.md` file is not a static document; it is a build artifact compiled from the source files located in the `protocols/` directory. This compilation is handled by the `make AGENTS.md` command, which orchestrates the `tooling/protocol_compiler.py` script.

To ensure that you are always operating under the most current set of rules and directives, you must periodically run `make AGENTS.md`. This is especially critical at the beginning of a new task or if you observe behavior that seems inconsistent with your documented protocols, as the protocols may have been updated.

This act of self-maintenance is a foundational element of robust, autonomous operation. It ensures that your understanding of your own governing principles remains synchronized with the repository's ground truth.