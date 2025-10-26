"""
Tests for the decidable refactoring tool.
"""

import unittest
import ast
from tooling.chomsky.refactor import CodeRefactorer

class TestCodeRefactorer(unittest.TestCase):

    def setUp(self):
        self.test_code = """
def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))
"""

    def test_refactor_to_decidable(self):
        refactorer = CodeRefactorer(self.test_code)
        new_source = refactorer.refactor_to_decidable()

        # Check that the new source code is what we expect
        expected_source = """def ackermann(m, n, fuel):
    if fuel == 0:
        return None
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1, fuel - 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1, fuel - 1), fuel - 1)"""

        # We'll compare the ASTs to avoid issues with formatting differences
        self.assertEqual(ast.dump(ast.parse(new_source)), ast.dump(ast.parse(expected_source)))

if __name__ == "__main__":
    unittest.main()
