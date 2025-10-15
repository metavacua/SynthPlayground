from typing import Set, Optional
from .formulas import Formula, Tensor, LinImplies, OfCourse
from .sequents import Sequent
from .proof import ProofTree, Rule

class ILLSequent(Sequent):
    def __init__(self, antecedent: Set[Formula], succedent: Formula):
        super().__init__(antecedent, {succedent})

    @property
    def succedent_formula(self) -> Formula:
        # In ILL, there's always exactly one formula in the succedent.
        return list(self.succedent)[0]

    def __repr__(self):
        ant_str = ", ".join(map(str, sorted(list(self.antecedent), key=str)))
        suc_str = str(self.succedent_formula)
        return f"{ant_str} ⊢ {suc_str}"

# Axiom
def axiom(A: Formula) -> ProofTree:
    """A ⊢ A"""
    conclusion = ILLSequent({A}, A)
    return ProofTree(conclusion, Rule("Axiom"))

# Multiplicative Rules
def tensor_right(left_proof: ProofTree, right_proof: ProofTree, formula: Tensor) -> ProofTree:
    """Γ ⊢ A   and   Δ ⊢ B
    -----------------------
         Γ, Δ ⊢ A ⊗ B
    """
    if left_proof.conclusion.succedent_formula != formula.left or right_proof.conclusion.succedent_formula != formula.right:
        raise ValueError("Premises do not support the conclusion for ⊗-R")
    antecedent = left_proof.conclusion.antecedent | right_proof.conclusion.antecedent
    conclusion = ILLSequent(antecedent, formula)
    return ProofTree(conclusion, Rule("⊗-R"), [left_proof, right_proof])

def tensor_left(proof: ProofTree, formula: Tensor) -> ProofTree:
    """Γ, A, B ⊢ C
    ---------------
     Γ, A ⊗ B ⊢ C
    """
    if formula.left not in proof.conclusion.antecedent or formula.right not in proof.conclusion.antecedent:
        raise ValueError("Premise does not contain subformulas for ⊗-L")
    new_antecedent = (proof.conclusion.antecedent - {formula.left, formula.right}) | {formula}
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("⊗-L"), [proof])

def lin_implies_right(proof: ProofTree, formula: LinImplies) -> ProofTree:
    """Γ, A ⊢ B
    ------------
    Γ ⊢ A ⊸ B
    """
    if formula.left not in proof.conclusion.antecedent or formula.right != proof.conclusion.succedent_formula:
        raise ValueError("Premise does not support conclusion for ⊸-R")
    new_antecedent = proof.conclusion.antecedent - {formula.left}
    conclusion = ILLSequent(new_antecedent, formula)
    return ProofTree(conclusion, Rule("⊸-R"), [proof])

def lin_implies_left(left_proof: ProofTree, right_proof: ProofTree, formula: LinImplies) -> ProofTree:
    """Γ ⊢ A   and   Δ, B ⊢ C
    --------------------------
       Γ, Δ, A ⊸ B ⊢ C
    """
    if left_proof.conclusion.succedent_formula != formula.left or formula.right not in right_proof.conclusion.antecedent:
        raise ValueError("Premises do not support conclusion for ⊸-L")
    antecedent = (left_proof.conclusion.antecedent | (right_proof.conclusion.antecedent - {formula.right})) | {formula}
    succedent = right_proof.conclusion.succedent_formula
    conclusion = ILLSequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("⊸-L"), [left_proof, right_proof])

# Exponential Rules
def of_course_right(proof: ProofTree) -> ProofTree:
    """!Γ ⊢ A
    ----------
    !Γ ⊢ !A
    """
    # This rule requires a context with only "of course" formulas.
    for f in proof.conclusion.antecedent:
        if not isinstance(f, OfCourse):
            raise ValueError("Antecedent for !-R must only contain '!' formulas.")

    conclusion = ILLSequent(proof.conclusion.antecedent, OfCourse(proof.conclusion.succedent_formula))
    return ProofTree(conclusion, Rule("!-R"), [proof])

def dereliction(proof: ProofTree, formula: OfCourse) -> ProofTree:
    """Γ, A ⊢ B
    ------------
    Γ, !A ⊢ B
    """
    if formula.operand not in proof.conclusion.antecedent:
        raise ValueError("Premise does not contain the derelicted formula.")
    new_antecedent = (proof.conclusion.antecedent - {formula.operand}) | {formula}
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("Dereliction"), [proof])

def contraction(proof: ProofTree, formula: OfCourse) -> ProofTree:
    """Γ, !A, !A ⊢ B
    ----------------
       Γ, !A ⊢ B
    """
    # A simple way to check for two instances is to count them
    if list(proof.conclusion.antecedent).count(formula) < 2:
         raise ValueError("Premise does not contain two instances of the contracted formula.")

    # This is tricky with sets. A proper implementation would use multisets.
    # For this PoC, we will just remove one instance.
    new_antecedent = proof.conclusion.antecedent
    # NOTE: This rule is not correctly implemented due to the use of sets
    # instead of multisets. With a set, we cannot represent or remove
    # duplicate formulas, so this rule is a no-op. A full implementation
    # would require changing the antecedent to be a multiset.
    new_antecedent = (proof.conclusion.antecedent - {formula}) | {formula} # This is a no-op with sets
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("Contraction"), [proof])

def weakening(proof: ProofTree, formula: OfCourse) -> ProofTree:
    """Γ ⊢ B
    ------------
    Γ, !A ⊢ B
    """
    if formula in proof.conclusion.antecedent:
        raise ValueError("Formula to be weakened is already in the antecedent.")
    new_antecedent = proof.conclusion.antecedent | {formula}
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("Weakening"), [proof])