# Intermediate Language Witnesses

This directory contains witness grammars for language families that fall between the Context-Free and Context-Sensitive classes in the Chomsky hierarchy.

## Research Findings: Indexed Grammars

The classes in the diagram such as `LCF Sensitive` are not standard terms. Research into formal language theory points to several "mildly context-sensitive" language families that occupy this intermediate space. Of these, **Indexed Grammars** provide a particularly intuitive model that aligns with the diagram's structural themes.

An Indexed Grammar augments a Context-Free Grammar by giving each non-terminal a stack of "indices". This allows the grammar to "remember" information and enforce dependencies that a normal CFG cannot, such as counting three different symbols in `a^n b^n c^n`.

The core components of an Indexed Grammar are:
- A set of main production rules.
- A set of "index" symbols.

The production rules fall into three categories:
1.  **Push Rule (`A -> B[f]`):** Pushes an index `f` onto the stack of non-terminal `B`.
2.  **Pop Rule (`A[f] -> α`):** Requires index `f` to be on top of `A`'s stack, pops it, and then expands `A` to `α`.
3.  **Copy Rule (`A -> α`):** Expands `A` to `α`, and all non-terminals in `α` inherit `A`'s full index stack.

## Hypothesis for "Left" vs. "Right"

The "left/right" distinction in the diagram can be hypothesized to be a restriction on the **Copy Rule**. For example:
- A **Left-Indexed Grammar** might only allow the *leftmost* non-terminal in `α` to inherit the stack.
- A **Right-Indexed Grammar** might only allow the *rightmost* non-terminal to inherit the stack.

This structural difference would likely result in different generative efficiencies and properties, fitting the overall theme of our exploration. The witnesses in this directory will be based on this Indexed Grammar formalism.