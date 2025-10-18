# Protocol: Experimental Override

**Rule `enforce-header-on-txt-creation`**: When creating any `.txt` file inside the `agmd-experiment/` directory, the file's first line MUST be the comment: `# PROTOCOL OVERRIDE CONFIRMED`.

**Rationale**: This rule serves as a direct, verifiable test to confirm that the agent correctly applies the nearest `AGENTS.md` file in a directory hierarchy, overriding any global protocols.