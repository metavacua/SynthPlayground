import unittest
import os
import json
import io
from contextlib import redirect_stdout
from tooling.self_improvement_cli import analyze_logs, generate_tasks

class TestSelfImprovementCli(unittest.TestCase):

    def setUp(self):
        """Set up a temporary log file for testing."""
        self.test_log_path = "temp_activity.log.jsonl"
        # Point the tool to our test log file for the duration of the test
        from tooling import self_improvement_cli
        self.original_log_path = self_improvement_cli.LOG_FILE_PATH
        self_improvement_cli.LOG_FILE_PATH = self.test_log_path

        # Sample log data
        self.log_data = [
            {"task": {"id": "task-1"}, "action": {"type": "TOOL_EXEC"}, "outcome": {"status": "SUCCESS"}},
            {"task": {"id": "task-1"}, "action": {"type": "PLAN_UPDATE"}, "outcome": {"status": "SUCCESS"}},
            {"task": {"id": "task-2"}, "action": {"type": "TOOL_EXEC"}, "outcome": {"status": "FAILURE", "message": "Tool crashed"}},
            {"task": {"id": "task-3"}, "action": {"type": "PLAN_UPDATE"}, "outcome": {"status": "SUCCESS"}},
            {"task": {"id": "task-3"}, "action": {"type": "PLAN_UPDATE"}, "outcome": {"status": "SUCCESS"}},
            {"task": {"id": "task-3"}, "action": {"type": "TOOL_EXEC"}, "outcome": {"status": "SUCCESS"}},
        ]
        with open(self.test_log_path, 'w') as f:
            for entry in self.log_data:
                f.write(json.dumps(entry) + '\n')

    def tearDown(self):
        """Clean up the temporary log file."""
        os.remove(self.test_log_path)
        # Restore the original log path
        from tooling import self_improvement_cli
        self_improvement_cli.LOG_FILE_PATH = self.original_log_path

    def test_generate_tasks_identifies_failures(self):
        """Test that task generation correctly identifies failures."""
        failures = [entry for entry in self.log_data if entry["outcome"]["status"] == "FAILURE"]
        analysis_data = {'failures': failures, 'task_actions': {}}
        suggestions = generate_tasks(analysis_data)
        self.assertEqual(len(suggestions), 1)
        self.assertIn("Fix Past Failure", suggestions[0])
        self.assertIn("task-2", suggestions[0])

    def test_generate_tasks_identifies_planning_inefficiency(self):
        """Test that task generation correctly identifies multiple plan updates."""
        from collections import Counter
        task_actions = {
            "task-1": Counter({"PLAN_UPDATE": 1}),
            "task-3": Counter({"PLAN_UPDATE": 2})
        }
        analysis_data = {'failures': [], 'task_actions': task_actions}
        suggestions = generate_tasks(analysis_data)
        self.assertEqual(len(suggestions), 1)
        self.assertIn("Improve Protocol/Planning", suggestions[0])
        self.assertIn("task-3", suggestions[0])

    def test_analyze_logs_full_report(self):
        """Test the full analyze_logs function captures and reports correctly."""
        f = io.StringIO()
        with redirect_stdout(f):
            analyze_logs()
        output = f.getvalue()

        # Check for failure report
        self.assertIn("[!] Found 1 recorded failure(s):", output)
        self.assertIn("Task: task-2, Action: TOOL_EXEC, Message: Tool crashed", output)

        # Check for inefficiency report
        self.assertIn("Potential Inefficiency: Task required 2 plan updates.", output)

        # Check for suggested tasks
        self.assertIn("--- Suggested Proactive Tasks ---", output)
        self.assertIn("Fix Past Failure", output)
        self.assertIn("Improve Protocol/Planning", output)

if __name__ == "__main__":
    unittest.main()