import ply.yacc as yacc
from .lexer import tokens
from lfi_ill.ast import (
    Atom,
    Tensor,
    Par,
    Plus,
    With,
    Negation,
    Consistency,
    Completeness,
    CoNegation,
    Undeterminedness,
    OfCourse,
    WhyNot,
    Section,
    One,
    Bottom,
    Zero,
    Top,
)

# Operator Precedence
precedence = (
    ("left", "TENSOR", "PAR"),
    ("left", "PLUS", "WITH"),
    ("right", "NEG", "CIRC", "COMP", "MINUS", "STAR", "OFC", "WHYNOT", "SEC"),
)

# --- Parsing Rules ---


def p_formula_literal(p):
    "formula : literal"
    p[0] = p[1]


def p_literal_atom(p):
    "literal : ID"
    p[0] = Atom(p[1])


def p_literal_atom_neg(p):
    "literal : ID BOT"
    p[0] = Atom(p[1], negated=True)


def p_formula_binary_op(p):
    """formula : formula TENSOR formula
    | formula PAR formula
    | formula PLUS formula
    | formula WITH formula"""
    if p[2] == "⊗":
        p[0] = Tensor(p[1], p[3])
    elif p[2] == "⅋":
        p[0] = Par(p[1], p[3])
    elif p[2] == "⊕":
        p[0] = Plus(p[1], p[3])
    elif p[2] == "&":
        p[0] = With(p[1], p[3])


def p_formula_unary_op(p):
    """formula : NEG formula
    | CIRC formula
    | COMP formula
    | MINUS formula
    | STAR formula
    | OFC formula
    | WHYNOT formula
    | SEC formula"""
    if p[1] == "¬":
        p[0] = Negation(p[2])
    elif p[1] == "∘":
        p[0] = Consistency(p[2])
    elif p[1] == "~":
        p[0] = Completeness(p[2])
    elif p[1] == "-":
        p[0] = CoNegation(p[2])
    elif p[1] == "*":
        p[0] = Undeterminedness(p[2])
    elif p[1] == "!":
        p[0] = OfCourse(p[2])
    elif p[1] == "?":
        p[0] = WhyNot(p[2])
    elif p[1] == "§":
        p[0] = Section(p[2])


def p_formula_units(p):
    """formula : ONE
    | BOT
    | ZERO
    | TOP"""
    if p[1] == "1":
        p[0] = One()
    elif p[1] == "⊥":
        p[0] = Bottom()
    elif p[1] == "0":
        p[0] = Zero()
    elif p[1] == "⊤":
        p[0] = Top()


def p_formula_group(p):
    "formula : LPAREN formula RPAREN"
    p[0] = p[2]


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse(data):
    return parser.parse(data)


__all__ = ["parser", "parse"]
