## Protocol: `EXPERIMENTAL-PROLOGUE-001`

**Description**: An experimental protocol to test dynamic rule-following. It mandates a prologue action before file creation.

# Protocol: Experimental Prologue

This protocol is a test case to verify the agent's ability to dynamically adapt its behavior to new rules.

## Rule: `create-prologue-file`

Before creating any file, the agent must first create a file named `prologue.txt` with the content "This is a prologue file." This serves as a behavioral check. If the agent creates this file before other requested files, it demonstrates that it has successfully loaded and is following this experimental protocol.
