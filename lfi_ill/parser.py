import ply.yacc as yacc
from lfi_ill.lexer import tokens
from lfi_ill.ast import *

precedence = (
    ('right', 'UNARY'),
    ('left', 'TENSOR', 'PAR', 'PLUS', 'WITH'),
)

# Parsing rules
def p_formula_literal(p):
    'formula : literal'
    p[0] = p[1]

def p_literal_atom(p):
    'literal : ID'
    p[0] = Atom(p[1])

def p_literal_atom_neg(p):
    'literal : ID BOT'
    p[0] = Atom(p[1], negated=True)

def p_formula_multiplicative(p):
    'formula : formula TENSOR formula'
    p[0] = Tensor(p[1], p[3])

def p_formula_par(p):
    'formula : formula PAR formula'
    p[0] = Par(p[1], p[3])

def p_formula_additive(p):
    'formula : formula PLUS formula'
    p[0] = Plus(p[1], p[3])

def p_formula_with(p):
    'formula : formula WITH formula'
    p[0] = With(p[1], p[3])

def p_formula_modalities(p):
    '''formula : OFC formula %prec UNARY
               | WHYNOT formula %prec UNARY
               | SEC formula %prec UNARY'''
    if p[1] == '!':
        p[0] = OfCourse(p[2])
    elif p[1] == '?':
        p[0] = WhyNot(p[2])
    elif p[1] == '§':
        p[0] = Section(p[2])

def p_formula_paraconsistent(p):
    '''formula : NEG formula %prec UNARY
               | CIRC formula %prec UNARY
               | TILDE formula %prec UNARY'''
    if p[1] == '¬':
        p[0] = Negation(p[2])
    elif p[1] == '∘':
        p[0] = Consistency(p[2])
    elif p[1] == '~':
        p[0] = Paracomplete(p[2])

def p_formula_units(p):
    '''formula : ONE
               | BOT
               | ZERO
               | TOP'''
    if p[1] == '1':
        p[0] = One()
    elif p[1] == '⊥':
        p[0] = Bottom()
    elif p[1] == '0':
        p[0] = Zero()
    elif p[1] == '⊤':
        p[0] = Top()

def p_formula_group(p):
    'formula : LPAREN formula RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

def parse(data):
    return parser.parse(data)