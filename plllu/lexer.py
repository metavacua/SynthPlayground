import ply.lex as lex

tokens = (
    'ID',
    'TENSOR',
    'PAR',
    'PLUS',
    'WITH',
    'OFC',
    'WHYNOT',
    'SEC',
    'NEG',
    'CIRC',
    'ONE',
    'BOT',
    'ZERO',
    'TOP',
    'LPAREN',
    'RPAREN',
    'TILDE',
)

# Tokens
t_TILDE = r'~'
t_TENSOR = r'⊗'
t_PAR = r'⅋'
t_PLUS = r'⊕'
t_WITH = r'&'
t_OFC = r'!'
t_WHYNOT = r'\?'
t_SEC = r'§'
t_NEG = r'¬'
t_CIRC = r'∘'
t_ONE = r'1'
t_BOT = r'⊥'
t_ZERO = r'0'
t_TOP = r'⊤'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()