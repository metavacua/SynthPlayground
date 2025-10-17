from __future__ import annotations
from dataclasses import dataclass

# Base class for all formulas
class Formula:
    def neg(self) -> Formula:
        raise NotImplementedError

# Atoms and their linear negations
@dataclass(frozen=True, eq=True)
class Atom(Formula):
    name: str
    negated: bool = False

    def __repr__(self) -> str:
        return f"{self.name}{'⊥' if self.negated else ''}"

    def neg(self) -> Atom:
        return Atom(self.name, not self.negated)

# Multiplicative Connectives
@dataclass(frozen=True, eq=True)
class Tensor(Formula):
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ⊗ {self.right})"

    def neg(self) -> Par:
        return Par(self.left.neg(), self.right.neg())

@dataclass(frozen=True, eq=True)
class Par(Formula):
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ⅋ {self.right})"

    def neg(self) -> Tensor:
        return Tensor(self.left.neg(), self.right.neg())

@dataclass(frozen=True, eq=True)
class One(Formula):
    def __repr__(self) -> str:
        return "1"

    def neg(self) -> Bottom:
        return Bottom()

@dataclass(frozen=True, eq=True)
class Bottom(Formula):
    def __repr__(self) -> str:
        return "⊥"

    def neg(self) -> One:
        return One()

# Additive Connectives
@dataclass(frozen=True, eq=True)
class With(Formula):
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} & {self.right})"

    def neg(self) -> Plus:
        return Plus(self.left.neg(), self.right.neg())

@dataclass(frozen=True, eq=True)
class Plus(Formula):
    left: Formula
    right: Formula

    def __repr__(self) -> str:
        return f"({self.left} ⊕ {self.right})"

    def neg(self) -> With:
        return With(self.left.neg(), self.right.neg())

@dataclass(frozen=True, eq=True)
class Top(Formula):
    def __repr__(self) -> str:
        return "⊤"

    def neg(self) -> Zero:
        return Zero()

@dataclass(frozen=True, eq=True)
class Zero(Formula):
    def __repr__(self) -> str:
        return "0"

    def neg(self) -> Top:
        return Top()

# Modal Operators
@dataclass(frozen=True, eq=True)
class OfCourse(Formula):
    formula: Formula

    def __repr__(self) -> str:
        return f"!{self.formula}"

    def neg(self) -> WhyNot:
        return WhyNot(self.formula.neg())

@dataclass(frozen=True, eq=True)
class WhyNot(Formula):
    formula: Formula

    def __repr__(self) -> str:
        return f"?{self.formula}"

    def neg(self) -> OfCourse:
        return OfCourse(self.formula.neg())

@dataclass(frozen=True, eq=True)
class Section(Formula):
    formula: Formula

    def __repr__(self) -> str:
        return f"§{self.formula}"

    def neg(self) -> Section:
        return Section(self.formula.neg())

# Paraconsistent and Other Operators
@dataclass(frozen=True, eq=True)
class Negation(Formula):
    formula: Formula

    def __repr__(self) -> str:
        return f"¬{self.formula}"

    def neg(self) -> NegationPerp:
        return NegationPerp(self)

@dataclass(frozen=True, eq=True)
class NegationPerp(Formula):
    formula: Formula # Should be a Negation instance

    def __repr__(self) -> str:
        return f"({self.formula})⊥"

    def neg(self) -> Formula:
        return self.formula

@dataclass(frozen=True, eq=True)
class Consistency(Formula):
    formula: Formula

    def __repr__(self) -> str:
        return f"∘{self.formula}"

    def neg(self) -> Inconsistency:
        return Inconsistency(self)

@dataclass(frozen=True, eq=True)
class Inconsistency(Formula):
    formula: Formula # Should be a Consistency instance

    def __repr__(self) -> str:
        return f"({self.formula})⊥"

    def neg(self) -> Formula:
        return self.formula

@dataclass(frozen=True, eq=True)
class Completeness(Formula):
    formula: Formula

    def __repr__(self) -> str:
        return f"~{self.formula}"

    def neg(self) -> NonCompleteness:
        return NonCompleteness(self)

@dataclass(frozen=True, eq=True)
class NonCompleteness(Formula):
    formula: Formula # Should be a Completeness instance

    def __repr__(self) -> str:
        return f"({self.formula})⊥"

    def neg(self) -> Formula:
        return self.formula