import unittest
import os
import shutil
import tempfile
from tooling.untested_code_detector import find_untested_code

class TestUntestedCodeDetector(unittest.TestCase):

    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.test_dir)

    def test_find_untested_code(self):
        with open(os.path.join(self.source_dir, "tested_file.py"), "w") as f:
            f.write("def foo(): pass")
        with open(os.path.join(self.test_dir, "test_tested_file.py"), "w") as f:
            f.write("import unittest")
        with open(os.path.join(self.source_dir, "untested_file.py"), "w") as f:
            f.write("def bar(): pass")

        untested_files, _, _ = find_untested_code(self.source_dir, self.test_dir)
        self.assertEqual(len(untested_files), 1)
        self.assertEqual(untested_files[0], os.path.join(self.source_dir, "untested_file.py"))

if __name__ == "__main__":
    unittest.main()
