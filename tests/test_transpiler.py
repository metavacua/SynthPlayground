import unittest
import os
import shutil
from toolchain.plang_transpiler import transpile_plang, PLangSyntaxError


class TestPLangTranspiler(unittest.TestCase):

    TEST_DIR = "test_transpiler_workspace"

    def setUp(self):
        """Create a temporary directory for test files."""
        os.makedirs(self.TEST_DIR, exist_ok=True)

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.TEST_DIR)

    def test_transpile_success(self):
        """Test a successful transpilation of a valid .plang file."""
        source_path = os.path.join(self.TEST_DIR, "valid.plang")
        output_path = os.path.join(self.TEST_DIR, "valid.py")

        plang_code = """
dialetheia config:
    "StanceA": {"value": 1},
    "StanceB": {"value": 2}

x = resolve config with "StanceA"
"""
        with open(source_path, "w") as f:
            f.write(plang_code)

        transpile_plang(source_path, output_path)

        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r") as f:
            transpiled_code = f.read()

            # Check that the transpiled code is what we expect
            self.assertIn(
                "config = {'StanceA': {'value': 1}, 'StanceB': {'value': 2}}",
                transpiled_code,
            )
            self.assertIn("x = config['StanceA']", transpiled_code)

    def test_transpile_invalid_syntax_in_block(self):
        """Test that the transpiler raises an error for invalid syntax inside a dialetheia block."""
        source_path = os.path.join(self.TEST_DIR, "invalid_syntax.plang")
        output_path = os.path.join(self.TEST_DIR, "invalid_syntax.py")

        # Missing comma between dictionary items
        plang_code = """
dialetheia config:
    "StanceA": {"value": 1}
    "StanceB": {"value": 2}
"""
        with open(source_path, "w") as f:
            f.write(plang_code)

        with self.assertRaises(PLangSyntaxError):
            transpile_plang(source_path, output_path)

    def test_transpile_unquoted_key(self):
        """Test that the transpiler raises an error for unquoted keys, as per the spec."""
        source_path = os.path.join(self.TEST_DIR, "unquoted_key.plang")
        output_path = os.path.join(self.TEST_DIR, "unquoted_key.py")

        plang_code = """
dialetheia config:
    StanceA: {"value": 1},
    "StanceB": {"value": 2}
"""
        with open(source_path, "w") as f:
            f.write(plang_code)

        with self.assertRaises(PLangSyntaxError):
            transpile_plang(source_path, output_path)


if __name__ == "__main__":
    unittest.main()
