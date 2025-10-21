from abc import ABC, abstractmethod


class Formula(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))


class Prop(Formula):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class UnaryOp(Formula):
    def __init__(self, operand: Formula):
        self.operand = operand


class Not(UnaryOp):
    def __repr__(self):
        return f"¬({self.operand})"


class BinaryOp(Formula):
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right


class And(BinaryOp):
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"


class Or(BinaryOp):
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"


class Implies(BinaryOp):
    def __repr__(self):
        return f"({self.left} → {self.right})"


# --- Linear Logic Connectives ---


class Tensor(BinaryOp):
    def __repr__(self):
        return f"({self.left} ⊗ {self.right})"


class Par(BinaryOp):
    def __repr__(self):
        return f"({self.left} ⅋ {self.right})"


class LinImplies(BinaryOp):
    def __repr__(self):
        return f"({self.left} ⊸ {self.right})"


class OfCourse(UnaryOp):
    def __repr__(self):
        return f"!({self.operand})"


class With(BinaryOp):
    """Additive Conjunction"""

    def __repr__(self):
        return f"({self.left} & {self.right})"


class Plus(BinaryOp):
    """Additive Disjunction"""

    def __repr__(self):
        return f"({self.left} ⊕ {self.right})"
