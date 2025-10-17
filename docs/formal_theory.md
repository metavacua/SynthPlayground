# A Formal Theory of the Agent-Tool-Protocol Network

## 1. Introduction: Intuitionistic Linear Logic as a Foundation

This document outlines a formal theory describing the operation of the AI agent within its development environment. The theory is grounded in **Intuitionistic Linear Logic (ILL)**, a substructural logic that is particularly well-suited for modeling systems with consumable, stateful resources. Unlike classical logic, where facts are eternally true, linear logic treats propositions as resources that can be created, consumed, and transformed.

The core of this theory models:
- The **state** of the agent and its environment (the file system) as a collection of resources.
- The **tools** available to the agent as state transformers that consume and produce resources.
- The **protocols** as a set of rules that constrain the agent's behavior.
- The **protocol compilation** process as a meta-level operation that generates the agent's operating instructions (`AGENTS.md`).

## 2. The Signature: Basic Resources

The state of the system is defined by a multiset of basic propositions (resources). The logical connective `⊗` (tensor) is used to represent the coexistence of these resources.

The fundamental resource types include:

- `File(path, content)`: Represents a file at a given `path` with specific `content`.
- `AgentState(S)`: Represents the internal state of the agent, where `S` could be `{idle, planning, working, blocked}`.
- `Tool(name)`: Represents the availability of a specific tool, e.g., `Tool(read_file)`.
- `Protocol(id, content)`: Represents a source protocol definition file, e.g., `Protocol('01_agent_shell', json_content)`.
- `Axiom(A)`: Represents a governing rule or constraint `A` that the agent must follow. These are typically derived from `AGENTS.md`.

A complete system state `Γ` is the tensor product of all existing resources:
`Γ = File(p1, c1) ⊗ File(p2, c2) ⊗ ... ⊗ AgentState(S) ⊗ Tool(t1) ⊗ ...`

## 3. Tool Semantics as State Transformations

Every tool in the agent's shell is modeled as a **linear implication (`⊸`)**. A tool is a function that consumes a set of resources (the preconditions) and produces a new set of resources (the postconditions), thereby transforming the system state.

### Example: `read_file`

The `read_file(path)` tool can be modeled as:

`∀p, c. (AgentState(working) ⊗ File(p, c)) ⊸ (AgentState(working) ⊗ File(p, c) ⊗ Knowledge(p, c))`

- **Reads as**: "For any path `p` and content `c`, if the agent is in the `working` state and a file `File(p, c)` exists, then this tool consumes that state and produces a new state where the agent now possesses the knowledge of the file's content (`Knowledge(p, c)`), while the original file resource remains unchanged." (Note: `read_file` is non-destructive).

### Example: `delete_file`

The `delete_file(path)` tool is a destructive operation:

`∀p, c. (AgentState(working) ⊗ File(p, c)) ⊸ AgentState(working)`

- **Reads as**: "For any path `p` and content `c`, if the agent is `working` and `File(p, c)` exists, this tool consumes both resources and produces a state where only the agent remains. The `File` resource is gone."

### Example: `replace_with_git_merge_diff`

This tool is more complex, consuming one version of a file and producing another:

`∀p, c1, c2. (AgentState(working) ⊗ File(p, c1)) ⊸ (AgentState(working) ⊗ File(p, c2))`

- **Reads as**: "This tool consumes the file with content `c1` and produces the file with content `c2`."

## 4. The Protocol Network and Meta-Level Compilation

The generation of `AGENTS.md` is a critical meta-level process that conditions the agent's behavior for a specific task.

### 4.1. Source Protocols as Resources

The files in the `protocols/` directory are themselves resources. For instance, `protocols/01_agent_shell.protocol.json` is represented as:

`Protocol('01_agent_shell', content_json)`

### 4.2. The `protocol_compiler` as a Higher-Order Function

The `protocol_compiler.py` script acts as a transformation function. It is not a tool used *by* the agent during its primary task, but a process that runs *before* the agent's task begins. Its logical representation is:

`Compiler: (⊗_{i} Protocol(id_i, c_i)) ⊸ File('AGENTS.md', compiled_content)`

- **Reads as**: "The `Compiler` function consumes the entire tensor product (collection) of source `Protocol` resources and produces a single `File` resource: `AGENTS.md`."

### 4.3. `AGENTS.md` as a Source of Axioms

Once `AGENTS.md` is created, the agent's first action is to read it. This act transforms the `AGENTS.md` file resource into a set of axioms that constrain all subsequent actions. This is modeled using the exponential modal operator `!` ("of course"), which marks a resource as permanent and reusable for the duration of the task.

`ReadAgentsMD: File('AGENTS.md', content) ⊸ (⊗_{j} !Axiom(rule_j))`

- **Reads as**: "The `ReadAgentsMD` action consumes the `AGENTS.md` file and produces a set of persistent, reusable axioms derived from its rules."

An `Axiom(rule_j)` is a logical formula that must hold true for any subsequent state transformation (tool use). For example, a rule "Do not edit build artifacts" translates to an axiom that prevents the application of any tool `T` to a `File(path, ...)` resource where `path` is in a `dist/` or `build/` directory.

## 5. Conclusion: A Logic of Action and Constraint

This formal theory provides a robust framework for understanding and verifying the agent's behavior. By modeling the system in Intuitionistic Linear Logic, we can reason precisely about state, resource consumption, and the cascading effects of actions. The meta-level compilation of `AGENTS.md` demonstrates how the agent's own operational rules are dynamically constructed from a verifiable source of truth, creating a powerful and self-consistent system of action and constraint.