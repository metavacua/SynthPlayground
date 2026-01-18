#!/usr/bin/env python3
"""
Unit tests for sandbox probe framework.

Tests cover:
- Probe compilation
- Probe execution
- Output parsing
- Result interpretation
- JSON serialization
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from tooling.sandbox_probe_runner import ProbeResult, ProbeExecution, SandboxProbeRunner


class TestProbeResult(unittest.TestCase):
    """Test the ProbeResult class."""

    def test_probe_result_success(self):
        """Test creating a successful probe result."""
        result = ProbeResult(
            test_name="READ /etc/hostname", success=True, observation="sandbox-vm-1"
        )

        self.assertTrue(result.success)
        self.assertEqual(result.test_name, "READ /etc/hostname")
        self.assertEqual(result.observation, "sandbox-vm-1")
        self.assertIsNone(result.error)
        self.assertIsNone(result.interpretation)
        self.assertIsNone(result.constraint)

    def test_probe_result_failure(self):
        """Test creating a failed probe result."""
        result = ProbeResult(
            test_name="WRITE /tmp/test.txt",
            success=False,
            error="PermissionDeniedException - Permission denied",
            interpretation="Permission denied - sandbox enforces access restrictions",
            constraint="Sandbox forbids WRITE /tmp/test.txt",
        )

        self.assertFalse(result.success)
        self.assertEqual(result.test_name, "WRITE /tmp/test.txt")
        self.assertEqual(result.error, "PermissionDeniedException - Permission denied")
        self.assertEqual(
            result.interpretation,
            "Permission denied - sandbox enforces access restrictions",
        )
        self.assertEqual(result.constraint, "Sandbox forbids WRITE /tmp/test.txt")

    def test_probe_result_to_dict(self):
        """Test converting ProbeResult to dictionary."""
        result = ProbeResult(
            test_name="TEST_NAME", success=True, observation="test_observation"
        )

        result_dict = result.to_dict()

        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict["test_name"], "TEST_NAME")
        self.assertTrue(result_dict["success"])
        self.assertEqual(result_dict["observation"], "test_observation")


class TestProbeExecution(unittest.TestCase):
    """Test the ProbeExecution class."""

    def test_probe_execution_initialization(self):
        """Test initializing a probe execution."""
        execution = ProbeExecution(
            probe_name="filesystem",
            timestamp="2026-01-18T06:24:34Z",
            objective="Determine filesystem constraints",
        )

        self.assertEqual(execution.probe_name, "filesystem")
        self.assertEqual(execution.timestamp, "2026-01-18T06:24:34Z")
        self.assertEqual(execution.objective, "Determine filesystem constraints")
        self.assertEqual(len(execution.tests), 0)
        self.assertEqual(len(execution.conclusions), 0)

    def test_probe_execution_add_test(self):
        """Test adding tests to execution."""
        execution = ProbeExecution(
            probe_name="test",
            timestamp="2026-01-18T06:24:34Z",
            objective="Test objective",
        )

        result1 = ProbeResult("TEST_1", True, observation="result1")
        result2 = ProbeResult("TEST_2", False, error="Error occurred")

        execution.add_test(result1)
        execution.add_test(result2)

        self.assertEqual(len(execution.tests), 2)
        self.assertEqual(execution.tests[0].test_name, "TEST_1")
        self.assertEqual(execution.tests[1].test_name, "TEST_2")

    def test_probe_execution_to_dict(self):
        """Test converting ProbeExecution to dictionary."""
        execution = ProbeExecution(
            probe_name="test",
            timestamp="2026-01-18T06:24:34Z",
            objective="Test objective",
        )

        result = ProbeResult("TEST_1", True, observation="result1")
        execution.add_test(result)
        execution.conclusions = ["Test conclusion"]
        execution.next_probe = "network"

        execution_dict = execution.to_dict()

        self.assertIsInstance(execution_dict, dict)
        self.assertEqual(execution_dict["probe_name"], "test")
        self.assertEqual(len(execution_dict["tests"]), 1)
        self.assertEqual(len(execution_dict["conclusions"]), 1)
        self.assertEqual(execution_dict["next_probe"], "network")


class TestSandboxProbeRunner(unittest.TestCase):
    """Test the SandboxProbeRunner class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.probes_dir = Path(self.temp_dir) / "probes"
        self.experiments_dir = Path(self.temp_dir) / "experiments"
        self.java_dir = Path(self.temp_dir) / "java"
        self.java_bin = self.java_dir / "bin"

        self.probes_dir.mkdir(parents=True)
        self.experiments_dir.mkdir(parents=True)
        self.java_bin.mkdir(parents=True)

        # Mock Java executables
        (self.java_bin / "javac").touch(mode=0o755)
        (self.java_bin / "java").touch(mode=0o755)

        # Patch the constants
        self.runner = SandboxProbeRunner(verbose=False)
        self.runner.PROBES_DIR = self.probes_dir
        self.runner.EXPERIMENTS_DIR = self.experiments_dir
        self.runner.JAVAC = self.java_bin / "javac"
        self.runner.JAVA = self.java_bin / "java"

    def tearDown(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.temp_dir)

    def test_run_command_success(self):
        """Test running a command successfully."""
        with patch.object(self.runner, "_run_command") as mock_run:
            mock_run.return_value = (0, "output", "")

            returncode, stdout, stderr = self.runner._run_command(["echo", "test"])

            self.assertEqual(returncode, 0)
            self.assertEqual(stdout, "output")
            self.assertEqual(stderr, "")

    def test_interpret_failure_permission_denied(self):
        """Test interpreting PermissionDeniedException."""
        test_name = "WRITE /tmp/test.txt"
        error = "PermissionDeniedException - Permission denied"

        interpretation = self.runner._interpret_failure(test_name, error)

        self.assertIn("Permission denied", interpretation)
        self.assertIn("sandbox enforces", interpretation)

    def test_interpret_failure_no_such_file(self):
        """Test interpreting NoSuchFileException."""
        test_name = "READ /nonexistent/file.txt"
        error = "NoSuchFileException - /nonexistent/file.txt"

        interpretation = self.runner._interpret_failure(test_name, error)

        self.assertIn("does not exist", interpretation)

    def test_infer_constraint_permission_denied(self):
        """Test inferring constraint from PermissionDeniedException."""
        test_name = "WRITE /tmp/test.txt"
        error = "PermissionDeniedException - Permission denied"

        constraint = self.runner._infer_constraint(test_name, error)

        self.assertIn("Sandbox forbids", constraint)

    def test_infer_constraint_no_such_file(self):
        """Test inferring constraint from NoSuchFileException."""
        test_name = "READ /nonexistent/file.txt"
        error = "NoSuchFileException - /nonexistent/file.txt"

        constraint = self.runner._infer_constraint(test_name, error)

        self.assertIn("does not exist", constraint)

    def test_parse_probe_output_simple(self):
        """Test parsing simple probe output."""
        output = """=== TEST PROBE START ===
✓ READ /etc/hostname
  Content: sandbox-vm-1
✗ WRITE /tmp/test.txt
  Error: PermissionDeniedException - Permission denied
=== TEST PROBE END ==="""

        execution = self.runner._parse_probe_output("test", output)

        self.assertEqual(len(execution.tests), 2)
        self.assertTrue(execution.tests[0].success)
        self.assertFalse(execution.tests[1].success)
        self.assertEqual(execution.tests[0].observation, "sandbox-vm-1")
        self.assertIn("PermissionDeniedException", execution.tests[1].error)

    def test_parse_probe_output_with_list(self):
        """Test parsing probe output with list results."""
        output = """=== TEST PROBE START ===
✓ LIST /tmp
  - file1.txt
  - file2.txt
✗ LIST /workspace
  Error: NoSuchFileException - /workspace
=== TEST PROBE END ==="""

        execution = self.runner._parse_probe_output("test", output)

        self.assertEqual(len(execution.tests), 2)
        self.assertTrue(execution.tests[0].success)
        self.assertFalse(execution.tests[1].success)

    def test_generate_conclusions_filesystem(self):
        """Test generating conclusions for filesystem probe."""
        execution = ProbeExecution(
            probe_name="filesystem",
            timestamp="2026-01-18T06:24:34Z",
            objective="Test objective",
        )

        # Add test results
        execution.add_test(
            ProbeResult("READ /etc/hostname", True, observation="sandbox-vm-1")
        )
        execution.add_test(
            ProbeResult("WRITE /tmp/test.txt", True, observation="/tmp/test.txt")
        )
        execution.add_test(
            ProbeResult(
                "WRITE /workspace/test.txt",
                False,
                error="NoSuchFileException",
                interpretation="Resource does not exist",
                constraint="Sandbox forbids WRITE /workspace",
            )
        )
        execution.add_test(
            ProbeResult("WORKING_DIRECTORY", True, observation="/home/engine/project")
        )

        conclusions = self.runner._generate_conclusions(execution, "filesystem")

        self.assertIsInstance(conclusions, list)
        self.assertGreater(len(conclusions), 0)

        # Check that expected conclusions are present
        conclusions_str = " ".join(conclusions)
        self.assertIn("read access", conclusions_str)

    def test_suggest_next_probe(self):
        """Test suggesting next probe in sequence."""
        self.assertEqual(self.runner._suggest_next_probe("filesystem"), "network")
        self.assertEqual(self.runner._suggest_next_probe("network"), "services")
        self.assertIsNone(self.runner._suggest_next_probe("services"))
        self.assertIsNone(self.runner._suggest_next_probe("unknown"))

    def test_save_results(self):
        """Test saving probe results to JSON file."""
        execution = ProbeExecution(
            probe_name="test",
            timestamp="2026-01-18T06:24:34Z",
            objective="Test objective",
        )

        result = ProbeResult("TEST_1", True, observation="result1")
        execution.add_test(result)

        filepath = self.runner.save_results(execution)

        self.assertTrue(filepath.exists())
        self.assertTrue(filepath.is_file())

        # Verify JSON content
        with open(filepath, "r") as f:
            data = json.load(f)

        self.assertEqual(data["probe_name"], "test")
        self.assertEqual(len(data["tests"]), 1)


class TestProbeOutputFormat(unittest.TestCase):
    """Test that probe output format is correct."""

    def test_success_marker(self):
        """Test that success marker is present."""
        output_lines = ["✓ READ /etc/hostname", "  Content: test"]

        self.assertTrue(output_lines[0].startswith("✓"))
        self.assertTrue("Content:" in output_lines[1])

    def test_failure_marker(self):
        """Test that failure marker is present."""
        output_lines = [
            "✗ WRITE /tmp/test.txt",
            "  Error: PermissionDeniedException - Permission denied",
        ]

        self.assertTrue(output_lines[0].startswith("✗"))
        self.assertTrue("Error:" in output_lines[1])

    def test_output_structure(self):
        """Test that output follows expected structure."""
        sample_output = """=== PROBE START ===
✓ TEST_ONE path
  Detail: information
✗ TEST_TWO path
  Error: ExceptionType - message
=== PROBE END ==="""

        self.assertIn("=== PROBE START ===", sample_output)
        self.assertIn("=== PROBE END ===", sample_output)
        self.assertIn("✓", sample_output)
        self.assertIn("✗", sample_output)


class TestEvidenceGrounding(unittest.TestCase):
    """Test that all conclusions are grounded in evidence."""

    def test_success_grounding(self):
        """Test that successful tests provide evidence."""
        result = ProbeResult(
            test_name="READ /etc/hostname", success=True, observation="sandbox-vm-1"
        )

        # Evidence is the observation
        self.assertIsNotNone(result.observation)
        self.assertEqual(result.observation, "sandbox-vm-1")

    def test_failure_grounding(self):
        """Test that failed tests provide evidence."""
        result = ProbeResult(
            test_name="WRITE /tmp/test.txt",
            success=False,
            error="PermissionDeniedException - Permission denied",
            interpretation="Permission denied - sandbox enforces access restrictions",
            constraint="Sandbox forbids WRITE /tmp/test.txt",
        )

        # Evidence is the error, interpretation, and constraint
        self.assertIsNotNone(result.error)
        self.assertIsNotNone(result.interpretation)
        self.assertIsNotNone(result.constraint)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestProbeResult))
    suite.addTests(loader.loadTestsFromTestCase(TestProbeExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestSandboxProbeRunner))
    suite.addTests(loader.loadTestsFromTestCase(TestProbeOutputFormat))
    suite.addTests(loader.loadTestsFromTestCase(TestEvidenceGrounding))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    import sys

    sys.exit(run_tests())
