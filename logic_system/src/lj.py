from typing import Optional, Iterable
from collections import Counter
from .formulas import Formula, And, Or, Implies, Not
from .sequents import Sequent
from .proof import ProofTree, Rule


class LJSequent(Sequent):
    def __init__(
        self, antecedent: Iterable[Formula], succedent: Optional[Formula] = None
    ):
        super().__init__(antecedent, [succedent] if succedent else [])
        if len(self.succedent) > 1:
            raise ValueError(
                "LJ sequents can have at most one formula in the succedent."
            )

    @property
    def succedent_formula(self) -> Optional[Formula]:
        if not self.succedent:
            return None
        return list(self.succedent.elements())[0]

    def __repr__(self):
        # Overriding for custom representation
        ant_str = ", ".join(map(str, self.antecedent.elements()))
        suc_str = str(self.succedent_formula) if self.succedent_formula else ""
        return f"{ant_str} ⊢ {suc_str}"


# Axiom
def axiom(A: Formula) -> ProofTree:
    """A ⊢ A"""
    conclusion = LJSequent([A], A)
    return ProofTree(conclusion, Rule("Axiom"))


# Structural Rules
def weak_left(proof: ProofTree, formula: Formula) -> ProofTree:
    """Γ ⊢ Δ  /  Γ, A ⊢ Δ"""
    conclusion = LJSequent(
        proof.conclusion.antecedent + Counter([formula]),
        proof.conclusion.succedent_formula,
    )
    return ProofTree(conclusion, Rule("Weak-L"), [proof])


def cut(left_proof: ProofTree, right_proof: ProofTree, formula: Formula) -> ProofTree:
    """Γ ⊢ A   and   A, Γ' ⊢ B / Γ, Γ' ⊢ B"""
    antecedent = (
        left_proof.conclusion.antecedent + right_proof.conclusion.antecedent
    ) - Counter([formula])
    succedent = right_proof.conclusion.succedent_formula
    conclusion = LJSequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("Cut"), [left_proof, right_proof])


# Logical Rules
def and_left(proof: ProofTree, formula: And) -> ProofTree:
    """Γ, A, B ⊢ Δ / Γ, A ∧ B ⊢ Δ"""
    new_antecedent = (
        proof.conclusion.antecedent - Counter([formula.left, formula.right])
    ) + Counter([formula])
    conclusion = LJSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("∧-L"), [proof])


def and_right(left_proof: ProofTree, right_proof: ProofTree) -> ProofTree:
    """Γ ⊢ A   and   Γ ⊢ B / Γ ⊢ A ∧ B"""
    formula = And(
        left_proof.conclusion.succedent_formula,
        right_proof.conclusion.succedent_formula,
    )
    antecedent = left_proof.conclusion.antecedent + right_proof.conclusion.antecedent
    conclusion = LJSequent(antecedent, formula)
    return ProofTree(conclusion, Rule("∧-R"), [left_proof, right_proof])


def or_left(left_proof: ProofTree, right_proof: ProofTree, formula: Or) -> ProofTree:
    """Γ, A ⊢ Δ   and   Γ, B ⊢ Δ / Γ, A ∨ B ⊢ Δ"""
    antecedent = (
        (left_proof.conclusion.antecedent - Counter([formula.left]))
        + (right_proof.conclusion.antecedent - Counter([formula.right]))
        + Counter([formula])
    )
    succedent = (
        left_proof.conclusion.succedent_formula
    )  # Should be the same in both proofs
    conclusion = LJSequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("∨-L"), [left_proof, right_proof])


def or_right(proof: ProofTree, formula: Or) -> ProofTree:
    """Γ ⊢ A / Γ ⊢ A ∨ B  or  Γ ⊢ B / Γ ⊢ A ∨ B"""
    conclusion = LJSequent(proof.conclusion.antecedent, formula)
    return ProofTree(conclusion, Rule("∨-R"), [proof])


def implies_left(
    left_proof: ProofTree, right_proof: ProofTree, formula: Implies
) -> ProofTree:
    """Γ ⊢ A   and   B, Γ' ⊢ C / A → B, Γ, Γ' ⊢ C"""
    antecedent = (
        left_proof.conclusion.antecedent + right_proof.conclusion.antecedent
    ) + Counter([formula])
    succedent = right_proof.conclusion.succedent_formula
    conclusion = LJSequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("→-L"), [left_proof, right_proof])


def implies_right(proof: ProofTree, formula: Implies) -> ProofTree:
    """A, Γ ⊢ B / Γ ⊢ A → B"""
    new_antecedent = proof.conclusion.antecedent - Counter([formula.left])
    conclusion = LJSequent(new_antecedent, formula)
    return ProofTree(conclusion, Rule("→-R"), [proof])


def not_left(proof: ProofTree, formula: Not) -> ProofTree:
    """Γ ⊢ A / ¬A, Γ ⊢"""
    new_antecedent = proof.conclusion.antecedent + Counter([formula])
    conclusion = LJSequent(new_antecedent, None)
    return ProofTree(conclusion, Rule("¬-L"), [proof])


def not_right(proof: ProofTree, formula: Not) -> ProofTree:
    """A, Γ ⊢ / Γ ⊢ ¬A"""
    new_antecedent = proof.conclusion.antecedent - Counter([formula.operand])
    conclusion = LJSequent(new_antecedent, formula)
    return ProofTree(conclusion, Rule("¬-R"), [proof])
