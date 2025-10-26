import unittest
import os
import shutil
from tooling import refactor_cf_to_r

class TestRefactorCfToR(unittest.TestCase):

    def setUp(self):
        # Create a dummy test file
        self.test_file = "test_file.py"
        with open(self.test_file, "w") as f:
            f.write("""
import re

def lexer(text):
    pos = 0
    while pos < len(text):
        if text[pos].isspace():
            pos += 1
            continue
        elif m := re.match(r"[0-9]+", text[pos:]):
            yield "NUMBER", m.group(0)
            pos += m.end()
        elif m := re.match(r"[a-zA-Z]+", text[pos:]):
            yield "IDENTIFIER", m.group(0)
            pos += m.end()
        else:
            yield "UNKNOWN", text[pos]
            pos += 1

def not_a_lexer():
    return "This is not a lexer"
""")

    def tearDown(self):
        # Clean up the dummy test file and the generated lexer file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("test_file_lexer.py"):
            os.remove("test_file_lexer.py")

    def test_refactor(self):
        # Run the refactoring tool on the test file
        refactor_cf_to_r.main(["test_file.py"])

        # Check that the lexer file was created
        self.assertTrue(os.path.exists("test_file_lexer.py"))

        # Check the contents of the lexer file
        with open("test_file_lexer.py", "r") as f:
            content = f.read()
            self.assertIn("def lexer(text):", content)
            self.assertNotIn("def not_a_lexer():", content)

        # Check the contents of the original file
        with open("test_file.py", "r") as f:
            content = f.read()
            self.assertIn("from test_file_lexer import lexer", content)
            self.assertNotIn("def lexer(text):", content)
            self.assertIn("def not_a_lexer():", content)

if __name__ == '__main__':
    unittest.main()
