from .lexer import Lexer, Token
from .ast import (
    Program, Statement, Expression, LetStatement, ReturnStatement,
    ExpressionStatement, Identifier, IntegerLiteral, StringLiteral,
    InfixExpression, CallExpression, FunctionDefinition, BlockStatement,
    IfStatement, ForStatement, ListLiteral, MemberAccess, UseStatement,
    PrintStatement
)

# Operator precedence levels
LOWEST = 1
EQUALS = 2       # ==, !=
LESSGREATER = 3  # >, <
SUM = 4          # +
PRODUCT = 5      # *
PREFIX = 6       # -X or !X
CALL = 7         # myFunction(X)
MEMBER = 8       # object.property

PRECEDENCES = {
    'EQ': EQUALS, 'NOT_EQ': EQUALS, 'LT': LESSGREATER, 'GT': LESSGREATER,
    'IN': EQUALS, 'PLUS': SUM, 'MINUS': SUM, 'DIV': PRODUCT, 'MUL': PRODUCT,
    'LPAREN': CALL, 'DOT': MEMBER,
}

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []
        self.current_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

        self.prefix_parse_fns = {
            'ID': self.parse_identifier, 'INTEGER': self.parse_integer_literal,
            'STRING': self.parse_string_literal, 'LPAREN': self.parse_grouped_expression,
            'LBRACKET': self.parse_list_literal,
        }
        self.infix_parse_fns = {
            'PLUS': self.parse_infix_expression, 'MINUS': self.parse_infix_expression,
            'MUL': self.parse_infix_expression, 'DIV': self.parse_infix_expression,
            'EQ': self.parse_infix_expression, 'NOT_EQ': self.parse_infix_expression,
            'LT': self.parse_infix_expression, 'GT': self.parse_infix_expression,
            'IN': self.parse_infix_expression, 'LPAREN': self.parse_call_expression,
            'DOT': self.parse_member_access,
        }

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_next_token()

    def parse_program(self):
        program = Program(statements=[])
        while self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_statement(self):
        if self.current_token.type == 'LET': return self.parse_let_statement()
        elif self.current_token.type == 'RETURN': return self.parse_return_statement()
        elif self.current_token.type == 'FUNC': return self.parse_function_definition()
        elif self.current_token.type == 'IF': return self.parse_if_statement()
        elif self.current_token.type == 'FOR': return self.parse_for_statement()
        elif self.current_token.type == 'PRINT': return self.parse_print_statement()
        else: return self.parse_expression_statement()

    def parse_let_statement(self):
        self.expect_peek('ID')
        name = Identifier(self.current_token.value)
        self.expect_peek('ASSIGN')
        self.next_token()
        value = self.parse_expression(LOWEST)
        if self.peek_token.type == 'SEMICOLON': self.next_token()
        return LetStatement(name=name, value=value)

    def parse_return_statement(self):
        self.next_token()
        value = self.parse_expression(LOWEST)
        if self.peek_token.type == 'SEMICOLON': self.next_token()
        return ReturnStatement(value=value)

    def parse_print_statement(self):
        self.next_token()
        value = self.parse_expression(LOWEST)
        return PrintStatement(value=value)

    def parse_expression_statement(self):
        stmt = ExpressionStatement(expression=self.parse_expression(LOWEST))
        if self.peek_token.type == 'SEMICOLON': self.next_token()
        return stmt

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns.get(self.current_token.type)
        if prefix is None: return None
        left_exp = prefix()
        while self.peek_token.type != 'SEMICOLON' and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None: return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

    def parse_identifier(self): return Identifier(value=self.current_token.value)
    def parse_integer_literal(self): return IntegerLiteral(value=int(self.current_token.value))
    def parse_string_literal(self): return StringLiteral(value=self.current_token.value)

    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(LOWEST)
        self.expect_peek('RPAREN')
        return exp

    def parse_block_statement(self):
        block = BlockStatement(statements=[])
        self.next_token() # eat '{'
        while self.current_token.type not in ['RBRACE', 'EOF']:
            stmt = self.parse_statement()
            if stmt: block.statements.append(stmt)
            self.next_token()
        return block

    def parse_function_definition(self):
        if not self.expect_peek('ID'):
            return None
        name = Identifier(self.current_token.value)
        if not self.expect_peek('LPAREN'):
            return None
        params = self.parse_function_parameters()
        if not self.expect_peek('LBRACE'):
            return None
        body = self.parse_block_statement()
        return FunctionDefinition(name, params, body)

    def parse_function_parameters(self):
        """Parses a list of identifiers for a function definition."""
        identifiers = []

        # Check for empty parameter list: fn()
        if self.peek_token.type == 'RPAREN':
            self.next_token()  # Consume the ')'
            return identifiers

        # Consume the first parameter
        self.next_token()
        if self.current_token.type != 'ID':
            self.errors.append(f"Expected parameter name to be an identifier, got {self.current_token.type}")
            return None # Error case
        identifiers.append(Identifier(self.current_token.value))

        # Consume subsequent parameters
        while self.peek_token.type == 'COMMA':
            self.next_token()  # Consume the ','
            self.next_token()  # Consume the identifier
            if self.current_token.type != 'ID':
                self.errors.append(f"Expected parameter name to be an identifier, got {self.current_token.type}")
                return None # Error case
            identifiers.append(Identifier(self.current_token.value))

        # Expect the closing parenthesis
        if not self.expect_peek('RPAREN'):
            return None  # expect_peek already logged the error

        return identifiers

    def parse_if_statement(self):
        self.next_token()
        condition = self.parse_expression(LOWEST)
        self.expect_peek('LBRACE')
        consequence = self.parse_block_statement()
        alternative = None
        if self.peek_token.type == 'ELSE':
            self.next_token()
            self.expect_peek('LBRACE')
            alternative = self.parse_block_statement()
        return IfStatement(condition, consequence, alternative)

    def parse_for_statement(self):
        self.next_token()
        identifier = Identifier(self.current_token.value)
        self.expect_peek('IN')
        self.next_token()
        iterable = self.parse_expression(LOWEST)
        self.expect_peek('LBRACE')
        body = self.parse_block_statement()
        return ForStatement(identifier, iterable, body)

    def parse_list_literal(self):
        self.next_token()
        elements = self.parse_expression_list('RBRACKET')
        return ListLiteral(elements)

    def parse_call_expression(self, function):
        self.next_token()
        args = self.parse_expression_list('RPAREN')
        return CallExpression(function, args)

    def parse_expression_list(self, end_token):
        elements = []
        if self.current_token.type == end_token: return elements
        elements.append(self.parse_expression(LOWEST))
        while self.peek_token.type == 'COMMA':
            self.next_token()
            self.next_token()
            elements.append(self.parse_expression(LOWEST))
        self.expect_peek(end_token)
        return elements

    def parse_infix_expression(self, left):
        op = self.current_token.value
        prec = self.current_precedence()
        self.next_token()
        right = self.parse_expression(prec)
        return InfixExpression(left, op, right)

    def parse_member_access(self, left):
        self.next_token()
        if self.current_token.type != 'ID': return None
        prop = Identifier(self.current_token.value)
        return MemberAccess(left, prop)

    def expect_peek(self, token_type):
        if self.peek_token.type == token_type:
            self.next_token()
            return True
        self.errors.append(f"expected next token to be {token_type}, got {self.peek_token.type} instead")
        return False

    def peek_precedence(self): return PRECEDENCES.get(self.peek_token.type, LOWEST)
    def current_precedence(self): return PRECEDENCES.get(self.current_token.type, LOWEST)