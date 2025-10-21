from collections import Counter
from .formulas import Formula, And, Or, Implies, Not
from .sequents import Sequent
from .proof import ProofTree, Rule


# Axiom
def axiom(A: Formula) -> ProofTree:
    """A ⊢ A"""
    conclusion = Sequent([A], [A])
    return ProofTree(conclusion, Rule("Axiom"))


# Structural Rules
def weak_left(proof: ProofTree, formula: Formula) -> ProofTree:
    """Γ ⊢ Δ  /  Γ, A ⊢ Δ"""
    conclusion = Sequent(
        proof.conclusion.antecedent + Counter([formula]), proof.conclusion.succedent
    )
    return ProofTree(conclusion, Rule("Weak-L"), [proof])


def weak_right(proof: ProofTree, formula: Formula) -> ProofTree:
    """Γ ⊢ Δ  /  Γ ⊢ Δ, A"""
    conclusion = Sequent(
        proof.conclusion.antecedent, proof.conclusion.succedent + Counter([formula])
    )
    return ProofTree(conclusion, Rule("Weak-R"), [proof])


# Logical Rules
def and_left(proof: ProofTree, formula: And) -> ProofTree:
    """Γ, A, B ⊢ Δ / Γ, A ∧ B ⊢ Δ"""
    new_antecedent = (
        proof.conclusion.antecedent - Counter([formula.left, formula.right])
    ) + Counter([formula])
    conclusion = Sequent(new_antecedent, proof.conclusion.succedent)
    return ProofTree(conclusion, Rule("∧-L"), [proof])


def and_right(left_proof: ProofTree, right_proof: ProofTree) -> ProofTree:
    """Γ ⊢ Δ, A   and   Γ ⊢ Δ, B / Γ ⊢ Δ, A ∧ B"""
    # This rule is additive in LK, meaning contexts are shared.
    # We assume Γ and Δ are the same in both premises.
    A = list(left_proof.conclusion.succedent.elements())[
        0
    ]  # A more robust way to get the formula might be needed
    B = list(right_proof.conclusion.succedent.elements())[0]
    formula = And(A, B)
    antecedent = left_proof.conclusion.antecedent
    succedent = (
        (left_proof.conclusion.succedent - Counter([A]))
        + (right_proof.conclusion.succedent - Counter([B]))
        + Counter([formula])
    )
    conclusion = Sequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("∧-R"), [left_proof, right_proof])


def or_left(left_proof: ProofTree, right_proof: ProofTree) -> ProofTree:
    """Γ, A ⊢ Δ   and   Γ, B ⊢ Δ / Γ, A ∨ B ⊢ Δ"""
    A = list(left_proof.conclusion.antecedent.elements())[0]
    B = list(right_proof.conclusion.antecedent.elements())[0]
    formula = Or(A, B)
    antecedent = (
        (left_proof.conclusion.antecedent - Counter([A]))
        + (right_proof.conclusion.antecedent - Counter([B]))
        + Counter([formula])
    )
    succedent = left_proof.conclusion.succedent
    conclusion = Sequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("∨-L"), [left_proof, right_proof])


def or_right(proof: ProofTree, formula: Or) -> ProofTree:
    """Γ ⊢ Δ, A, B / Γ ⊢ Δ, A ∨ B"""
    new_succedent = (
        proof.conclusion.succedent - Counter([formula.left, formula.right])
    ) + Counter([formula])
    conclusion = Sequent(proof.conclusion.antecedent, new_succedent)
    return ProofTree(conclusion, Rule("∨-R"), [proof])


def implies_left(
    left_proof: ProofTree, right_proof: ProofTree, formula: Implies
) -> ProofTree:
    """Γ ⊢ Δ, A   and   B, Γ ⊢ Δ / A → B, Γ ⊢ Δ"""
    antecedent = (
        left_proof.conclusion.antecedent + right_proof.conclusion.antecedent
    ) + Counter([formula])
    succedent = (left_proof.conclusion.succedent - Counter([formula.left])) + (
        right_proof.conclusion.succedent - Counter([formula.right])
    )
    conclusion = Sequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("→-L"), [left_proof, right_proof])


def implies_right(proof: ProofTree, formula: Implies) -> ProofTree:
    """A, Γ ⊢ Δ, B / Γ ⊢ Δ, A → B"""
    new_antecedent = proof.conclusion.antecedent - Counter([formula.left])
    new_succedent = (proof.conclusion.succedent - Counter([formula.right])) + Counter(
        [formula]
    )
    conclusion = Sequent(new_antecedent, new_succedent)
    return ProofTree(conclusion, Rule("→-R"), [proof])


def not_left(proof: ProofTree, formula: Not) -> ProofTree:
    """Γ ⊢ Δ, A / ¬A, Γ ⊢ Δ"""
    new_antecedent = proof.conclusion.antecedent + Counter([formula])
    new_succedent = proof.conclusion.succedent - Counter([formula.operand])
    conclusion = Sequent(new_antecedent, new_succedent)
    return ProofTree(conclusion, Rule("¬-L"), [proof])


def not_right(proof: ProofTree, formula: Not) -> ProofTree:
    """A, Γ ⊢ Δ / Γ ⊢ Δ, ¬A"""
    new_antecedent = proof.conclusion.antecedent - Counter([formula.operand])
    new_succedent = proof.conclusion.succedent + Counter([formula])
    conclusion = Sequent(new_antecedent, new_succedent)
    return ProofTree(conclusion, Rule("¬-R"), [proof])
