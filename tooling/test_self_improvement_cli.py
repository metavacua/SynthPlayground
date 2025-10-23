import unittest
import os
import json
from tooling.self_improvement_cli import (
    analyze_planning_efficiency,
    analyze_error_rates,
    analyze_protocol_violations,
)

class TestSelfImprovementCli(unittest.TestCase):

    def setUp(self):
        self.log_file = "test_activity.log.jsonl"
        with open(self.log_file, "w") as f:
            f.write(json.dumps({"task_id": "task-1", "action": {"type": "PLAN_UPDATE"}}) + "\n")
            f.write(json.dumps({"task_id": "task-1", "action": {"type": "PLAN_UPDATE"}}) + "\n")
            f.write(json.dumps({"task_id": "task-2", "action": {"type": "TOOL_EXEC"}, "outcome": {"status": "SUCCESS"}}) + "\n")
            f.write(json.dumps({"task_id": "task-3", "action": {"type": "TOOL_EXEC"}, "outcome": {"status": "FAILURE"}}) + "\n")
            f.write(json.dumps({"task_id": "task-4", "action": {"type": "SYSTEM_FAILURE"}, "outcome": {"message": "reset_all"}}) + "\n")

    def tearDown(self):
        os.remove(self.log_file)

    def test_analyze_planning_efficiency(self):
        inefficient_tasks = analyze_planning_efficiency(self.log_file)
        self.assertEqual(inefficient_tasks, {"task-1": 2})

    def test_analyze_error_rates(self):
        error_data = analyze_error_rates(self.log_file)
        self.assertEqual(error_data["total_actions"], 5)
        self.assertEqual(error_data["total_failures"], 1)
        self.assertEqual(error_data["failure_rate"], 0.2)

    def test_analyze_protocol_violations(self):
        violations = analyze_protocol_violations(self.log_file)
        self.assertEqual(violations, ["task-4"])

if __name__ == "__main__":
    unittest.main()
