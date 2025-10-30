import unittest
import os
import sys
import json
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tooling.symbol_extractor import SymbolExtractor

class TestSymbolExtractor(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'tests/fixtures/symbol_extractor'
        self.ast_dir = os.path.join(self.test_dir, 'asts')
        self.symbol_map_file = os.path.join(self.test_dir, 'symbol_map.json')
        os.makedirs(self.ast_dir, exist_ok=True)

        # Create a dummy AST file for testing
        self.dummy_ast_content = {
            "type": "module",
            "children": [
                {
                    "type": "function_definition",
                    "field": "body",
                    "children": [
                        {"type": "def", "text": "def"},
                        {"type": "identifier", "field": "name", "text": "my_function"},
                        {"type": "parameters", "text": "()"},
                        {"type": ":", "text": ":"},
                        {"type": "block", "children": [{"type": "pass"}]}
                    ]
                }
            ]
        }
        with open(os.path.join(self.ast_dir, 'dummy_file.py.json'), 'w') as f:
            json.dump(self.dummy_ast_content, f)

        self.extractor = SymbolExtractor(ast_dir=self.ast_dir, symbol_map_file=self.symbol_map_file)
        self.extractor.generate_symbol_map()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_symbols_from_file(self):
        symbols = self.extractor.get_symbols_from_file('dummy_file.py')
        self.assertEqual(len(symbols), 1)
        self.assertEqual(symbols[0]['name'], 'my_function')
        self.assertEqual(symbols[0]['type'], 'function_definition')

    def test_find_all_references(self):
        references = self.extractor.find_all_references('my_function')
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0]['filepath'], 'dummy_file.py')
        self.assertEqual(references[0]['type'], 'function_definition')

if __name__ == '__main__':
    unittest.main()
