import unittest
import os
import shutil
from tooling.placeholder_manager import scan_for_placeholders, validate_placeholders

class TestPlaceholderManager(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory with various files for testing."""
        self.test_dir = "temp_placeholder_test"
        os.makedirs(self.test_dir, exist_ok=True)

        # File with valid placeholders
        with open(os.path.join(self.test_dir, "valid_file.py"), "w") as f:
            f.write("# This is a test file\n")
            f.write("def my_func():\n")
            f.write("    # TODO[task-123]: Implement the core logic here.\n")
            f.write("    pass # Another comment TODO[tech-debt]: Refactor this later.\n")

        # File with invalid placeholders
        with open(os.path.join(self.test_dir, "invalid_file.js"), "w") as f:
            f.write("// A simple JS file\n")
            f.write("function oldStyle() {\n")
            f.write("    // TODO: This needs to be fixed.\n")
            f.write("}\n")
            f.write("// another todo without brackets\n")

        # File with a mix of valid and invalid
        with open(os.path.join(self.test_dir, "mixed_file.txt"), "w") as f:
            f.write("This file has a TODO[task-456]: A valid one.\n")
            f.write("And also a simple, old TODO that is not compliant.\n")

        # Create an ignored directory with a file containing a TODO
        self.ignored_dir = os.path.join(self.test_dir, "__pycache__")
        os.makedirs(self.ignored_dir, exist_ok=True)
        with open(os.path.join(self.ignored_dir, "cached.py"), "w") as f:
            f.write("# TODO[should-be-ignored]: This should not be found.")

    def tearDown(self):
        """Clean up the temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_scan_for_placeholders(self):
        """Test that the scan command finds only valid, structured placeholders."""
        placeholders = scan_for_placeholders(self.test_dir)

        self.assertEqual(len(placeholders), 3, "Should find exactly three valid placeholders.")

        task_ids = {p['task_id'] for p in placeholders}
        self.assertEqual(task_ids, {'task-123', 'tech-debt', 'task-456'})

        # Check one placeholder in detail
        p1 = next(p for p in placeholders if p['task_id'] == 'task-123')
        self.assertEqual(p1['file'], os.path.join(self.test_dir, 'valid_file.py'))
        self.assertEqual(p1['line'], 3)
        self.assertEqual(p1['description'], "Implement the core logic here.")

    def test_validate_placeholders(self):
        """Test that the validate command finds all non-compliant TODOs."""
        non_compliant = validate_placeholders(self.test_dir)

        self.assertEqual(len(non_compliant), 3, "Should find exactly three non-compliant TODOs.")

        contents = {nc['content'] for nc in non_compliant}
        self.assertIn("// TODO: This needs to be fixed.", contents)
        self.assertIn("// another todo without brackets", contents)
        self.assertIn("And also a simple, old TODO that is not compliant.", contents)

        # Check that ignored directories are actually ignored
        for nc in non_compliant:
            self.assertNotIn("__pycache__", nc['file'])

if __name__ == '__main__':
    unittest.main()