import unittest
from tooling.hdl_parser import parse_sequent
from logic_system.src.formulas import Prop, LinImplies, Tensor
from collections import Counter


class TestHDLParser(unittest.TestCase):
    def test_parse_sequent_simple(self):
        s = "A |- B"
        sequent = parse_sequent(s)
        self.assertEqual(sequent.antecedent, Counter({Prop("A"): 1}))
        self.assertEqual(sequent.succedent, Counter({Prop("B"): 1}))

    def test_parse_sequent_with_implication(self):
        s = "A, A -> B |- B"
        sequent = parse_sequent(s)
        self.assertEqual(
            sequent.antecedent,
            Counter({Prop("A"): 1, LinImplies(Prop("A"), Prop("B")): 1}),
        )
        self.assertEqual(sequent.succedent, Counter({Prop("B"): 1}))

    def test_parse_sequent_with_tensor(self):
        s = "A * B |- C"
        sequent = parse_sequent(s)
        self.assertEqual(sequent.antecedent, Counter({Tensor(Prop("A"), Prop("B")): 1}))
        self.assertEqual(sequent.succedent, Counter({Prop("C"): 1}))


if __name__ == "__main__":
    unittest.main()
