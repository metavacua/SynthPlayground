import unittest
import os
import json
import ast
from unittest.mock import patch, MagicMock

# Import the functions to be tested
from tooling.symbol_map_generator import generate_symbol_map, is_ctags_available, generate_symbols_with_ctags, generate_symbols_with_ast

class TestSymbolMapGenerator(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.output_dir = "knowledge_core"
        self.output_file = os.path.join(self.output_dir, "symbols.json")

        # Create a dummy file to be scanned by the AST parser
        self.test_py_file_path = "test_temp_file.py"
        with open(self.test_py_file_path, "w") as f:
            f.write("def sample_function():\n    pass\n\nclass SampleClass:\n    pass\n")

        # Clean up any old output files
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.test_py_file_path):
            os.remove(self.test_py_file_path)

    @patch('shutil.which', return_value='/usr/bin/ctags')
    @patch('subprocess.run')
    def test_ctags_availability(self, mock_run, mock_which):
        """Tests that the script correctly identifies when ctags is available."""
        mock_run.return_value = MagicMock(stdout="Universal Ctags", returncode=0)
        self.assertTrue(is_ctags_available())

    @patch('shutil.which', return_value=None)
    def test_ctags_unavailability(self, mock_which):
        """Tests that the script correctly identifies when ctags is not available."""
        self.assertFalse(is_ctags_available())

    @patch('tooling.symbol_map_generator.is_ctags_available', return_value=True)
    @patch('tooling.symbol_map_generator.generate_symbols_with_ctags', return_value=True)
    def test_main_function_uses_ctags_when_available(self, mock_gen_ctags, mock_is_available):
        """Ensures the main function calls the ctags generator when available."""
        generate_symbol_map()
        mock_gen_ctags.assert_called_once()

    @patch('tooling.symbol_map_generator.is_ctags_available', return_value=False)
    @patch('tooling.symbol_map_generator.generate_symbols_with_ast', return_value=True)
    def test_main_function_falls_back_to_ast_when_ctags_unavailable(self, mock_gen_ast, mock_is_available):
        """Ensures the main function falls back to the AST generator."""
        generate_symbol_map()
        mock_gen_ast.assert_called_once()

    @patch('tooling.symbol_map_generator.SCAN_DIRECTORIES', new=["."])
    def test_ast_symbol_generation(self):
        """Tests the AST-based symbol generation with a known temporary file."""
        # Override the scan directories to only include the current dir where the temp file is
        with patch('tooling.symbol_map_generator.SCAN_DIRECTORIES', [os.path.dirname(self.test_py_file_path)]):
             # To avoid scanning other files, we will create a temp dir
            temp_dir = "temp_test_dir_for_ast"
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.join(temp_dir, "test_file.py")
            with open(temp_file_path, "w") as f:
                f.write("def my_func(): pass\nclass MyClass: pass")

            with patch('tooling.symbol_map_generator.SCAN_DIRECTORIES', [temp_dir]):
                generate_symbols_with_ast()

            self.assertTrue(os.path.exists(self.output_file))

            with open(self.output_file, 'r') as f:
                data = json.load(f)

            symbol_names = {item['name'] for item in data}
            self.assertIn("my_func", symbol_names)
            self.assertIn("MyClass", symbol_names)
            self.assertEqual(len(data), 2)

            # Cleanup
            os.remove(temp_file_path)
            os.rmdir(temp_dir)

if __name__ == "__main__":
    unittest.main()