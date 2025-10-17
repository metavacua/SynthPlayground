# Regular Language Witnesses

This directory contains witness grammars for the **Regular Languages** class, corresponding to the lowest level of the formal language hierarchy diagram.

The key distinction at this level is between left-linear and right-linear grammars.

- `right_linear_grammar.txt`: A grammar where non-terminals appear only at the right end of production rules (e.g., `A -> aB`). This type of grammar builds strings from left to right.
- `left_linear_grammar.txt`: A grammar where non-terminals appear only at the left end of production rules (e.g., `A -> Ba`). This type of grammar builds strings from right to left.

While both grammar types are equivalent in expressive power (they both generate the exact same set of regular languages), their internal structure and the process of generation (their "directionality") are different. This distinction is the first and simplest example of the diagram's theme: separating computational effectiveness from structural efficiency and properties.

Both grammars in this directory generate the language `L = {a^n b^m | n, m > 0}`.