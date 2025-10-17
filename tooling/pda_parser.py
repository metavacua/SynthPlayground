import sys
import os
import ply.lex as lex
import ply.yacc as yacc

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- AST Node Definitions ---
def AtomNode(name):
    return ('atom', name)

def UnaryOpNode(op, child):
    return ('unary_op', op, child)

def BinaryOpNode(op, left, right):
    return ('binary_op', op, left, right)

# --- Lexer Definition ---

tokens = (
    'ATOM',
    'IMPLIES',
    'WITH',
    'PLUS',
    'NOT',      # LFU undeterminedness operator '~'
    'BANG',
    'CONSISTENCY', # LFI consistency operator '∘'
    'LPAREN',
    'RPAREN',
)

# Regex for tokens
t_IMPLIES = r'-o'
t_WITH = r'&'
t_PLUS = r'\|'
t_NOT = r'~'
t_BANG = r'!'
t_CONSISTENCY = r'∘'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ATOM(t):
    r'[A-Z][A-Z0-9]*'
    return t

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Build the lexer
lexer = lex.lex()


# --- Parser Definition ---

# Operator precedence and associativity
precedence = (
    ('right', 'IMPLIES'),
    ('left', 'PLUS'),
    ('left', 'WITH'),
    ('right', 'NOT', 'BANG', 'CONSISTENCY'),
)

def p_formula_binary(p):
    """
    formula : formula IMPLIES formula
            | formula WITH formula
            | formula PLUS formula
    """
    p[0] = BinaryOpNode(p[2], p[1], p[3])

def p_formula_unary(p):
    """
    formula : NOT formula
            | BANG formula
            | CONSISTENCY formula
    """
    p[0] = UnaryOpNode(p[1], p[2])

def p_formula_group(p):
    """
    formula : LPAREN formula RPAREN
    """
    p[0] = p[2]

def p_formula_atom(p):
    """
    formula : ATOM
    """
    p[0] = AtomNode(p[1])

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        raise SyntaxError("Syntax error: Unexpected end of input")

# Build the parser
parser = yacc.yacc(debug=False, write_tables=False)

def parse_formula(formula_string):
    """
    Parses a pLLLU formula string into an AST.
    """
    return parser.parse(formula_string, lexer=lexer)

# --- Self-test for demonstration ---
if __name__ == '__main__':
    print("--- Testing the pLLLU PDA Parser ---")
    test_formulas = [
        "A",
        "~A",
        "∘A",
        "A -o B",
        "∘(A & B)",
    ]

    for formula in test_formulas:
        try:
            ast = parse_formula(formula)
            print(f"SUCCESS: \"{formula}\" -> {ast}")
        except SyntaxError as e:
            print(f"FAILURE: \"{formula}\" -> {e}")

    print("\n--- Testing Expected Failures ---")
    try:
        parse_formula("A ∘ B") # Infix is not supported for consistency
        print("FAILURE: \"A ∘ B\" should have failed but didn't.")
    except SyntaxError as e:
        print(f"SUCCESS: \"A ∘ B\" correctly failed with error: {e}")