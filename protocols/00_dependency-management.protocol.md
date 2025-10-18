# Protocol: Dependency Management

This protocol establishes a formal process for managing Python dependencies to ensure a reliable and repeatable execution environment.

**Rule `dependency-install-on-start`**: After reading `AGENTS.md`, the agent must install the dependencies listed in `requirements.txt` using `pip`. This transforms dependency management from an ad-hoc, reactive process into a proactive, automated, and verifiable step in the agent's workflow.