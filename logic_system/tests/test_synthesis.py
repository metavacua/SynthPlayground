import unittest
from collections import Counter
from logic_system.src.formulas import Prop, LinImplies, OfCourse, Tensor
from logic_system.src.ill import ILLSequent, axiom
from logic_system.src.synthesizer import Synthesizer
from logic_system.src.proof import ProofTree

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
        """Tests synthesis of a proof for A ⊢ B ⊸ (A ⊗ B)"""
        A = Prop("A")
        B = Prop("B")
        # Goal: A ⊢ B ⊸ (A ⊗ B)
        goal = ILLSequent([A], LinImplies(B, Tensor(A, B)))

        proof = self.synthesizer.synthesize(goal)
        self.assertEqual(proof.conclusion, goal)


    def test_dereliction_synthesis(self):
        """Tests synthesis of a proof involving dereliction."""
        A = Prop("A")
        goal = ILLSequent([OfCourse(A)], A)
        proof = self.synthesizer.synthesize(goal)
        self.assertEqual(proof.rule.name, "Dereliction")
        self.assertEqual(proof.premises[0].rule.name, "Axiom")

    def test_tensor_right_synthesis(self):
        """Tests a simple case of tensor right synthesis."""
        A = Prop("A")
        B = Prop("B")
        goal = ILLSequent([A, B], Tensor(A, B))
        proof = self.synthesizer.synthesize(goal)
        self.assertEqual(proof.rule.name, "⊗-R")
        self.assertEqual(proof.premises[0].conclusion, ILLSequent([A], A))
        self.assertEqual(proof.premises[1].conclusion, ILLSequent([B], B))


if __name__ == '__main__':
    unittest.main()