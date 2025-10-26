import unittest
import os
import shutil
from tooling import refactor_cs_to_cf

class TestRefactorCsToCf(unittest.TestCase):

    def setUp(self):
        # Create a dummy test file
        self.test_file = "test_file.py"
        with open(self.test_file, "w") as f:
            f.write("""
import os
import sys

def pure_function(x, y):
    return x + y

def impure_function(path):
    with open(path, "r") as f:
        return f.read()
""")

    def tearDown(self):
        # Clean up the dummy test file and the generated logic file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("test_file_logic.py"):
            os.remove("test_file_logic.py")

    def test_refactor(self):
        # Run the refactoring tool on the test file
        refactor_cs_to_cf.main(["test_file.py"])

        # Check that the logic file was created
        self.assertTrue(os.path.exists("test_file_logic.py"))

        # Check the contents of the logic file
        with open("test_file_logic.py", "r") as f:
            content = f.read()
            self.assertIn("def pure_function(x, y):", content)
            self.assertNotIn("def impure_function(path):", content)

        # Check the contents of the original file
        with open("test_file.py", "r") as f:
            content = f.read()
            self.assertIn("from test_file_logic import pure_function", content)
            self.assertNotIn("def pure_function(x, y):", content)
            self.assertIn("def impure_function(path):", content)

if __name__ == '__main__':
    unittest.main()
