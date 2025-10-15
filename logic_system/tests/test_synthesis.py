import unittest
from collections import Counter
from logic_system.src.formulas import Prop, LinImplies, OfCourse
from logic_system.src.sequents import Sequent
from logic_system.src.ill import ILLSequent
from logic_system.src.synthesizer import Synthesizer

class TestSynthesis(unittest.TestCase):

    def setUp(self):
        self.synthesizer = Synthesizer()

    def test_axiom_synthesis(self):
        """Tests that the synthesizer can find a simple axiom proof."""
        A = Prop("A")
        goal = ILLSequent([A], A)
        proof = self.synthesizer.synthesize(goal)
        self.assertEqual(proof.conclusion, goal)
        self.assertEqual(proof.rule.name, "Axiom")

    def test_lin_implies_right_synthesis(self):
        """Tests synthesis of a proof for Γ ⊢ A ⊸ B."""
        A = Prop("A")
        B = Prop("B")
        goal = ILLSequent([], LinImplies(A, B))

        # This will fail because the synthesizer needs to be able to handle context changes
        with self.assertRaises(ValueError):
            self.synthesizer.synthesize(goal)

    def test_dereliction_synthesis(self):
        """Tests synthesis of a proof involving dereliction."""
        A = Prop("A")
        B = Prop("B")
        goal = ILLSequent([OfCourse(A)], B)

        # This will fail as the synthesizer needs to know that A ⊢ B is provable
        with self.assertRaises(ValueError):
            self.synthesizer.synthesize(goal)

if __name__ == '__main__':
    unittest.main()