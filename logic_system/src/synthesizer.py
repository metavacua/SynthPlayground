from . import ill
from .proof import ProofTree, Rule
from .sequents import Sequent
from .formulas import Formula, LinImplies, OfCourse, With, Plus, Tensor
from collections import Counter

class Synthesizer:
    def __init__(self, logic_module=ill):
        self.logic = logic_module

    def synthesize(self, goal: Sequent, max_depth=10) -> ProofTree:
        if max_depth <= 0:
            raise RecursionError("Max depth reached during synthesis")

        # --- Axiom Rule ---
        # A ⊢ A
        if len(goal.antecedent) == 1 and len(goal.succedent) == 1:
            ant = list(goal.antecedent.elements())[0]
            suc = list(goal.succedent.elements())[0]
            if ant == suc:
                return self.logic.axiom(ant)

        # --- Right Rules (deconstruct succedent) ---
        succedent_formula = goal.succedent_formula

        # ⊸-R
        if isinstance(succedent_formula, LinImplies):
            formula = succedent_formula
            new_goal = self.logic.ILLSequent(goal.antecedent + Counter([formula.left]), formula.right)
            try:
                premise_proof = self.synthesize(new_goal, max_depth - 1)
                return self.logic.lin_implies_right(premise_proof, formula)
            except (ValueError, RecursionError):
                pass

        # ⊗-R
        if isinstance(succedent_formula, Tensor):
            formula = succedent_formula
            # This rule is non-deterministic, we need to split the antecedent
            # This is a hard problem (partition problem). For now, we don't handle it.
            pass

        # --- Left Rules (deconstruct antecedent) ---
        for ant_formula in goal.antecedent:
            # !-L (Dereliction)
            if isinstance(ant_formula, OfCourse):
                new_antecedent = (goal.antecedent - Counter([ant_formula])) + Counter([ant_formula.operand])
                new_goal = self.logic.ILLSequent(new_antecedent, succedent_formula)
                try:
                    premise_proof = self.synthesize(new_goal, max_depth - 1)
                    return self.logic.dereliction(premise_proof, ant_formula)
                except (ValueError, RecursionError):
                    pass

            # ⊸-L
            if isinstance(ant_formula, LinImplies):
                # This requires two premises, one of which is to prove the LHS of the implication.
                # This also requires partitioning the context. Very complex.
                pass


        raise ValueError(f"Could not synthesize a proof for goal: {goal}")