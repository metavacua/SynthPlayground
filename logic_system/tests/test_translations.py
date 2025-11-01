import unittest
from collections import Counter
from logic_system.src.formulas import Prop, Implies, And, Or, Not, OfCourse, LinImplies, With, Plus
from logic_system.src.sequents import Sequent
from logic_system.src.ill import contraction as ill_contraction, ILLSequent
from logic_system.src import lj
from logic_system.src.translations import lj_to_lk, translate_formula_lj_to_ill, lj_to_ill_proof
from logic_system.src.proof import ProofTree, Rule

class TestTranslations(unittest.TestCase):

    def test_lj_to_lk_translation(self):
        """
        Tests the direct embedding translation from LJ to LK.
        """
        # 1. Construct a simple LJ proof for ⊢ A → A
        A = Prop("A")
        axiom_proof = lj.axiom(A) # A ⊢ A
        lj_proof = lj.implies_right(axiom_proof, Implies(A, A)) # ⊢ A → A

        # 2. Translate the LJ proof to LK
        lk_proof = lj_to_lk(lj_proof)

        # 3. Assert correctness
        self.assertIsInstance(lk_proof.conclusion, Sequent)
        self.assertEqual(lk_proof.conclusion.antecedent, Counter())
        self.assertEqual(lk_proof.conclusion.succedent, Counter([Implies(A, A)]))
        self.assertEqual(lk_proof.rule.name, "→-R")
        self.assertEqual(len(lk_proof.premises), 1)
        self.assertEqual(lk_proof.premises[0].conclusion.antecedent, Counter([A]))
        self.assertEqual(lk_proof.premises[0].conclusion.succedent, Counter([A]))
        self.assertEqual(lk_proof.premises[0].rule.name, "Axiom")

    def test_lj_to_ill_formula_translation(self):
        """
        Tests the formula translation from LJ to ILL.
        """
        A = Prop("A")
        B = Prop("B")
        bottom = Prop("⊥")

        # Test atoms
        self.assertEqual(translate_formula_lj_to_ill(A), A)

        # Test conjunction
        formula_and = And(A, B)
        translated_and = translate_formula_lj_to_ill(formula_and)
        self.assertEqual(translated_and, With(A, B))

        # Test disjunction
        formula_or = Or(A, B)
        translated_or = translate_formula_lj_to_ill(formula_or)
        self.assertEqual(translated_or, Plus(OfCourse(A), OfCourse(B)))

        # Test implication
        formula_imp = Implies(A, B)
        translated_imp = translate_formula_lj_to_ill(formula_imp)
        self.assertEqual(translated_imp, OfCourse(LinImplies(OfCourse(A), OfCourse(B))))

        # Test negation
        formula_not = Not(A)
        translated_not = translate_formula_lj_to_ill(formula_not)
        self.assertEqual(translated_not, OfCourse(LinImplies(OfCourse(A), OfCourse(bottom))))

    def test_ill_contraction(self):
        """
        Tests the contraction rule in Intuitionistic Linear Logic.
        """
        A = Prop("A")
        B = Prop("B")
        of_course_A = OfCourse(A)

        # Create a premise Γ, !A, !A ⊢ B
        antecedent = Counter([of_course_A, of_course_A, B])
        succedent = B
        premise_sequent = ILLSequent(antecedent, succedent)
        premise_proof = ProofTree(premise_sequent, Rule("Premise"))

        # Apply contraction: Γ, !A, !A ⊢ B  /  Γ, !A ⊢ B
        contracted_proof = ill_contraction(premise_proof, of_course_A)

        # Assert the new antecedent is correct
        expected_antecedent = Counter([of_course_A, B])
        self.assertEqual(contracted_proof.conclusion.antecedent, expected_antecedent)
        self.assertEqual(contracted_proof.conclusion.succedent_formula, B)

    def test_lj_axiom_to_ill_proof_translation(self):
        """
        Tests the translation of a simple LJ axiom proof to ILL.
        """
        # 1. Construct LJ proof for A ⊢ A
        A = Prop("A")
        lj_proof = lj.axiom(A)

        # 2. Translate to ILL
        ill_proof = lj_to_ill_proof(lj_proof)

        # 3. Assert correctness: !A* ⊢ A*
        A_star = OfCourse(translate_formula_lj_to_ill(A))

        # The result should be !A* ⊢ A* which comes from dereliction on A* ⊢ A*
        self.assertIsInstance(ill_proof.conclusion, ILLSequent)
        self.assertEqual(ill_proof.conclusion.antecedent, Counter([A_star]))
        self.assertEqual(ill_proof.conclusion.succedent_formula, A_star.operand)
        self.assertEqual(ill_proof.rule.name, "Dereliction")
        self.assertEqual(len(ill_proof.premises), 1)
        self.assertEqual(ill_proof.premises[0].rule.name, "Axiom")

    def test_lj_implies_left_to_ill(self):
        """Tests the translation of an LJ proof with →-L."""
        A = Prop("A")
        B = Prop("B")

        # Construct LJ proof for A, A → B ⊢ B
        p1 = lj.axiom(A) # A ⊢ A
        p2 = lj.axiom(B) # B ⊢ B
        p3 = lj.implies_left(p1, p2, Implies(A, B)) # A, A → B ⊢ B

        # Translate to ILL
        ill_proof = lj_to_ill_proof(p3)

        # We expect a valid proof, even if it's complex
        self.assertIsInstance(ill_proof, ProofTree)


if __name__ == '__main__':
    unittest.main()