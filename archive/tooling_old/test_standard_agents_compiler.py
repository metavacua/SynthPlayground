import unittest
import os
import shutil
from unittest.mock import patch
from tooling.standard_agents_compiler import parse_makefile_command, main as compiler_main

class TestStandardAgentsCompiler(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_std_agents_compiler_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.makefile_path = os.path.join(self.test_dir, "Makefile")
        self.target_file = os.path.join(self.test_dir, "AGENTS.standard.md")

        self.makefile_content = """
install:
	pip install -r requirements.txt

test:
	@echo "Running tests..."
	python -m unittest discover

lint:
	flake8 .

format:
	black .
"""
        with open(self.makefile_path, "w") as f:
            f.write(self.makefile_content)

        # Patch the paths to use our temporary files
        patch('tooling.standard_agents_compiler.MAKEFILE_PATH', self.makefile_path).start()
        patch('tooling.standard_agents_compiler.TARGET_FILE', self.target_file).start()
        self.addCleanup(patch.stopall)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_makefile_command(self):
        """Tests parsing commands from the Makefile content."""
        self.assertEqual(parse_makefile_command("install", self.makefile_content), "pip install -r requirements.txt")
        self.assertEqual(parse_makefile_command("test", self.makefile_content), "python -m unittest discover")
        self.assertEqual(parse_makefile_command("lint", self.makefile_content), "flake8 .")
        self.assertEqual(parse_makefile_command("non_existent", self.makefile_content), "make non_existent")

    def test_main_generates_correct_file(self):
        """Tests that the main function generates the AGENTS.standard.md correctly."""
        compiler_main()

        self.assertTrue(os.path.exists(self.target_file))
        with open(self.target_file, "r") as f:
            content = f.read()

        self.assertIn("pip install -r requirements.txt", content)
        self.assertIn("python -m unittest discover", content)
        self.assertIn("flake8 .", content)
        self.assertIn("black .", content)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_makefile_not_found(self, mock_open):
        """Tests that the script handles a missing Makefile."""
        # The main function should catch the error and print a message, not raise the error.
        # We can't easily test the print statement without more complex mocking,
        # so we just ensure it doesn't crash.
        try:
            compiler_main()
        except Exception as e:
            self.fail(f"compiler_main() raised an exception unexpectedly: {e}")

if __name__ == "__main__":
    unittest.main()