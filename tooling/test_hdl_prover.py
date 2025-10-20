import unittest
from unittest.mock import patch
from collections import Counter
from tooling.hdl_prover import (
    parse_formula,
    parse_sequent,
    prove_sequent,
    main as hdl_main,
)
from logic_system.src.formulas import Prop, LinImplies, Tensor
from logic_system.src.sequents import Sequent


class TestHdlProver(unittest.TestCase):

    def test_parse_formula(self):
        """Tests the formula parser."""
        self.assertEqual(parse_formula("A"), Prop("A"))
        self.assertEqual(parse_formula("A -> B"), LinImplies(Prop("A"), Prop("B")))
        self.assertEqual(parse_formula("A * B"), Tensor(Prop("A"), Prop("B")))
        self.assertEqual(
            parse_formula("A -> B * C"),
            LinImplies(Prop("A"), Tensor(Prop("B"), Prop("C"))),
        )

    def test_parse_sequent(self):
        """Tests the sequent parser."""
        sequent = parse_sequent("A, A -> B |- B")
        expected_antecedent = Counter(
            {Prop("A"): 1, LinImplies(Prop("A"), Prop("B")): 1}
        )
        self.assertEqual(sequent.antecedent, expected_antecedent)
        self.assertEqual(sequent.succedent, Counter({Prop("B"): 1}))

    def test_prove_provable_sequent(self):
        """Tests a known provable sequent."""
        sequent = Sequent({Prop("A"), LinImplies(Prop("A"), Prop("B"))}, {Prop("B")})
        self.assertTrue(prove_sequent(sequent))

    def test_prove_unprovable_sequent(self):
        """Tests a known unprovable sequent."""
        sequent = Sequent({Prop("A")}, {Prop("B")})
        self.assertFalse(prove_sequent(sequent))

    @patch("sys.argv", ["tooling/hdl_prover.py", "A, A -> B |- B"])
    def test_main_provable(self):
        """Tests the main function with a provable sequent."""
        self.assertTrue(hdl_main())

    @patch("sys.argv", ["tooling/hdl_prover.py", "A |- B"])
    def test_main_unprovable(self):
        """Tests the main function with an unprovable sequent."""
        self.assertFalse(hdl_main())

    @patch("sys.argv", ["tooling/hdl_prover.py", "invalid-sequent"])
    def test_main_invalid_sequent(self):
        """Tests that the main function exits on a parsing error."""
        with self.assertRaises(SystemExit):
            hdl_main()


if __name__ == "__main__":
    unittest.main()
