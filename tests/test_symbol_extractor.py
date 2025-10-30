import os
import json
import unittest
import shutil
import tempfile
from tooling.symbol_extractor import main as symbol_extractor_main
from tooling.ast_generator import generate_asts_for_repo

class TestSymbolExtractor(unittest.TestCase):

    def setUp(self):
        self.test_repo_dir = tempfile.mkdtemp()
        self.asts_dir = os.path.join(self.test_repo_dir, 'knowledge_core', 'asts')
        self.output_file = os.path.join(self.test_repo_dir, 'knowledge_core', 'symbol_map.json')
        os.makedirs(self.asts_dir, exist_ok=True)
        self.sample_file = os.path.join(self.test_repo_dir, 'sample.py')
        with open(self.sample_file, 'w') as f:
            f.write("""def hello():
    print("Hello, World!")

class MyClass:
    pass
""")
        generate_asts_for_repo(root_dir=self.test_repo_dir, output_dir=self.asts_dir)

    def tearDown(self):
        shutil.rmtree(self.test_repo_dir)

    def test_symbol_extraction(self):
        import sys
        original_argv = sys.argv
        sys.argv = ['tooling/symbol_extractor.py', '--asts-dir', self.asts_dir, '--output-file', self.output_file]

        symbol_extractor_main()

        sys.argv = original_argv

        with open(self.output_file, 'r') as f:
            symbol_map = json.load(f)

        self.assertIn('hello', symbol_map)
        self.assertEqual(len(symbol_map['hello']), 1)
        self.assertEqual(symbol_map['hello'][0]['type'], 'function_definition')

        self.assertIn('MyClass', symbol_map)
        self.assertEqual(len(symbol_map['MyClass']), 1)
        self.assertEqual(symbol_map['MyClass'][0]['type'], 'class_definition')

if __name__ == '__main__':
    unittest.main()
