from . import lk
from . import ill
from .proof import ProofTree, Rule
from .formulas import (
    Formula,
    Prop,
    And,
    Or,
    Implies,
    Not,
    LinImplies,
    OfCourse,
    With,
    Plus,
)
from .synthesizer import Synthesizer
from collections import Counter


def lj_to_lk(lj_proof: ProofTree) -> ProofTree:
    """
    Translates a proof from the LJ calculus to the LK calculus.
    This is a direct embedding, as any valid LJ proof is also a valid LK proof.
    """
    translated_premises = [lj_to_lk(p) for p in lj_proof.premises]

    return ProofTree(
        conclusion=lk.Sequent(
            lj_proof.conclusion.antecedent, lj_proof.conclusion.succedent
        ),
        rule=lj_proof.rule,
        premises=translated_premises,
    )


def translate_formula_lj_to_ill(formula: Formula) -> Formula:
    """
    Translates a formula from Intuitionistic Logic (LJ) to Intuitionistic Linear Logic (ILL)
    using a standard Girard-style translation.
    """
    if isinstance(formula, Prop):
        return formula  # Atoms are translated to themselves
    elif isinstance(formula, And):
        return With(
            translate_formula_lj_to_ill(formula.left),
            translate_formula_lj_to_ill(formula.right),
        )
    elif isinstance(formula, Or):
        return Plus(
            OfCourse(translate_formula_lj_to_ill(formula.left)),
            OfCourse(translate_formula_lj_to_ill(formula.right)),
        )
    elif isinstance(formula, Implies):
        # A -> B becomes !(A* -o B*)
        return OfCourse(
            LinImplies(
                OfCourse(translate_formula_lj_to_ill(formula.left)),
                OfCourse(translate_formula_lj_to_ill(formula.right)),
            )
        )
    elif isinstance(formula, Not):
        # Not A is A -> bottom, so !(A* -o bottom)
        bottom = Prop("⊥")
        return OfCourse(
            LinImplies(
                OfCourse(translate_formula_lj_to_ill(formula.operand)), OfCourse(bottom)
            )
        )
    else:
        raise TypeError(f"Unknown formula type for translation: {type(formula)}")


def bang_context(context: Counter) -> Counter:
    """Applies ! to every formula in a context."""
    return Counter({OfCourse(f): c for f, c in context.items()})


def lj_to_ill_proof(lj_proof: ProofTree) -> ProofTree:
    """
    Translates a full proof from LJ to ILL.
    A proof of Γ ⊢ A in LJ becomes a proof of !Γ* ⊢ A* in ILL.
    """
    rule_name = lj_proof.rule.name
    conclusion = lj_proof.conclusion
    premises = lj_proof.premises
    ill_synthesizer = Synthesizer(ill)

    if rule_name == "Axiom":
        formula = list(conclusion.antecedent.elements())[0]
        formula_star = translate_formula_lj_to_ill(formula)
        axiom_proof = ill.axiom(formula_star)
        return ill.dereliction(axiom_proof, OfCourse(formula_star))

    elif rule_name == "∧-R":
        left_premise = lj_to_ill_proof(premises[0])
        right_premise = lj_to_ill_proof(premises[1])
        formula = conclusion.succedent_formula
        formula_star = translate_formula_lj_to_ill(formula)
        return ill.with_right(left_premise, right_premise)

    elif rule_name == "∧-L":
        premise = lj_to_ill_proof(premises[0])
        formula = And(
            premises[0].conclusion.antecedent.elements()[0],
            premises[0].conclusion.antecedent.elements()[1],
        )
        formula_star = translate_formula_lj_to_ill(formula)
        return ill.with_left_1(premise, formula_star)

    elif rule_name == "∨-R":
        premise = lj_to_ill_proof(premises[0])
        formula = conclusion.succedent_formula
        formula_star = translate_formula_lj_to_ill(formula)
        if formula_star.left == translate_formula_lj_to_ill(
            premises[0].conclusion.succedent_formula
        ):
            return ill.plus_right_1(premise, formula_star)
        else:
            return ill.plus_right_2(premise, formula_star)

    elif rule_name == "∨-L":
        left_premise = lj_to_ill_proof(premises[0])
        right_premise = lj_to_ill_proof(premises[1])
        formula = Or(
            premises[0].conclusion.antecedent.elements()[1],
            premises[1].conclusion.antecedent.elements()[1],
        )
        formula_star = translate_formula_lj_to_ill(formula)
        return ill.plus_left(left_premise, right_premise, formula_star)

    elif rule_name == "→-R":
        premise = lj_to_ill_proof(premises[0])
        implication = conclusion.succedent_formula
        implication_star = translate_formula_lj_to_ill(implication)
        proof = ill.lin_implies_right(premise, implication_star.operand)
        return ill.of_course_right(proof)

    elif rule_name == "→-L":
        left_premise = lj_to_ill_proof(premises[0])
        right_premise = lj_to_ill_proof(premises[1])

        implication = [f for f in conclusion.antecedent if isinstance(f, Implies)][0]
        implication_star = translate_formula_lj_to_ill(implication)

        goal_succedent = right_premise.conclusion.succedent_formula
        goal_antecedent = (
            left_premise.conclusion.antecedent
            + (
                right_premise.conclusion.antecedent
                - Counter([translate_formula_lj_to_ill(implication.right)])
            )
            + Counter([implication_star])
        )
        goal = ill.ILLSequent(goal_antecedent, goal_succedent)

        # Use the synthesizer to find the proof
        return ill_synthesizer.synthesize(goal)

    elif rule_name == "¬-L":
        premise = lj_to_ill_proof(premises[0])
        return ProofTree(
            conclusion=ill.ILLSequent(
                premise.conclusion.antecedent, OfCourse(Prop("⊥"))
            ),
            rule=Rule("¬-L (Translated)"),
            premises=[premise],
        )

    elif rule_name == "¬-R":
        premise = lj_to_ill_proof(premises[0])
        formula = conclusion.succedent_formula
        formula_star = translate_formula_lj_to_ill(formula)
        proof = ill.lin_implies_right(premise, formula_star.operand)
        return ill.of_course_right(proof)

    else:
        raise NotImplementedError(
            f"Translation for rule '{rule_name}' is not yet implemented."
        )


def ill_to_ll(ill_proof: ProofTree) -> ProofTree:
    """
    Translates a proof from the ILL calculus to the LL calculus.
    This is a direct embedding, as any valid ILL proof is also a valid LL proof.
    """
    translated_premises = [ill_to_ll(p) for p in ill_proof.premises]

    return ProofTree(
        conclusion=lk.Sequent(
            ill_proof.conclusion.antecedent, ill_proof.conclusion.succedent
        ),
        rule=ill_proof.rule,
        premises=translated_premises,
    )
