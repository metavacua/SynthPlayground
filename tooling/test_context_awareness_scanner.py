import unittest
import os
from tooling.context_awareness_scanner_logic import analyze_python_file

class TestContextAwarenessScanner(unittest.TestCase):
    def test_analyze_python_file(self):
        content = """
import os
import sys

class MyClass:
    def my_method(self):
        pass

def my_function():
    pass
"""
        defined_symbols, imported_symbols = analyze_python_file(content)
        self.assertEqual(len(defined_symbols), 3)
        self.assertEqual(len(imported_symbols), 2)

        # The order of defined_symbols is not guaranteed, so we check for the presence of each symbol.
        symbol_names = {s["name"] for s in defined_symbols}
        self.assertIn("MyClass", symbol_names)
        self.assertIn("my_method", symbol_names)
        self.assertIn("my_function", symbol_names)

        import_names = {s["name"] for s in imported_symbols}
        self.assertIn("os", import_names)
        self.assertIn("sys", import_names)

if __name__ == '__main__':
    unittest.main()
