from typing import Union

# Types
class TInt:
    def __repr__(self): return "TInt"
    def __eq__(self, other): return isinstance(other, TInt)

class TString:
    def __repr__(self): return "TString"
    def __eq__(self, other): return isinstance(other, TString)

class TBool:
    def __repr__(self): return "TBool"
    def __eq__(self, other): return isinstance(other, TBool)

class TUnit:
    def __repr__(self): return "TUnit"
    def __eq__(self, other): return isinstance(other, TUnit)

class TPar:
    def __repr__(self): return "TPar"
    def __eq__(self, other): return isinstance(other, TPar)

class TTensor:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self): return f"({self.t1} * {self.t2})"
    def __eq__(self, other): return isinstance(other, TTensor) and self.t1 == other.t1 and self.t2 == other.t2

class TFun:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self): return f"({self.t1} -o {self.t2})"
    def __eq__(self, other): return isinstance(other, TFun) and self.t1 == other.t1 and self.t2 == other.t2

class TWith:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self): return f"({self.t1} & {self.t2})"
    def __eq__(self, other): return isinstance(other, TWith) and self.t1 == other.t1 and self.t2 == other.t2

class TPlus:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __repr__(self): return f"({self.t1} + {self.t2})"
    def __eq__(self, other): return isinstance(other, TPlus) and self.t1 == other.t1 and self.t2 == other.t2

class TOfCourse:
    def __init__(self, t): self.t = t
    def __repr__(self): return f"!{self.t}"
    def __eq__(self, other): return isinstance(other, TOfCourse) and self.t == other.t

class TWhyNot:
    def __init__(self, t): self.t = t
    def __repr__(self): return f"?{self.t}"
    def __eq__(self, other): return isinstance(other, TWhyNot) and self.t == other.t

Type = Union[TInt, TString, TBool, TUnit, TPar, TTensor, TFun, TWith, TPlus, TOfCourse, TWhyNot]

# Terms
class Var:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Var({self.name})"
    def __eq__(self, other): return isinstance(other, Var) and self.name == other.name

class Int:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Int({self.value})"
    def __eq__(self, other): return isinstance(other, Int) and self.value == other.value

class String:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"String({self.value})"
    def __eq__(self, other): return isinstance(other, String) and self.value == other.value

class Bool:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Bool({self.value})"
    def __eq__(self, other): return isinstance(other, Bool) and self.value == other.value

class Unit:
    def __repr__(self): return "Unit"
    def __eq__(self, other): return isinstance(other, Unit)

class TensorPair:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self): return f"({self.e1} * {self.e2})"
    def __eq__(self, other): return isinstance(other, TensorPair) and self.e1 == other.e1 and self.e2 == other.e2

class LetTensor:
    def __init__(self, v1, v2, e1, e2):
        self.v1 = v1
        self.v2 = v2
        self.e1 = e1
        self.e2 = e2
    def __repr__(self): return f"let {self.v1} * {self.v2} = {self.e1} in {self.e2}"
    def __eq__(self, other): return isinstance(other, LetTensor) and self.v1 == other.v1 and self.v2 == other.v2 and self.e1 == other.e1 and self.e2 == other.e2

class Fun:
    def __init__(self, var, type_, body):
        self.var = var
        self.type_ = type_
        self.body = body
    def __repr__(self): return f"fun {self.var}:{self.type_} -> {self.body}"
    def __eq__(self, other): return isinstance(other, Fun) and self.var == other.var and self.type_ == other.type_ and self.body == other.body

class App:
    def __init__(self, f, arg):
        self.f = f
        self.arg = arg
    def __repr__(self): return f"({self.f} {self.arg})"
    def __eq__(self, other): return isinstance(other, App) and self.f == other.f and self.arg == other.arg

class WithPair:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
    def __repr__(self): return f"<{self.e1}, {self.e2}>"
    def __eq__(self, other): return isinstance(other, WithPair) and self.e1 == other.e1 and self.e2 == other.e2

class Fst:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"fst({self.e})"
    def __eq__(self, other): return isinstance(other, Fst) and self.e == other.e

class Snd:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"snd({self.e})"
    def __eq__(self, other): return isinstance(other, Snd) and self.e == other.e

class Inl:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"inl({self.e})"
    def __eq__(self, other): return isinstance(other, Inl) and self.e == other.e

class Inr:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"inr({self.e})"
    def __eq__(self, other): return isinstance(other, Inr) and self.e == other.e

class Case:
    def __init__(self, e, v1, e1, v2, e2):
        self.e = e
        self.v1 = v1
        self.e1 = e1
        self.v2 = v2
        self.e2 = e2
    def __repr__(self): return f"case {self.e} of inl({self.v1}) => {self.e1} | inr({self.v2}) => {self.e2}"
    def __eq__(self, other): return isinstance(other, Case) and self.e == other.e and self.v1 == other.v1 and self.e1 == other.e1 and self.v2 == other.v2 and self.e2 == other.e2

class Promotion:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"!{self.e}"
    def __eq__(self, other): return isinstance(other, Promotion) and self.e == other.e

class Dereliction:
    def __init__(self, v, e1, e2):
        self.v = v
        self.e1 = e1
        self.e2 = e2
    def __repr__(self): return f"let !{self.v} = {self.e1} in {self.e2}"
    def __eq__(self, other): return isinstance(other, Dereliction) and self.v == other.v and self.e1 == other.e1 and self.e2 == other.e2

class WhyNot:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"?{self.e}"
    def __eq__(self, other): return isinstance(other, WhyNot) and self.e == other.e

class LetWhyNot:
    def __init__(self, v, e1, e2):
        self.v = v
        self.e1 = e1
        self.e2 = e2
    def __repr__(self): return f"let ?{self.v} = {self.e1} in {self.e2}"
    def __eq__(self, other): return isinstance(other, LetWhyNot) and self.v == other.v and self.e1 == other.e1 and self.e2 == other.e2

class Par:
    def __init__(self, e): self.e = e
    def __repr__(self): return f"Par({self.e})"
    def __eq__(self, other): return isinstance(other, Par) and self.e == other.e

class LetPar:
    def __init__(self, v, e1, e2):
        self.v = v
        self.e1 = e1
        self.e2 = e2
    def __repr__(self): return f"let Par({self.v}) = {self.e1} in {self.e2}"
    def __eq__(self, other): return isinstance(other, LetPar) and self.v == other.v and self.e1 == other.e1 and self.e2 == other.e2


Term = Union[Var, Int, String, Bool, Unit, TensorPair, LetTensor, Fun, App, WithPair, Fst, Snd, Inl, Inr, Case, Promotion, Dereliction, WhyNot, LetWhyNot, Par, LetPar]