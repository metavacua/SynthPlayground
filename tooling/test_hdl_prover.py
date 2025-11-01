import unittest
from tooling.hdl_parser import parse_sequent
from tooling.hdl_prover import prove_sequent


class TestHDLProver(unittest.TestCase):
    def test_prove_sequent_axiom(self):
        s = "A |- A"
        sequent = parse_sequent(s)
        self.assertTrue(prove_sequent(sequent))

    def test_prove_sequent_implication(self):
        s = "A, A -> B |- B"
        sequent = parse_sequent(s)
        self.assertTrue(prove_sequent(sequent))

    def test_prove_sequent_fail(self):
        s = "A |- B"
        sequent = parse_sequent(s)
        self.assertFalse(prove_sequent(sequent))


if __name__ == "__main__":
    unittest.main()
