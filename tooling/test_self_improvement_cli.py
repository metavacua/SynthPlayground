"""
Unit tests for the self-improvement analysis CLI tool.
"""

import unittest
import os
import json
from tooling.self_improvement_cli import (
    analyze_planning_efficiency,
    analyze_protocol_violations,
)


class TestPlanningEfficiencyAnalysis(unittest.TestCase):
    """Tests for the analyze_planning_efficiency function."""

    def setUp(self):
        """Set up a temporary log file for testing planning efficiency."""
        self.test_log_path = "temp_test_planning_activity.log.jsonl"
        log_entries = [
            # An efficient task with only one plan update
            {
                "task": {"id": "task-efficient-1"},
                "action": {"type": "PLAN_UPDATE"},
            },
            # An inefficient task with three plan revisions
            {
                "task": {"id": "task-inefficient-1"},
                "action": {"type": "PLAN_UPDATE"},
            },
            {
                "task": {"id": "task-inefficient-1"},
                "action": {"type": "PLAN_UPDATE"},
            },
            {
                "task": {"id": "task-inefficient-1"},
                "action": {"type": "PLAN_UPDATE"},
            },
        ]
        with open(self.test_log_path, "w") as f:
            for entry in log_entries:
                full_entry = {
                    "log_id": "test-id",
                    "session_id": "test-session",
                    "timestamp": "now",
                    "phase": "Phase 5",
                    "outcome": {"status": "SUCCESS"},
                }
                full_entry.update(entry)
                f.write(json.dumps(full_entry) + "\n")

    def tearDown(self):
        """Clean up the temporary log file."""
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)

    def test_analyze_planning_efficiency(self):
        """Test that the analysis correctly identifies tasks with multiple plan updates."""
        inefficient_tasks = analyze_planning_efficiency(self.test_log_path)
        self.assertEqual(len(inefficient_tasks), 1)
        self.assertIn("task-inefficient-1", inefficient_tasks)
        self.assertEqual(inefficient_tasks["task-inefficient-1"], 3)


class TestProtocolViolationAnalysis(unittest.TestCase):
    """Tests for the analyze_protocol_violations function."""

    def setUp(self):
        """Set up a temporary log file for testing protocol violations."""
        self.test_log_path = "temp_test_violation_activity.log.jsonl"
        log_entries = [
            # Case 1: Violation via SYSTEM_FAILURE
            {
                "task": {"id": "task-violation-1"},
                "action": {
                    "type": "SYSTEM_FAILURE",
                    "details": {"tool_name": "reset_all"},
                },
            },
            # Case 2: Violation via TOOL_EXEC
            {
                "task": {"id": "task-violation-2"},
                "action": {"type": "TOOL_EXEC", "details": {"command": "reset_all"}},
            },
            # Case 3: No violation (normal tool use)
            {
                "task": {"id": "task-clean-1"},
                "action": {"type": "TOOL_EXEC", "details": {"command": "ls -la"}},
            },
            # Case 4: No violation (unrelated system failure)
            {
                "task": {"id": "task-clean-2"},
                "action": {
                    "type": "SYSTEM_FAILURE",
                    "details": {"tool_name": "other_tool"},
                },
            },
        ]
        with open(self.test_log_path, "w") as f:
            for entry in log_entries:
                full_entry = {
                    "log_id": "test-id",
                    "session_id": "test-session",
                    "timestamp": "now",
                    "phase": "Phase 5",
                    "outcome": {"status": "SUCCESS"},
                }
                full_entry.update(entry)
                f.write(json.dumps(full_entry) + "\n")

    def tearDown(self):
        """Clean up the temporary log file."""
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)

    def test_analyze_protocol_violations(self):
        """Test that `reset_all` is detected in both SYSTEM_FAILURE and TOOL_EXEC logs."""
        violation_tasks = analyze_protocol_violations(self.test_log_path)
        self.assertEqual(len(violation_tasks), 2, "Should find exactly two violations")
        self.assertIn("task-violation-1", violation_tasks)
        self.assertIn("task-violation-2", violation_tasks)


if __name__ == "__main__":
    unittest.main()
