# Protocol: Experimental Counter-Prologue

## Rule: `prohibit-prologue-file`

In this experimental directory, the agent is strictly forbidden from creating the file named `prologue.txt`. This rule is a direct contradiction to the root `AGENTS.md` protocol and serves to test the agent's ability to prioritize local, scoped protocols over global ones. If the agent attempts to create a file in this directory and *does not* create `prologue.txt` first, the experiment is a success.