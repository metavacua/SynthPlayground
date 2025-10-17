from lfi_ill.token import Token
from lfi_ill.ast import *

LOWEST = 1
TENSOR = 2

PRECEDENCES = {
    'TENSOR': TENSOR,
}

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.peek_token = self.lexer.get_next_token()
        self.errors = []

        self.prefix_parse_fns = {
            'ID': self.parse_identifier, 'INTEGER': self.parse_integer_literal,
            'STRING': self.parse_string_literal, 'LPAREN': self.parse_grouped_expression,
            'LBRACKET': self.parse_with_pair, 'TRUE': self.parse_boolean,
            'FALSE': self.parse_boolean, 'BOTH': self.parse_boolean,
            'NEITHER': self.parse_boolean, 'CASE': self.parse_case_expression,
            'LET': self.parse_let_expression, 'FUN': self.parse_fun_expression,
            'FST': self.parse_fst, 'SND': self.parse_snd,
            'OFC': self.parse_promotion, 'WHYNOT': self.parse_why_not,
            'PAR': self.parse_par,
        }
        self.infix_parse_fns = {
            'TENSOR': self.parse_infix_expression,
        }

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse(self):
        return self.parse_expression()

    def parse_expression(self, precedence=1):
        prefix = self.prefix_parse_fns.get(self.current_token.type)
        if prefix is None:
            self.error()
        left_exp = prefix()

        while self.peek_token.type != 'EOF' and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

    def parse_identifier(self):
        return Var(self.current_token.value)

    def parse_integer_literal(self):
        return Int(int(self.current_token.value))

    def parse_string_literal(self):
        return String(self.current_token.value[1:-1])

    def parse_boolean(self):
        return Bool(self.current_token.value)

    def parse_grouped_expression(self):
        self.next_token()
        expr = self.parse_expression()
        self.eat('RPAREN')
        return expr

    def parse_infix_expression(self, left):
        op = self.current_token.value
        precedence = self.current_precedence()
        self.next_token()
        right = self.parse_expression(precedence)
        return TensorPair(left, right)

    def peek_precedence(self):
        return PRECEDENCES.get(self.peek_token.type, 0)

    def current_precedence(self):
        return PRECEDENCES.get(self.current_token.type, 0)

    def parse_with_pair(self):
        self.eat('LBRACKET')
        e1 = self.parse_expression()
        self.eat('COMMA')
        e2 = self.parse_expression()
        self.eat('RBRACKET')
        return WithPair(e1, e2)

    def parse_fst(self):
        self.eat('FST')
        self.eat('LPAREN')
        expr = self.parse_expression()
        self.eat('RPAREN')
        return Fst(expr)

    def parse_snd(self):
        self.eat('SND')
        self.eat('LPAREN')
        expr = self.parse_expression()
        self.eat('RPAREN')
        return Snd(expr)

    def parse_promotion(self):
        self.eat('OFC')
        return Promotion(self.parse_atom())

    def parse_why_not(self):
        self.eat('WHYNOT')
        return WhyNot(self.parse_atom())

    def parse_par(self):
        self.eat('PAR')
        self.eat('LPAREN')
        expr = self.parse_expression()
        self.eat('RPAREN')
        return Par(expr)

    def parse_fun_expression(self):
        self.eat('FUN')
        var = self.parse_expression()
        self.eat('COLON')
        type_ = self.parse_type()
        self.eat('ARROW')
        body = self.parse_expression()
        return Fun(var, type_, body)

    def parse_let_expression(self):
        self.eat('LET')
        if self.current_token.type == 'OFC':
            self.eat('OFC')
            v = self.parse_expression()
            self.eat('ASSIGN')
            e1 = self.parse_expression()
            self.eat('IN')
            e2 = self.parse_expression()
            return Dereliction(v, e1, e2)
        elif self.current_token.type == 'WHYNOT':
            self.eat('WHYNOT')
            v = self.parse_expression()
            self.eat('ASSIGN')
            e1 = self.parse_expression()
            self.eat('IN')
            e2 = self.parse_expression()
            return LetWhyNot(v, e1, e2)
        elif self.current_token.type == 'PAR':
            self.eat('PAR')
            self.eat('LPAREN')
            v = self.parse_expression()
            self.eat('RPAREN')
            self.eat('ASSIGN')
            e1 = self.parse_expression()
            self.eat('IN')
            e2 = self.parse_expression()
            return LetPar(v, e1, e2)
        else:
            v1 = self.parse_expression()
            self.eat('TENSOR')
            v2 = self.parse_expression()
            self.eat('ASSIGN')
            e1 = self.parse_expression()
            self.eat('IN')
            e2 = self.parse_expression()
            return LetTensor(v1, v2, e1, e2)

    def parse_case_expression(self):
        self.eat('CASE')
        expr_to_match = self.parse_expression()
        self.eat('OF')
        self.eat('INL')
        self.eat('LPAREN')
        v1 = self.parse_expression()
        self.eat('RPAREN')
        self.eat('ARROW')
        e1 = self.parse_expression()
        self.eat('PIPE')
        self.eat('INR')
        self.eat('LPAREN')
        v2 = self.parse_expression()
        self.eat('RPAREN')
        self.eat('ARROW')
        e2 = self.parse_expression()
        return Case(expr_to_match, v1, e1, v2, e2)

    def parse_type(self):
        token = self.current_token
        if token.type == 'TInt':
            self.eat('TInt')
            return TInt()
        elif token.type == 'TString':
            self.eat('TString')
            return TString()
        elif token.type == 'TBool':
            self.eat('TBool')
            return TBool()
        elif token.type == 'TUnit':
            self.eat('TUnit')
            return TUnit()
        elif token.type == 'TPar':
            self.eat('TPar')
            return TPar()
        else:
            self.error()