import os
import json
import unittest
import shutil
import tempfile
from tooling.ast_generator import generate_asts_for_repo

class TestAstGenerator(unittest.TestCase):

    def setUp(self):
        self.test_repo_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_repo_dir, 'knowledge_core', 'asts')
        os.makedirs(self.output_dir, exist_ok=True)
        with open(os.path.join(self.test_repo_dir, 'sample.py'), 'w') as f:
            f.write('def hello():\\n    print("Hello, World!")')

    def tearDown(self):
        shutil.rmtree(self.test_repo_dir)
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_ast_generation(self):
        generate_asts_for_repo(root_dir=self.test_repo_dir, output_dir=self.output_dir)
        expected_ast_path = os.path.join(self.output_dir, 'sample.py.json')
        self.assertTrue(os.path.exists(expected_ast_path))
        with open(expected_ast_path, 'r') as f:
            ast_data = json.load(f)
        self.assertEqual(ast_data['type'], 'module')

if __name__ == '__main__':
    unittest.main()
