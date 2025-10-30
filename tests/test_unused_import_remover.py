import os
import unittest
import shutil
import sys
import tempfile
from tooling.unused_import_remover import main as unused_import_remover_main

class TestUnusedImportRemover(unittest.TestCase):

    def setUp(self):
        self.test_repo_dir = tempfile.mkdtemp()
        self.sample_file = os.path.join(self.test_repo_dir, 'sample.py')
        with open(self.sample_file, 'w') as f:
            f.write("""import os, sys
from os import path, environ

def hello():
    print(sys.version)
""")

    def tearDown(self):
        shutil.rmtree(self.test_repo_dir)

    def test_remove_unused_imports(self):
        original_argv = sys.argv
        sys.argv = ['tooling/unused_import_remover.py', self.sample_file, '--fix']

        unused_import_remover_main()

        sys.argv = original_argv

        with open(self.sample_file, 'r') as f:
            content = f.read()

        self.assertNotIn('import os', content)
        self.assertIn('import sys', content)
        self.assertNotIn('from os import path', content)
        self.assertNotIn('from os import environ', content)

if __name__ == '__main__':
    unittest.main()
