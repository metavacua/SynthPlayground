from . import ill
from .proof import ProofTree, Rule
from .sequents import Sequent
from .formulas import Formula, LinImplies, OfCourse, With, Plus, Tensor
from collections import Counter
from itertools import combinations

class Synthesizer:
    def __init__(self, logic_module=ill):
        self.logic = logic_module

    def _get_partitions(self, multiset):
        """Generator for all 2-partitions of a multiset."""
        elements = list(multiset.elements())
        for i in range(len(elements) // 2 + 1):
            for combo1 in combinations(elements, i):
                c1 = Counter(combo1)
                c2 = multiset - c1
                yield c1, c2

    def synthesize(self, goal: Sequent, max_depth=10, visited=None) -> ProofTree:
        if visited is None:
            visited = set()

        if goal in visited:
            raise RecursionError("Already visited this goal")

        visited.add(goal)

        if max_depth <= 0:
            raise RecursionError("Max depth reached during synthesis")

        # --- Axiom Rule ---
        if len(goal.antecedent) == 1 and len(goal.succedent) == 1:
            ant = list(goal.antecedent.elements())[0]
            suc = list(goal.succedent.elements())[0]
            if ant == suc:
                return self.logic.axiom(ant)

        # --- Right Rules ---
        succedent_formula = goal.succedent_formula

        if isinstance(succedent_formula, LinImplies):
            formula = succedent_formula
            new_goal = self.logic.ILLSequent(goal.antecedent + Counter([formula.left]), formula.right)
            try:
                premise_proof = self.synthesize(new_goal, max_depth - 1, visited)
                return self.logic.lin_implies_right(premise_proof, formula)
            except (ValueError, RecursionError):
                pass

        if isinstance(succedent_formula, Tensor):
            formula = succedent_formula
            for ant_part1, ant_part2 in self._get_partitions(goal.antecedent):
                try:
                    goal1 = self.logic.ILLSequent(ant_part1, formula.left)
                    goal2 = self.logic.ILLSequent(ant_part2, formula.right)
                    premise1 = self.synthesize(goal1, max_depth - 1, visited)
                    premise2 = self.synthesize(goal2, max_depth - 1, visited)
                    return self.logic.tensor_right(premise1, premise2)
                except (ValueError, RecursionError):
                    continue

        if isinstance(succedent_formula, OfCourse):
            formula = succedent_formula
            if all(isinstance(f, OfCourse) for f in goal.antecedent):
                new_goal = self.logic.ILLSequent(goal.antecedent, formula.operand)
                try:
                    premise_proof = self.synthesize(new_goal, max_depth - 1, visited)
                    return self.logic.of_course_right(premise_proof)
                except (ValueError, RecursionError):
                    pass

        # --- Left Rules ---
        for ant_formula in list(goal.antecedent.elements()):
            if isinstance(ant_formula, OfCourse):
                # Dereliction
                new_antecedent = (goal.antecedent - Counter([ant_formula])) + Counter([ant_formula.operand])
                new_goal = self.logic.ILLSequent(new_antecedent, succedent_formula)
                try:
                    premise_proof = self.synthesize(new_goal, max_depth - 1, visited)
                    return self.logic.dereliction(premise_proof, ant_formula)
                except (ValueError, RecursionError):
                    pass

                # Contraction
                new_antecedent = goal.antecedent + Counter([ant_formula])
                new_goal = self.logic.ILLSequent(new_antecedent, succedent_formula)
                try:
                    premise_proof = self.synthesize(new_goal, max_depth - 1, visited)
                    return self.logic.contraction(premise_proof, ant_formula)
                except (ValueError, RecursionError):
                    pass

                # Weakening
                new_antecedent = goal.antecedent - Counter([ant_formula])
                new_goal = self.logic.ILLSequent(new_antecedent, succedent_formula)
                try:
                    premise_proof = self.synthesize(new_goal, max_depth - 1, visited)
                    return self.logic.weakening(premise_proof, ant_formula)
                except (ValueError, RecursionError):
                    pass


            if isinstance(ant_formula, LinImplies):
                formula = ant_formula
                remaining_antecedent = goal.antecedent - Counter([formula])
                for part1, part2 in self._get_partitions(remaining_antecedent):
                    try:
                        goal1 = self.logic.ILLSequent(part1, formula.left)
                        goal2 = self.logic.ILLSequent(part2 + Counter([formula.right]), succedent_formula)
                        premise1 = self.synthesize(goal1, max_depth - 1, visited)
                        premise2 = self.synthesize(goal2, max_depth - 1, visited)
                        return self.logic.lin_implies_left(premise1, premise2, formula)
                    except (ValueError, RecursionError):
                        continue

        raise ValueError(f"Could not synthesize a proof for goal: {goal}")