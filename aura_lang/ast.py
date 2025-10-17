# Abstract Syntax Tree (AST) node definitions for Aura-zero

class AST:
    pass

class Program(AST):
    def __init__(self, statements):
        self.statements = statements

class Statement(AST):
    pass

class Expression(AST):
    pass

class FunctionDefinition(Statement):
    def __init__(self, name, params, body):
        self.name = name  # An Identifier node
        self.params = params  # A list of Identifier nodes
        self.body = body  # A BlockStatement node

class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

class LetStatement(Statement):
    def __init__(self, name, value):
        self.name = name  # An Identifier node
        self.value = value  # An Expression node

class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value # An Expression node

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class IfStatement(Statement):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition # An Expression node
        self.consequence = consequence # A BlockStatement node
        self.alternative = alternative # A BlockStatement node or None

class ForStatement(Statement):
    def __init__(self, identifier, iterable, body):
        self.identifier = identifier # An Identifier node
        self.iterable = iterable # An Expression node
        self.body = body # A BlockStatement node

class UseStatement(Statement):
    # For now, this is just a placeholder. The interpreter will handle it.
    def __init__(self, path):
        self.path = path

class PrintStatement(Statement):
    # A dedicated statement for the 'print' keyword for simplicity
    def __init__(self, value):
        self.value = value

# --- Expressions ---

class Identifier(Expression):
    def __init__(self, value):
        self.value = value

class IntegerLiteral(Expression):
    def __init__(self, value):
        self.value = value

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

class ListLiteral(Expression):
    def __init__(self, elements):
        self.elements = elements

class CallExpression(Expression):
    def __init__(self, function, arguments):
        self.function = function  # Identifier
        self.arguments = arguments  # List of Expressions

class InfixExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class MemberAccess(Expression):
    def __init__(self, object, property):
        self.object = object # An expression
        self.property = property # An Identifier