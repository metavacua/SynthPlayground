import unittest
import sys
from pathlib import Path

# Add the parent directory to the path to allow imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.tooling.hdl_prover import main as hdl_prover_main
from unittest.mock import patch

class TestHdlProver(unittest.TestCase):

    @patch('sys.argv', ['src/tooling/hdl_prover.py', 'A |- A'])
    def test_provable_axiom(self):
        self.assertEqual(hdl_prover_main(), "Provable")

    @patch('sys.argv', ['src/tooling/hdl_prover.py', 'A, A -> B |- B'])
    def test_provable_modus_ponens(self):
        self.assertEqual(hdl_prover_main(), "Provable")

    @patch('sys.argv', ['src/tooling/hdl_prover.py', 'A |- B'])
    def test_unprovable(self):
        self.assertEqual(hdl_prover_main(), "Not provable")

if __name__ == '__main__':
    unittest.main()