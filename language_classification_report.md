# Language Classification Report

This report categorizes the various programs and language implementations within the repository into the Chomsky hierarchy: regular, context-free, and context-sensitive.

## 1. Regular Language Programs

### Finite Development Cycle (FDC)

The Finite Development Cycle, defined in `tooling/fdc_fsm.json`, is a **regular language**. The FSM specifies a finite number of states, a well-defined alphabet of operations, and a set of transitions. This ensures that the development process is computationally tractable and decidable.

## 2. Context-Free Language Programs

### Aura Language

The `aura_lang/` implementation is a **context-free language**. The parser (`aura_lang/parser.py`) is a Pratt parser that handles nested structures, operator precedence, and function definitions without requiring contextual information.

#### Formal Analysis

To demonstrate that `aura_lang` is not a regular language, we can use the **pumping lemma for regular languages**. The pumping lemma states that for any regular language, there is a pumping length `p` such that any string `s` in the language with length at least `p` can be divided into three parts, `s = xyz`, satisfying the following conditions:

1.  `|y| > 0`
2.  `|xy| <= p`
3.  For any `i >= 0`, the string `xy^iz` is also in the language.

Consider the `aura_lang` language's ability to handle nested function calls. A string like `f(f(f(...f(x)...)))` with `n` nested calls is a valid Aura program. Let's represent this as `f^n(x)`.

If `aura_lang` were regular, the pumping lemma would hold. Let `p` be the pumping length. Consider the string `s = f^p(x)`, which is in `aura_lang`. According to the lemma, we can split `s` into `xyz`. Since `|xy| <= p`, `xy` must be a part of the `f^p` prefix. This means `y` must be a sequence of one or more `f`'s.

If we pump `y` (e.g., `i = 2`), we get a string with more `f`'s than closing parentheses. This would result in a syntax error, as the parentheses would be unbalanced. Therefore, the pumped string is not in `aura_lang`, which contradicts the pumping lemma. This proves that `aura_lang` is not a regular language.

The language is, however, context-free. A context-free grammar can easily handle this kind of nested structure with a production rule like `Expr -> ID '(' Expr ')'`, which is recursive.

### LFI ILL Language

The `lfi_ill/` language, defined by `lfi_ill/grammar.bnf`, is a **context-free language**. The BNF grammar specifies production rules with a single non-terminal on the left-hand side, which is the definition of a context-free grammar.

## 3. Context-Sensitive Language Programs

### Python Orchestration Scripts

The Python scripts in the `tooling/` directory are **context-sensitive programs**. Their behavior is dependent on runtime conditions, such as the state of the file system, environment variables, and the outputs of other programs.
