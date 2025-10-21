import unittest
import os
import subprocess
import shutil


class TestGuardian(unittest.TestCase):
    def setUp(self):
        os.makedirs("reviews", exist_ok=True)

    def tearDown(self):
        if os.path.exists("reviews"):
            shutil.rmtree("reviews")

    def test_valid_review_document(self):
        with open("reviews/test.md", "w") as f:
            f.write("# Summary\n\n# Impact Analysis\n\n# Verification Plan\n")
        result = subprocess.run(
            ["python3", "tooling/guardian.py", "reviews/test.md"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Review document is valid.", result.stdout)

    def test_missing_section(self):
        with open("reviews/test.md", "w") as f:
            f.write("# Summary\n\n# Impact Analysis\n")
        result = subprocess.run(
            ["python3", "tooling/guardian.py", "reviews/test.md"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "Error: Missing required section 'Verification Plan'", result.stdout
        )

    def test_wrong_file_type(self):
        with open("reviews/test.txt", "w") as f:
            f.write("# Summary\n\n# Impact Analysis\n\n# Verification Plan\n")
        result = subprocess.run(
            ["python3", "tooling/guardian.py", "reviews/test.txt"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: Review document must be a markdown file.", result.stdout)


if __name__ == "__main__":
    unittest.main()
