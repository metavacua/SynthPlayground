import os
import unittest
import shutil
import sys
from tooling.refactor import main as refactor_main
from tooling.ast_generator import generate_asts_for_repo

class TestRefactor(unittest.TestCase):

    def setUp(self):
        self.test_repo_dir = 'test_repo'
        self.output_dir = os.path.join(self.test_repo_dir, 'knowledge_core', 'asts')
        os.makedirs(self.output_dir, exist_ok=True)
        self.sample_file = os.path.join(self.test_repo_dir, 'sample.py')
        with open(self.sample_file, 'w') as f:
            f.write('def hello():\\n    print("Hello, World!")\\n\\nhello_world = hello\\n')
        generate_asts_for_repo(root_dir=self.test_repo_dir, output_dir=self.output_dir)

    def tearDown(self):
        shutil.rmtree(self.test_repo_dir)

    def test_refactor(self):
        original_argv = sys.argv
        sys.argv = ['tooling/refactor.py', '--old-name', 'hello', '--new-name', 'greet', '--search-path', self.test_repo_dir, '--root-dir', self.test_repo_dir]

        refactor_main()

        sys.argv = original_argv

        with open(self.sample_file, 'r') as f:
            content = f.read()

        self.assertIn('def greet():', content)
        self.assertIn('hello_world = greet', content)
        self.assertNotIn('def hello():', content)
        self.assertNotIn('hello_world = hello', content)

if __name__ == '__main__':
    unittest.main()
