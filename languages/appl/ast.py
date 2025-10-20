from typing import Union

class TInt:
    def __repr__(self):
        return "TInt"
    def __eq__(self, other):
        return isinstance(other, TInt)

class TString:
    def __repr__(self):
        return "TString"
    def __eq__(self, other):
        return isinstance(other, TString)

class TBool:
    def __repr__(self):
        return "TBool"
    def __eq__(self, other):
        return isinstance(other, TBool)

class TState:
    def __repr__(self):
        return "TState"
    def __eq__(self, other):
        return isinstance(other, TState)

class TAction:
    def __repr__(self):
        return "TAction"
    def __eq__(self, other):
        return isinstance(other, TAction)

class TGoal:
    def __repr__(self):
        return "TGoal"
    def __eq__(self, other):
        return isinstance(other, TGoal)

class TUnit:
    def __repr__(self):
        return "TUnit"
    def __eq__(self, other):
        return isinstance(other, TUnit)

class TList:
    def __init__(self, t):
        self.t = t
    def __repr__(self):
        return f"TList({self.t})"
    def __eq__(self, other):
        return isinstance(other, TList) and self.t == other.t

class TTerm:
    def __repr__(self):
        return "TTerm"
    def __eq__(self, other):
        return isinstance(other, TTerm)

class TProd:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self):
        return f"({self.t1} * {self.t2})"
    def __eq__(self, other):
        return isinstance(other, TProd) and self.t1 == other.t1 and self.t2 == other.t2

class TSum:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self):
        return f"({self.t1} + {self.t2})"
    def __eq__(self, other):
        return isinstance(other, TSum) and self.t1 == other.t1 and self.t2 == other.t2

class TFun:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self):
        return f"({self.t1} -> {self.t2})"
    def __eq__(self, other):
        return isinstance(other, TFun) and self.t1 == other.t1 and self.t2 == other.t2

class TExponential:
    def __init__(self, t):
        self.t = t
    def __repr__(self):
        return f"!{self.t}"
    def __eq__(self, other):
        return isinstance(other, TExponential) and self.t == other.t

Type = Union[TInt, TString, TBool, TState, TAction, TGoal, TUnit, TList, TTerm, TProd, TSum, TFun, TExponential]

class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"
    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

class Int:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Int({self.value})"
    def __eq__(self, other):
        return isinstance(other, Int) and self.value == other.value

class String:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String({self.value})"
    def __eq__(self, other):
        return isinstance(other, String) and self.value == other.value

class Bool:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Bool({self.value})"
    def __eq__(self, other):
        return isinstance(other, Bool) and self.value == other.value

class App:
    def __init__(self, f, arg):
        self.f = f
        self.arg = arg
    def __repr__(self):
        return f"App({self.f}, {self.arg})"
    def __eq__(self, other):
        return isinstance(other, App) and self.f == other.f and self.arg == other.arg

class Fun:
    def __init__(self, var, type, body):
        self.var = var
        self.type = type
        self.body = body
    def __repr__(self):
        return f"Fun({self.var}: {self.type}, {self.body})"
    def __eq__(self, other):
        return isinstance(other, Fun) and self.var == other.var and self.type == other.type and self.body == other.body

class Pair:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return f"Pair({self.e1}, {self.e2})"
    def __eq__(self, other):
        return isinstance(other, Pair) and self.e1 == other.e1 and self.e2 == other.e2

class Let:
    def __init__(self, var, e1, e2):
        self.var = var
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return f"Let({self.var}, {self.e1}, {self.e2})"
    def __eq__(self, other):
        return isinstance(other, Let) and self.var == other.var and self.e1 == other.e1 and self.e2 == other.e2

class LetPair:
    def __init__(self, v1, v2, e1, e2):
        self.v1 = v1
        self.v2 = v2
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return f"LetPair(({self.v1}, {self.v2}), {self.e1}, {self.e2})"
    def __eq__(self, other):
        return isinstance(other, LetPair) and self.v1 == other.v1 and self.v2 == other.v2 and self.e1 == other.e1 and self.e2 == other.e2

class Inl:
    def __init__(self, e, t_right):
        self.e = e
        self.t_right = t_right
    def __repr__(self):
        return f"Inl({self.e}, {self.t_right})"
    def __eq__(self, other):
        return isinstance(other, Inl) and self.e == other.e and self.t_right == other.t_right

class Inr:
    def __init__(self, e, t_left):
        self.e = e
        self.t_left = t_left
    def __repr__(self):
        return f"Inr({self.e}, {self.t_left})"
    def __eq__(self, other):
        return isinstance(other, Inr) and self.e == other.e and self.t_left == other.t_left

class Case:
    def __init__(self, e, v1, e1, v2, e2):
        self.e = e
        self.v1 = v1
        self.e1 = e1
        self.v2 = v2
        self.e2 = e2
    def __repr__(self):
        return f"Case({self.e}, inl({self.v1}) => {self.e1}, inr({self.v2}) => {self.e2})"
    def __eq__(self, other):
        return isinstance(other, Case) and self.e == other.e and self.v1 == other.v1 and self.e1 == other.e1 and self.v2 == other.v2 and self.e2 == other.e2

class Promote:
    def __init__(self, e):
        self.e = e
    def __repr__(self):
        return f"Promote({self.e})"
    def __eq__(self, other):
        return isinstance(other, Promote) and self.e == other.e

class LetBang:
    def __init__(self, v, e1, e2):
        self.v = v
        self.e1 = e1
        self.e2 = e2
    def __repr__(self):
        return f"LetBang(!{self.v}, {self.e1}, {self.e2})"
    def __eq__(self, other):
        return isinstance(other, LetBang) and self.v == other.v and self.e1 == other.e1 and self.e2 == other.e2

class Unit:
    def __repr__(self):
        return "Unit"
    def __eq__(self, other):
        return isinstance(other, Unit)

class Nil:
    def __init__(self, type):
        self.type = type
    def __repr__(self):
        return f"Nil({self.type})"
    def __eq__(self, other):
        return isinstance(other, Nil) and self.type == other.type

class Cons:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
    def __repr__(self):
        return f"Cons({self.head}, {self.tail})"
    def __eq__(self, other):
        return isinstance(other, Cons) and self.head == other.head and self.tail == other.tail

class AST:
    def __init__(self, term):
        self.term = term
    def __repr__(self):
        return f"AST({self.term})"
    def __eq__(self, other):
        return isinstance(other, AST) and self.term == other.term

Term = Union[Var, Int, String, Bool, App, Fun, Pair, Let, LetPair, Inl, Inr, Case, Promote, LetBang, Unit, Nil, Cons, AST]