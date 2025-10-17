import unittest
import os
import shutil
from unittest.mock import patch, MagicMock, call
from tooling.capability_verifier import main as capability_verifier_main

class TestCapabilityVerifier(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_capability_verifier_dir"
        os.makedirs(os.path.join(self.test_dir, "knowledge_core"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "tests"), exist_ok=True)
        self.test_file = os.path.join(self.test_dir, "test_new_capability.py")
        with open(self.test_file, "w") as f:
            f.write("import unittest\nclass T(unittest.TestCase):\n    def test_fail(self): self.fail()")

        # Patch sys.argv to avoid parsing command line args
        patcher_argv = patch('sys.argv', ['tooling/capability_verifier.py', '--test-file', self.test_file])
        patcher_argv.start()
        self.addCleanup(patcher_argv.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('tooling.capability_verifier.subprocess.run')
    def test_successful_verification(self, mock_subprocess_run):
        """Tests the full successful workflow of the capability verifier."""
        mock_subprocess_run.side_effect = [
            MagicMock(returncode=1, stderr="Initial failure"),      # Step 1
            MagicMock(returncode=0, stdout="Orchestrator success"), # Step 2
            MagicMock(returncode=0, stdout="Final success"),        # Step 3
            MagicMock(returncode=0, stdout="Regression success")    # Step 4
        ]

        capability_verifier_main()

        self.assertEqual(mock_subprocess_run.call_count, 4)

    def test_unexpected_initial_pass(self):
        """Tests that the verifier exits if the initial test passes."""
        with patch('tooling.capability_verifier.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Unexpected pass")
            with self.assertRaises(SystemExit):
                capability_verifier_main()

    @patch('tooling.capability_verifier.subprocess.run')
    def test_orchestrator_failure(self, mock_run):
        """Tests that the verifier exits if the orchestrator fails."""
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="Initial failure"), # Step 1
            MagicMock(returncode=1, stderr="Orchestrator failure") # Step 2
        ]
        with self.assertRaises(SystemExit):
            capability_verifier_main()

    @patch('tooling.capability_verifier.subprocess.run')
    def test_final_test_failure(self, mock_run):
        """Tests that the verifier exits if the final test still fails."""
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="Initial failure"), # Step 1
            MagicMock(returncode=0, stdout="Orchestrator success"), # Step 2
            MagicMock(returncode=1, stderr="Final failure") # Step 3
        ]
        with self.assertRaises(SystemExit):
            capability_verifier_main()

    @patch('tooling.capability_verifier.subprocess.run')
    def test_regression_failure(self, mock_run):
        """Tests that the verifier exits if regression tests fail."""
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="Initial failure"), # Step 1
            MagicMock(returncode=0, stdout="Orchestrator success"), # Step 2
            MagicMock(returncode=0, stdout="Final success"), # Step 3
            MagicMock(returncode=1, stderr="Regression failure") # Step 4
        ]
        with self.assertRaises(SystemExit):
            capability_verifier_main()

if __name__ == "__main__":
    unittest.main()