from . import lj
from . import lk
from .proof import ProofTree, Rule

def lj_to_lk(lj_proof: ProofTree) -> ProofTree:
    """
    Translates a proof from the LJ calculus to the LK calculus.
    This is a direct embedding, as any valid LJ proof is also a valid LK proof.
    """
    translated_premises = [lj_to_lk(p) for p in lj_proof.premises]

    return ProofTree(
        conclusion=lk.Sequent(lj_proof.conclusion.antecedent, lj_proof.conclusion.succedent),
        rule=lj_proof.rule,
        premises=translated_premises
    )

from .formulas import Formula, Prop, And, Or, Implies, Not, Tensor, Par, LinImplies, OfCourse, With, Plus

def translate_formula_lj_to_ill(formula: Formula) -> Formula:
    """
    Translates a formula from Intuitionistic Logic (LJ) to Intuitionistic Linear Logic (ILL)
    using a standard Girard-style translation.
    """
    if isinstance(formula, Prop):
        return formula # Atoms are translated to themselves
    elif isinstance(formula, And):
        return With(translate_formula_lj_to_ill(formula.left), translate_formula_lj_to_ill(formula.right))
    elif isinstance(formula, Or):
        return Plus(OfCourse(translate_formula_lj_to_ill(formula.left)), OfCourse(translate_formula_lj_to_ill(formula.right)))
    elif isinstance(formula, Implies):
        return OfCourse(LinImplies(translate_formula_lj_to_ill(formula.left), translate_formula_lj_to_ill(formula.right)))
    elif isinstance(formula, Not):
        # This translation typically requires a bottom element in linear logic.
        # We'll represent it with a special proposition for now.
        bottom = Prop("⊥")
        return OfCourse(LinImplies(translate_formula_lj_to_ill(formula.operand), bottom))
    else:
        raise TypeError(f"Unknown formula type for translation: {type(formula)}")

from . import ill

def lj_to_ill_proof(lj_proof: ProofTree) -> ProofTree:
    """
    Translates a full proof from LJ to ILL.
    A proof of Γ ⊢ A in LJ becomes a proof of !Γ* ⊢ A* in ILL.

    NOTE: This is a placeholder implementation for the proof-of-concept.
    A full, correct implementation of this translation is highly non-trivial
    and would require a dedicated theorem prover or proof synthesizer for
    Intuitionistic Linear Logic. This function demonstrates the principle for
    a few key rules but is not guaranteed to be correct or complete.
    """

    rule_name = lj_proof.rule.name

    if rule_name == "Axiom":
        # LJ: A ⊢ A
        # ILL: !A* ⊢ A*
        formula = set(lj_proof.conclusion.antecedent).pop()
        formula_star = translate_formula_lj_to_ill(formula)
        # Start with the axiom A* ⊢ A*
        axiom_proof = ill.axiom(formula_star)
        # Apply dereliction to get !A* ⊢ A*
        return ill.dereliction(axiom_proof, OfCourse(formula_star))

    elif rule_name == "→-R":
        # LJ: Γ, A ⊢ B  /  Γ ⊢ A → B
        # ILL: !Γ*, !A* ⊢ B*  /  !Γ* ⊢ !(A* ⊸ B*)
        premise_proof = lj_proof.premises[0]
        translated_premise = lj_to_ill_proof(premise_proof)

        # We have a proof of !Γ*, !A* ⊢ B*
        # We need to get to !Γ* ⊢ !(A* ⊸ B*)

        # First, apply ⊸-R to get !Γ* ⊢ !A* ⊸ B*
        # This requires some manipulation of the context that is not straightforward.
        # For this PoC, we will assume the premise translation gives us what we need
        # and apply the final rules.

        implication = set(lj_proof.conclusion.succedent).pop()
        ill_implication = translate_formula_lj_to_ill(implication) # This will be !(A* ⊸ B*)

        # Let's assume we have a proof of !Γ* ⊢ A* ⊸ B*
        # We then need to apply the !-R rule to get !Γ* ⊢ !(A* ⊸ B*)
        # This requires the context !Γ* to be all "of course" formulas, which it is by our induction hypothesis.

        # This part of the translation is highly non-trivial and requires a full proof
        # synthesizer. For the PoC, we will return a placeholder.
        return ProofTree(
            conclusion=ill.ILLSequent(
                {OfCourse(translate_formula_lj_to_ill(f)) for f in lj_proof.conclusion.antecedent},
                translate_formula_lj_to_ill(set(lj_proof.conclusion.succedent).pop())
            ),
            rule=Rule("→-R (Translated)"),
            premises=[translated_premise]
        )

    else:
        # For other rules, we'll just translate the conclusion and premises recursively for now.
        translated_premises = [lj_to_ill_proof(p) for p in lj_proof.premises]
        return ProofTree(
            conclusion=ill.ILLSequent(
                {OfCourse(translate_formula_lj_to_ill(f)) for f in lj_proof.conclusion.antecedent},
                translate_formula_lj_to_ill(set(lj_proof.conclusion.succedent).pop())
            ),
            rule=Rule(f"{rule_name} (Translated)"),
            premises=translated_premises
        )

def ill_to_ll(ill_proof: ProofTree) -> ProofTree:
    """
    Translates a proof from the ILL calculus to the LL calculus.
    This is a direct embedding, as any valid ILL proof is also a valid LL proof.
    """
    translated_premises = [ill_to_ll(p) for p in ill_proof.premises]

    return ProofTree(
        conclusion=lk.Sequent(ill_proof.conclusion.antecedent, ill_proof.conclusion.succedent),
        rule=ill_proof.rule,
        premises=translated_premises
    )