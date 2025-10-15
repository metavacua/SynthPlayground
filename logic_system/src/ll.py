from collections import Counter
from .formulas import Formula, Tensor, Par
from .sequents import Sequent
from .proof import ProofTree, Rule

# Axiom
def axiom(A: Formula) -> ProofTree:
    """A ⊢ A"""
    conclusion = Sequent([A], [A])
    return ProofTree(conclusion, Rule("Axiom"))

# Multiplicative Rules

def tensor_right(left_proof: ProofTree, right_proof: ProofTree, formula: Tensor) -> ProofTree:
    """Γ ⊢ Δ, A   and   Γ' ⊢ Δ', B
    --------------------------------
          Γ, Γ' ⊢ Δ, Δ', A ⊗ B
    """
    A = formula.left
    B = formula.right
    if A not in left_proof.conclusion.succedent or B not in right_proof.conclusion.succedent:
        raise ValueError("Premises do not support the conclusion for ⊗-R")

    antecedent = left_proof.conclusion.antecedent + right_proof.conclusion.antecedent
    succedent = (left_proof.conclusion.succedent - Counter([A])) + (right_proof.conclusion.succedent - Counter([B])) + Counter([formula])
    conclusion = Sequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("⊗-R"), [left_proof, right_proof])

def tensor_left(proof: ProofTree, formula: Tensor) -> ProofTree:
    """Γ, A, B ⊢ Δ
    ---------------
     Γ, A ⊗ B ⊢ Δ
    """
    if formula.left not in proof.conclusion.antecedent or formula.right not in proof.conclusion.antecedent:
        raise ValueError("Premises do not support the conclusion for ⊗-L")
    new_antecedent = (proof.conclusion.antecedent - Counter([formula.left, formula.right])) + Counter([formula])
    conclusion = Sequent(new_antecedent, proof.conclusion.succedent)
    return ProofTree(conclusion, Rule("⊗-L"), [proof])

def par_right(proof: ProofTree, formula: Par) -> ProofTree:
    """Γ ⊢ Δ, A, B
    ---------------
     Γ ⊢ Δ, A ⅋ B
    """
    if formula.left not in proof.conclusion.succedent or formula.right not in proof.conclusion.succedent:
        raise ValueError("Premises do not support the conclusion for ⅋-R")
    new_succedent = (proof.conclusion.succedent - Counter([formula.left, formula.right])) + Counter([formula])
    conclusion = Sequent(proof.conclusion.antecedent, new_succedent)
    return ProofTree(conclusion, Rule("⅋-R"), [proof])

def par_left(left_proof: ProofTree, right_proof: ProofTree, formula: Par) -> ProofTree:
    """Γ, A ⊢ Δ   and   Γ', B ⊢ Δ'
    --------------------------------
          Γ, Γ', A ⅋ B ⊢ Δ, Δ'
    """
    A = formula.left
    B = formula.right
    if A not in left_proof.conclusion.antecedent or B not in right_proof.conclusion.antecedent:
        raise ValueError("Premises do not support the conclusion for ⅋-L")

    antecedent = (left_proof.conclusion.antecedent - Counter([A])) + (right_proof.conclusion.antecedent - Counter([B])) + Counter([formula])
    succedent = left_proof.conclusion.succedent + right_proof.conclusion.succedent
    conclusion = Sequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("⅋-L"), [left_proof, right_proof])

def cut(left_proof: ProofTree, right_proof: ProofTree) -> ProofTree:
    """Γ ⊢ Δ, A   and   A, Γ' ⊢ Δ'
    --------------------------------
             Γ, Γ' ⊢ Δ, Δ'
    """
    cut_formulas = left_proof.conclusion.succedent & right_proof.conclusion.antecedent
    if not cut_formulas:
        raise ValueError("Cut rule requires a common formula.")

    cut_formula = list(cut_formulas.elements())[0]

    antecedent = (left_proof.conclusion.antecedent + right_proof.conclusion.antecedent) - Counter([cut_formula])
    succedent = (left_proof.conclusion.succedent + right_proof.conclusion.succedent) - Counter([cut_formula])
    conclusion = Sequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("Cut"), [left_proof, right_proof])