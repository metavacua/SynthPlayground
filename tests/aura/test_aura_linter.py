# tests/aura/test_aura_linter.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import unittest
from tooling.aura.aura_linter import lint_aura_files

class TestAuraLinter(unittest.TestCase):
    def test_lint_missing_semicolon(self):
        with self.assertRaises(SystemExit) as cm:
            lint_aura_files(["tests/aura/linter_test_cases/missing_semicolon.aura"])
        self.assertEqual(cm.exception.code, 1)

    def test_lint_invalid_token(self):
        with self.assertRaises(SystemExit) as cm:
            lint_aura_files(["tests/aura/linter_test_cases/invalid_token.aura"])
        self.assertEqual(cm.exception.code, 1)

    def test_lint_incomplete_statement(self):
        with self.assertRaises(SystemExit) as cm:
            lint_aura_files(["tests/aura/linter_test_cases/incomplete_statement.aura"])
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
