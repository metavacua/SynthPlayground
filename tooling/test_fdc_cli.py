import unittest
import os
import tempfile
import subprocess
from unittest.mock import patch

class TestFdcCliLinter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.plan_file_path = os.path.join(self.temp_dir.name, "plan.txt")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _run_lint(self, plan_content):
        """Helper function to run the lint command on a given plan content."""
        with open(self.plan_file_path, "w") as f:
            f.write(plan_content)

        result = subprocess.run(
            ["python3", "tooling/fdc_cli.py", "lint", self.plan_file_path],
            capture_output=True,
            text=True
        )
        return result

    def test_lint_fails_without_justification_for_large_changeset(self):
        """
        Verify that the linter fails if a plan uses a tool that triggers
        large changesets without providing a 'review_justification.md'.
        """
        invalid_plan = (
            'set_plan "This plan should fail the new lint check"\n'
            'plan_step_complete ""\n'
            'run_in_bash_session python3 tooling/self_correction_orchestrator.py\n'
            'run_in_bash_session close --task-id test-task\n'
            'submit'
        )
        result = self._run_lint(invalid_plan)

        self.assertNotEqual(result.returncode, 0, "Linter should have failed but it passed.")
        self.assertIn(
            "Error: Plan uses a large-changeset tool ('tooling/self_correction_orchestrator.py') but does not provide a 'review_justification.md' file.",
            result.stderr
        )

    def test_lint_succeeds_with_justification_for_large_changeset(self):
        """
        Verify that the linter passes if a plan uses a large-changeset tool
        but correctly provides a 'review_justification.md' file.
        """
        valid_plan = (
            'set_plan "This plan should pass"\n'
            'plan_step_complete ""\n'
            'create_file_with_block review_justification.md "This change is large because..."\n'
            'run_in_bash_session python3 tooling/self_correction_orchestrator.py\n'
            'run_in_bash_session close --task-id test-task\n'
            'submit'
        )
        result = self._run_lint(valid_plan)
        self.assertEqual(result.returncode, 0, f"Linter should have passed but failed with error: {result.stderr}")
        self.assertIn("Linting Complete: All checks passed.", result.stdout)


if __name__ == "__main__":
    unittest.main()