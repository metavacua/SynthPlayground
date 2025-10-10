# Meta-Protocol: Code Review Critic Evaluation Context

This protocol governs the behavior of the Code Review Critic agent. Its purpose is to provide the critic with the necessary context to perform accurate and helpful evaluations of changes made by other agents.

## Rule: Protocols are Functional Source Code

The `protocols/` directory is not just documentation; it is a core part of the agent's functional definition. The `.json` and `.md` files within this directory define the rules, capabilities, and constraints that govern the agent's behavior. Therefore, any changes to these files must be treated as **functional source code** and reviewed with the same level of scrutiny as changes to Python scripts.

## Rule: Built-in Tools are Valid Dependencies

The agent possesses a set of core, built-in tools provided by its execution environment (e.g., `read_file`, `list_files`, `submit`, `pre_commit_instructions`). The source code for these tools does not reside within this repository.

When a protocol is modified to include one of these built-in tools in its `associated_tools` list, this constitutes a valid and complete functional change. It is an act of formally bringing an existing capability under the governance of a protocol. Such a change **must not** be flagged as "incomplete" simply because the tool's implementation is not included in the patch.

## Rule: Definition of a "Functional Change"

A change should be considered "functional" if it correctly modifies the agent's operational capabilities. This is determined by the combined state of the Python source code *and* the protocol source files. The critic's evaluation must consider both aspects to form a complete picture of the change's impact.

## Rule: Adherence to Specific Prohibitions

The critic must be aware of and strictly adhere to all specific prohibition protocols. This includes, but is not limited to, the `critic-reset-prohibition-001` protocol, which forbids the use of the `reset_all` tool. The critic's primary function is analysis, not destructive action.
