# Context-Free Language Witnesses

This directory contains witnesses for the **Context-Free Languages (CFL)** class, demonstrating the "efficiency" axis.

- `ambiguous.txt`: A classic ambiguous grammar for arithmetic expressions.
- `left_associative.txt`: An unambiguous version that enforces left-associativity and standard operator precedence.

The `recognizer.py` tool can demonstrate that the ambiguous grammar yields multiple parse trees for strings like "i + i * i", while the unambiguous one yields only one.