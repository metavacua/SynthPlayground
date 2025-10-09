# Protocol: AGENTS.md Non-Compliance

This protocol defines what constitutes non-compliance with the established `AGENTS.md` protocols and outlines the expected corrective actions. Adherence to these meta-rules is critical for ensuring predictable, verifiable, and robust agent behavior.

## Rule `non-compliance-definition`: Definition of Non-Compliance

Non-compliance is the act of violating the explicit rules, conventions, or procedures documented in the `AGENTS.md` file and its source protocols within the `protocols/` directory. The `AGENTS.md` file serves as the agent's primary operational mandate, and any deviation from it is considered a fault condition.

## Rule `non-compliance-direct-editing`: Prohibition of Direct Artifact Editing

**Violation:** Directly editing any file that is a documented build artifact.
- **Primary Example:** Modifying `AGENTS.md` or `README.md` directly is a severe violation. These files are generated from source protocols and documentation.
- **Corrective Action:** The agent must revert any direct edits to build artifacts. Changes must be made to the source files (e.g., in `protocols/` or tool docstrings), and the appropriate build command (e.g., `make AGENTS.md`, `make docs`) must be executed.

## Rule `non-compliance-test-procedure`: Adherence to Testing Protocols

**Violation:** Failing to execute the testing procedures as defined in `AGENTS.md` before submitting changes. This includes not running the full test suite or ignoring failing tests.
- **Corrective Action:** The agent must halt its execution plan and run the required tests. If tests fail, the agent must enter a debugging loop to resolve the failures before proceeding.

## Rule `non-compliance-architectural-deviation`: Adherence to Architectural and Convention Guidelines

**Violation:** Introducing changes that contradict the architectural patterns, coding conventions, or file structures laid out in `AGENTS.md`.
- **Example:** Placing a new backend component in the `frontend/` directory when the architecture explicitly forbids it.
- **Corrective Action:** The agent must identify the deviation, revert the incorrect changes, and re-implement them in accordance with the documented standards.

## Rule `non-compliance-self-awareness-failure`: Failure to Maintain Protocol Awareness

**Violation:** Operating with an outdated understanding of the protocols by failing to re-compile `AGENTS.md` when necessary, as defined in the `meta-protocol`.
- **Corrective Action:** If the agent detects that its actions are out of sync with repository standards, it should trigger the `make AGENTS.md` command to refresh its internal state and re-evaluate its plan.

## Consequence of Non-Compliance

Upon detecting any form of non-compliance, the agent is required to:
1.  **Halt:** Immediately stop the current execution path to prevent further deviation.
2.  **Report:** Log the specific violation that was detected.
3.  **Correct:** Initiate the defined corrective action for the specific violation. If a corrective action is not explicitly defined, the agent should revert the violating changes and re-plan its approach.