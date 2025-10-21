import re
from appl_ast import (
    App,
    Bool,
    Case,
    Cons,
    Fun,
    Inl,
    Inr,
    Int,
    Let,
    LetBang,
    LetPair,
    Nil,
    Pair,
    Promote,
    String,
    TAction,
    TBool,
    TExponential,
    TFun,
    TGoal,
    TInt,
    TList,
    TProd,
    TSum,
    TState,
    TString,
    TUnit,
    Term,
    Unit,
    Var,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if expected and token != expected:
                raise ValueError(
                    f"Expected '{expected}' but got '{token}' at position {self.pos}. Remaining tokens: {self.tokens[self.pos:]}"
                )
            self.pos += 1
            return token
        if expected:
            raise ValueError(f"Expected '{expected}' but got end of input")
        return None

    def parse_atom(self):
        token = self.peek()
        if token.isdigit():
            self.consume()
            return Int(int(token))
        elif token.startswith('"'):
            self.consume()
            return String(token[1:-1])
        elif token == "true":
            self.consume()
            return Bool(True)
        elif token == "false":
            self.consume()
            return Bool(False)
        elif token == "unit":
            self.consume()
            return Unit()
        elif token == "Nil":
            self.consume()
            self.consume("(")
            t = self.parse_type()
            self.consume(")")
            return Nil(t)
        elif token == "Cons":
            self.consume()
            self.consume("(")
            h = self.parse_expr()
            self.consume(",")
            t = self.parse_expr()
            self.consume(")")
            return Cons(h, t)
        elif token and token not in [
            "let",
            "in",
            "case",
            "of",
            "inl",
            "inr",
            "fn",
            "(",
            ")",
            ",",
            "=>",
            "|",
            "!",
            "=",
            "*",
            "+",
            "->",
            "::",
            ":",
        ]:
            self.consume()
            return Var(token)
        elif token == "(":
            self.consume("(")
            expr = self.parse_expr()
            if self.peek() == ",":
                self.consume(",")
                expr2 = self.parse_expr()
                self.consume(")")
                return Pair(expr, expr2)

            self.consume(")")
            return expr
        else:
            raise ValueError(f"Unexpected token: {token}")

    def parse_app(self):
        left = self.parse_atom()
        # Application stops at keywords or tokens that delimit expressions.
        stop_tokens = [
            ",",
            ")",
            "in",
            "of",
            "|",
            "=>",
            "EOF",
            "=",  # existing
            "let",
            "case",
            "fn",
            "inl",
            "inr",
            "::",
            ":",  # new keywords
        ]
        while self.peek() is not None and self.peek() not in stop_tokens:
            left = App(left, self.parse_atom())
        return left

    def parse_expr(self):
        token = self.peek()

        if token == "fn":
            self.consume("fn")
            var = self.consume()
            self.consume(":")
            type = self.parse_type()
            self.consume("=>")
            body = self.parse_expr()
            return Fun(var, type, body)

        if token == "let":
            self.consume("let")
            if self.peek() == "(":
                # let pair
                self.consume("(")
                v1 = self.consume()
                self.consume(",")
                v2 = self.consume()
                self.consume(")")
                self.consume("=")
                e1 = self.parse_expr()
                self.consume("in")
                e2 = self.parse_expr()
                return LetPair(v1, v2, e1, e2)
            elif self.peek() == "!":
                # let bang
                self.consume("!")
                v = self.consume()
                self.consume("=")
                e1 = self.parse_expr()
                self.consume("in")
                e2 = self.parse_expr()
                return LetBang(v, e1, e2)
            else:
                # let var
                v = self.consume()
                self.consume("=")
                e1 = self.parse_expr()
                self.consume("in")
                e2 = self.parse_expr()
                return Let(v, e1, e2)

        if token == "case":
            self.consume("case")
            e = self.parse_expr()
            self.consume("of")

            # inl part
            self.consume("inl")
            v1 = self.consume()
            self.consume("=>")
            e1 = self.parse_expr()

            # inr part
            self.consume("|")
            self.consume("inr")
            v2 = self.consume()
            self.consume("=>")
            e2 = self.parse_expr()

            return Case(e, v1, e1, v2, e2)

        if token == "inl":
            self.consume("inl")
            self.consume("(")
            e = self.parse_expr()
            self.consume(",")
            t_right = self.parse_type()
            self.consume(")")
            return Inl(e, t_right)

        if token == "inr":
            self.consume("inr")
            self.consume("(")
            e = self.parse_expr()
            self.consume(",")
            t_left = self.parse_type()
            self.consume(")")
            return Inr(e, t_left)

        if token == "!":
            self.consume("!")
            return Promote(self.parse_expr())

        return self.parse_cons()

    def parse_cons(self):
        left = self.parse_app()
        if self.peek() == "::":
            self.consume("::")
            right = self.parse_cons()
            return Cons(left, right)
        return left

    def parse_type(self):
        token = self.consume()
        if token == "Int":
            return TInt()
        elif token == "String":
            return TString()
        elif token == "Bool":
            return TBool()
        elif token == "State":
            return TState()
        elif token == "Action":
            return TAction()
        elif token == "Goal":
            return TGoal()
        elif token == "Unit":
            return TUnit()
        elif token == "(":
            t1 = self.parse_type()
            op = self.consume()
            if op == "*":
                t2 = self.parse_type()
                self.consume(")")
                return TProd(t1, t2)
            elif op == "+":
                t2 = self.parse_type()
                self.consume(")")
                return TSum(t1, t2)
            elif op == "->":
                t2 = self.parse_type()
                self.consume(")")
                return TFun(t1, t2)
            else:
                raise ValueError(f"Unknown type operator: {op}")
        elif token == "!":
            return TExponential(self.parse_type())
        elif token.startswith("List"):  # e.g. List(Int)
            self.consume("(")
            inner_type = self.parse_type()
            self.consume(")")
            return TList(inner_type)
        else:
            raise ValueError(f"Unknown type: {token}")


def parse(s: str) -> Term:
    # Remove single-line comments
    s = re.sub(r"//.*", "", s)
    s = s.strip()
    tokens = re.findall(
        r'::|:|\(|\)|,|=>|->|=|\*|\+|!|\||\b(?:let|in|case|of|inl|inr|fn|unit|Int|String|Bool|State|Action|Goal|Unit|List|Cons|Nil)\b|\w+|"[^"]*"',
        s,
    )
    tokens = [t for t in tokens if t]
    parser = Parser(tokens)
    result = parser.parse_expr()
    if parser.peek() is not None:
        raise ValueError(
            f"Did not consume all tokens. Remaining: {parser.tokens[parser.pos:]}"
        )
    return result
