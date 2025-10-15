# Regular Language Witnesses

This directory contains witness grammars for the **Regular Languages** class.

- `right_linear_grammar.txt`: A grammar where non-terminals appear only at the right end of production rules.
- `left_linear_grammar.txt`: A grammar where non-terminals appear only at the left end of production rules.

Though equivalent in expressive power, their different structures ("directionality") can be analyzed by the toolchain. Both grammars generate the language `L = {a^n b^m | n, m > 0}`.