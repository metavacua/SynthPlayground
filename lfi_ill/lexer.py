import re
from lfi_ill.token import Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = self.tokenize()
        print("Tokens:", self.tokens)

    def tokenize(self):
        token_specification = [
            ('TInt', r'TInt'), ('TString', r'TString'), ('TBool', r'TBool'), ('TUnit', r'TUnit'),
            ('TPar', r'TPar'),
            ('LET', r'let'), ('INL', r'inl'), ('INR', r'inr'), ('IN', r'in'), ('FUN', r'fun'), ('CASE', r'case'), ('OF', r'of'),
            ('FST', r'fst'), ('SND', r'snd'),
            ('TRUE', r'True'), ('FALSE', r'False'), ('BOTH', r'Both'), ('NEITHER', r'Neither'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('INTEGER', r'\d+'),
            ('STRING', r'"[^"]*"'),
            ('ARROW', r'->'), ('Lollipop', r'-o'),
            ('TENSOR', r'\*'), ('PLUS', r'\+'), ('WITH', r'&'),
            ('OFC', r'!'), ('WHYNOT', r'\?'),
            ('LPAREN', r'\('), ('RPAREN', r'\)'),
            ('LBRACE', r'{'), ('RBRACE', r'}'),
            ('LBRACKET', r'<'), ('RBRACKET', r'>'),
            ('COMMA', r','), ('COLON', r':'), ('ASSIGN', r'='),
            ('PIPE', r'\|'),
            ('COMMENT', r'#.*'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NEWLINE' or kind == 'SKIP' or kind == 'COMMENT':
                continue
            if kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected')
            tokens.append(Token(kind, value, mo.start()))
        return tokens

    def get_next_token(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return Token('EOF', '', self.pos)