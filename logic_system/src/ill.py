from typing import Iterable, Optional
from collections import Counter
from .formulas import Formula, Tensor, LinImplies, OfCourse, With, Plus
from .sequents import Sequent
from .proof import ProofTree, Rule

class ILLSequent(Sequent):
    def __init__(self, antecedent: Iterable[Formula], succedent: Formula):
        super().__init__(antecedent, [succedent])
        if len(self.succedent) != 1:
            raise ValueError("ILL sequents must have exactly one formula in the succedent.")

    @property
    def succedent_formula(self) -> Formula:
        return list(self.succedent.elements())[0]

    def __repr__(self):
        # Overriding for custom representation
        ant_str = ", ".join(map(str, self.antecedent.elements()))
        suc_str = str(self.succedent_formula)
        return f"{ant_str} ⊢ {suc_str}"

# Axiom
def axiom(A: Formula) -> ProofTree:
    """A ⊢ A"""
    conclusion = ILLSequent([A], A)
    return ProofTree(conclusion, Rule("Axiom"))

# Structural Rule
def cut(left_proof: ProofTree, right_proof: ProofTree) -> ProofTree:
    """Γ ⊢ A   and   Δ, A ⊢ C
    --------------------------
         Γ, Δ ⊢ C
    """
    cut_formula = left_proof.conclusion.succedent_formula
    if cut_formula not in right_proof.conclusion.antecedent:
        raise ValueError("Cut formula not found in the antecedent of the right premise.")

    antecedent = left_proof.conclusion.antecedent + (right_proof.conclusion.antecedent - Counter([cut_formula]))
    succedent = right_proof.conclusion.succedent_formula
    conclusion = ILLSequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("Cut"), [left_proof, right_proof])

# Multiplicative Rules
def tensor_right(left_proof: ProofTree, right_proof: ProofTree, formula: Tensor) -> ProofTree:
    """Γ ⊢ A   and   Δ ⊢ B
    -----------------------
         Γ, Δ ⊢ A ⊗ B
    """
    if left_proof.conclusion.succedent_formula != formula.left or right_proof.conclusion.succedent_formula != formula.right:
        raise ValueError("Premises do not support the conclusion for ⊗-R")
    antecedent = left_proof.conclusion.antecedent + right_proof.conclusion.antecedent
    conclusion = ILLSequent(antecedent, formula)
    return ProofTree(conclusion, Rule("⊗-R"), [left_proof, right_proof])

def tensor_left(proof: ProofTree, formula: Tensor) -> ProofTree:
    """Γ, A, B ⊢ C
    ---------------
     Γ, A ⊗ B ⊢ C
    """
    if formula.left not in proof.conclusion.antecedent or formula.right not in proof.conclusion.antecedent:
        raise ValueError("Premise does not contain subformulas for ⊗-L")
    new_antecedent = (proof.conclusion.antecedent - Counter([formula.left, formula.right])) + Counter([formula])
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("⊗-L"), [proof])

def lin_implies_right(proof: ProofTree, formula: LinImplies) -> ProofTree:
    """Γ, A ⊢ B
    ------------
    Γ ⊢ A ⊸ B
    """
    if formula.left not in proof.conclusion.antecedent or formula.right != proof.conclusion.succedent_formula:
        raise ValueError("Premise does not support conclusion for ⊸-R")
    new_antecedent = proof.conclusion.antecedent - Counter([formula.left])
    conclusion = ILLSequent(new_antecedent, formula)
    return ProofTree(conclusion, Rule("⊸-R"), [proof])

def lin_implies_left(left_proof: ProofTree, right_proof: ProofTree, formula: LinImplies) -> ProofTree:
    """Γ ⊢ A   and   Δ, B ⊢ C
    --------------------------
       Γ, Δ, A ⊸ B ⊢ C
    """
    if left_proof.conclusion.succedent_formula != formula.left or formula.right not in right_proof.conclusion.antecedent:
        raise ValueError("Premises do not support conclusion for ⊸-L")
    antecedent = (left_proof.conclusion.antecedent + (right_proof.conclusion.antecedent - Counter([formula.right]))) + Counter([formula])
    succedent = right_proof.conclusion.succedent_formula
    conclusion = ILLSequent(antecedent, succedent)
    return ProofTree(conclusion, Rule("⊸-L"), [left_proof, right_proof])

# Additive Rules
def with_right(left_proof: ProofTree, right_proof: ProofTree, formula: With) -> ProofTree:
    """Γ ⊢ A   and   Γ ⊢ B
    -----------------------
          Γ ⊢ A & B
    """
    if left_proof.conclusion.antecedent != right_proof.conclusion.antecedent:
        raise ValueError("Antecedents must be the same for &-R.")
    if left_proof.conclusion.succedent_formula != formula.left or right_proof.conclusion.succedent_formula != formula.right:
        raise ValueError("Premises do not support the conclusion for &-R")

    conclusion = ILLSequent(left_proof.conclusion.antecedent, formula)
    return ProofTree(conclusion, Rule("&-R"), [left_proof, right_proof])

def with_left(proof: ProofTree, formula: With, chosen_formula: Formula) -> ProofTree:
    """Γ, A ⊢ C
    ------------
    Γ, A & B ⊢ C
    or
    Γ, B ⊢ C
    ------------
    Γ, A & B ⊢ C
    """
    if chosen_formula not in [formula.left, formula.right]:
        raise ValueError("Chosen formula must be a subformula of the With formula.")
    if chosen_formula not in proof.conclusion.antecedent:
        raise ValueError("Premise does not contain the chosen subformula.")

    new_antecedent = (proof.conclusion.antecedent - Counter([chosen_formula])) + Counter([formula])
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("&-L"), [proof])


def plus_right_1(proof: ProofTree, formula: Plus) -> ProofTree:
    """Γ ⊢ A
    ------------
    Γ ⊢ A ⊕ B
    """
    if proof.conclusion.succedent_formula != formula.left:
        raise ValueError("Premise does not support conclusion for ⊕-R1")
    conclusion = ILLSequent(proof.conclusion.antecedent, formula)
    return ProofTree(conclusion, Rule("⊕-R1"), [proof])

def plus_right_2(proof: ProofTree, formula: Plus) -> ProofTree:
    """Γ ⊢ B
    ------------
    Γ ⊢ A ⊕ B
    """
    if proof.conclusion.succedent_formula != formula.right:
        raise ValueError("Premise does not support conclusion for ⊕-R2")
    conclusion = ILLSequent(proof.conclusion.antecedent, formula)
    return ProofTree(conclusion, Rule("⊕-R2"), [proof])

def plus_left(left_proof: ProofTree, right_proof: ProofTree, formula: Plus) -> ProofTree:
    """Γ, A ⊢ C   and   Γ, B ⊢ C
    --------------------------
         Γ, A ⊕ B ⊢ C
    """
    if left_proof.conclusion.succedent_formula != right_proof.conclusion.succedent_formula:
        raise ValueError("Succedents must be the same for ⊕-L")
    if formula.left not in left_proof.conclusion.antecedent or formula.right not in right_proof.conclusion.antecedent:
        raise ValueError("Premises do not contain the correct subformulas for ⊕-L")

    # Contexts must be the same except for the formula being replaced
    if (left_proof.conclusion.antecedent - Counter([formula.left])) != (right_proof.conclusion.antecedent - Counter([formula.right])):
        raise ValueError("Contexts must be the same for ⊕-L")

    antecedent = (left_proof.conclusion.antecedent - Counter([formula.left])) + Counter([formula])
    conclusion = ILLSequent(antecedent, left_proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("⊕-L"), [left_proof, right_proof])


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
    new_antecedent = (proof.conclusion.antecedent - Counter([formula.operand])) + Counter([formula])
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("Dereliction"), [proof])

def contraction(proof: ProofTree, formula: OfCourse) -> ProofTree:
    """Γ, !A, !A ⊢ B
    ----------------
       Γ, !A ⊢ B
    """
    if proof.conclusion.antecedent[formula] < 2:
         raise ValueError("Premise does not contain two instances of the contracted formula.")

    # Remove one instance of the !A formula
    new_antecedent = proof.conclusion.antecedent - Counter([formula])
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("Contraction"), [proof])

def weakening(proof: ProofTree, formula: OfCourse) -> ProofTree:
    """Γ ⊢ B
    ------------
    Γ, !A ⊢ B
    """
    # This rule in ILL is for weakening a !-formula from the antecedent.
    # The premise should not contain the formula that is being weakened in.
    # The correct rule is Γ, !A ⊢ B / Γ ⊢ B, which is "forgetting".
    # The rule Γ ⊢ B / Γ, !A ⊢ B is also a form of weakening.
    # We will implement the latter.
    new_antecedent = proof.conclusion.antecedent + Counter([formula])
    conclusion = ILLSequent(new_antecedent, proof.conclusion.succedent_formula)
    return ProofTree(conclusion, Rule("Weakening"), [proof])