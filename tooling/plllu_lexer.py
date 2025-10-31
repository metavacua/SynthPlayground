"""
This module provides functionality for...
"""

import ply.lex as lex

tokens = (
    "ATOM",
    "IMPLIES",
    "WITH",
    "PLUS",
    "NOT",  # LFU undeterminedness operator '~'
    "BANG",
    "CONSISTENCY",  # LFI consistency operator '∘'
    "SECTION",
    "WHYNOT",
    "LPAREN",
    "RPAREN",
)

# Regex for tokens
t_IMPLIES = r"-o"
t_WITH = r"&"
t_PLUS = r"\|"
t_NOT = r"~"
t_BANG = r"!"
t_CONSISTENCY = r"∘"
t_SECTION = r"§"
t_WHYNOT = r"\?"
t_LPAREN = r"\("
t_RPAREN = r"\)"


def t_ATOM(t):
    r"[A-Z][A-Z0-9]*"
    return t


# Ignored characters (spaces and tabs)
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")


# Build the lexer
lexer = lex.lex()
