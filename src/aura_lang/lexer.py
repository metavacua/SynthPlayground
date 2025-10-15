import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def number(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        token = KEYWORDS.get(result, Token('ID', result))
        return token

    def string(self):
        """Handle string literals."""
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token('STRING', result)


    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue

            # Multi-character tokens first
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('NOT_EQ', '!=')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('EQ', '==')

            if self.current_char == '-' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token('ARROW', '->')

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char.isdigit():
                return Token('INTEGER', self.number())

            if self.current_char == '"':
                return self.string()

            # Single-character tokens
            try:
                token_type = TOKEN_MAP[self.current_char]
                token = Token(token_type, self.current_char)
                self.advance()
                return token
            except KeyError:
                self.error()

        return Token('EOF', None)

    def error(self):
        raise Exception(f"Invalid character: '{self.current_char}'")

# --- Token Definitions ---
KEYWORDS = {
    'func': Token('FUNC', 'func'),
    'let': Token('LET', 'let'),
    'if': Token('IF', 'if'),
    'else': Token('ELSE', 'else'),
    'return': Token('RETURN', 'return'),
    'for': Token('FOR', 'for'),
    'in': Token('IN', 'in'),
    'use': Token('USE', 'use'),
    'print': Token('PRINT', 'print'),
}

TOKEN_MAP = {
    '=': 'ASSIGN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '[': 'LBRACKET',
    ']': 'RBRACKET',
    ',': 'COMMA',
    ':': 'COLON',
    '.': 'DOT',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '!': 'BANG',
    ';': 'SEMICOLON',
    '>': 'GT',
    '<': 'LT',
}