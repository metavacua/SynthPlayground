# Distinctions in Context-Sensitive and Context-Free Grammars

This document outlines the fine distinctions between classes of context-sensitive and context-free languages and grammars, with a particular focus on ambiguity.

## 1. Grammar Definitions

### 1.1. Context-Free Grammars (CFGs)

A **Context-Free Grammar (CFG)** is a formal grammar where every production rule is of the form:

`V → w`

where `V` is a single non-terminal symbol, and `w` is a string of terminals and/or non-terminals.

The term "context-free" comes from the fact that the non-terminal `V` can always be replaced by `w`, regardless of the context in which `V` appears.

**Example:** A simple CFG for a language of matched parentheses:

`S → (S)`
`S → ε` (where ε is the empty string)

### 1.2. Ambiguous Grammars

An **ambiguous grammar** is a context-free grammar for which there exists a string that can have more than one leftmost derivation or parse tree. This means a single string can be interpreted in multiple ways structurally.

**Example:** A grammar for simple arithmetic expressions:

`E → E + E | E * E | id`

The string `id + id * id` has two possible parse trees, reflecting two different orders of operations, making the grammar ambiguous.

### 1.3. Context-Sensitive Grammars (CSGs)

A **Context-Sensitive Grammar (CSG)** is a formal grammar where the production rules are of the form:

`αAβ → αγβ`

where `A` is a non-terminal, and `α`, `β`, and `γ` are strings of terminals and non-terminals. The key constraints are that `γ` must not be empty, and the rule `S → ε` is allowed only if the start symbol `S` does not appear on the right-hand side of any other rule.

This form means that `A` can only be replaced by `γ` in the "context" of `α` and `β`.

**Example:** A CSG for the non-context-free language {aⁿbⁿcⁿ | n ≥ 1}:

1. `S → aSBC | aBC`
2. `CB → BC`
3. `aB → ab`
4. `bB → bb`
5. `bC → bc`
6. `cC → cc`

## 2. Key Distinctions

### 2.1. Expressive Power

- **CFGs** can describe many programming language constructs and nested structures, but they cannot enforce rules that require counting or matching across disconnected parts of a string. For instance, they cannot generate the language `L = {aⁿbⁿcⁿ | n ≥ 1}`.

- **CSGs** are more powerful than CFGs. They can describe languages that CFGs cannot, including `L`. This is because the context-sensitive rules can be used to coordinate the number of `a`'s, `b`'s, and `c`'s.

### 2.2. Ambiguity

- **Ambiguity in CFGs:**
    - A language is **unambiguous** if there exists at least one unambiguous CFG for it. For example, the ambiguous arithmetic grammar above can be rewritten to be unambiguous by introducing precedence levels.
    - A language is **inherently ambiguous** if *every* possible CFG for that language is ambiguous. No unambiguous CFG can be created for it.

- **Relationship to CSGs:**
    - All context-free languages are also context-sensitive. This means that if a language is context-free (whether ambiguous or not), it can be described by a CSG.
    - The concept of ambiguity is primarily discussed in the context of CFGs. While a CSG could be designed to have multiple derivations for a string, the focus in the Chomsky hierarchy is on the expressive power of the grammar type.

### 2.3. The Role of "Context"

- In a **CFG**, the replacement of a non-terminal is independent of its neighbors. This is why it cannot handle dependencies like in `aⁿbⁿcⁿ`.

- In a **CSG**, the rules are sensitive to the surrounding symbols (the context). This allows for the enforcement of dependencies between different parts of a string. The rule `CB → BC` in the example for `aⁿbⁿcⁿ` demonstrates this: it can only be applied when `C` is immediately followed by `B`.

## 3. Summary Table

| Feature | Context-Free Grammar (CFG) | Ambiguous CFG | Context-Sensitive Grammar (CSG) |
|---|---|---|---|
| **Rule Form** | `V → w` | `V → w` | `αAβ → αγβ` |
| **Language Class** | Context-Free Languages | A property of a grammar, not a language class | Context-Sensitive Languages |
| **Expressive Power** | Less powerful | N/A | More powerful than CFGs |
| **Ambiguity** | Can be ambiguous or unambiguous | By definition, is ambiguous | Can describe all CFLs, including inherently ambiguous ones. |
| **Example Language** | `{aⁿbⁿ | n ≥ 0}` | N/A | `{aⁿbⁿcⁿ | n ≥ 1}` |
| **Key Characteristic**| Context-independent rules | Multiple parse trees for at least one string | Context-dependent rules |