import unittest
import os
import json
import shutil
from jsonschema import ValidationError
from utils.logger import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        """Set up a temporary environment for each test."""
        self.test_dir = "test_temp"
        os.makedirs(self.test_dir, exist_ok=True)

        self.schema_path = os.path.join(self.test_dir, "test_schema.md")
        self.log_path = os.path.join(self.test_dir, "test_activity.log.jsonl")

        # A simplified, valid schema for testing
        self.test_schema = {
            "type": "object",
            "properties": {
                "log_id": {"type": "string"},
                "session_id": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"},
                "phase": {"type": "string"},
                "task": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "plan_step": {"type": "integer"}
                    },
                    "required": ["id", "plan_step"]
                },
                "action": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "details": {"type": "object"}
                    },
                    "required": ["type", "details"]
                },
                "outcome": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"}
                    },
                    "required": ["status"]
                },
                "evidence_citation": {"type": "string"}
            },
            "required": ["log_id", "session_id", "timestamp", "phase", "task", "action", "outcome"]
        }

        # Write the schema to the test file
        with open(self.schema_path, 'w') as f:
            f.write("```json\n")
            f.write(json.dumps(self.test_schema))
            f.write("\n```")

        # Ensure the log file is empty before each test
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

        self.logger = Logger(schema_path=self.schema_path, log_path=self.log_path)

    def tearDown(self):
        """Clean up the temporary environment after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_log_success(self):
        """Test that a valid log entry is written successfully."""
        self.logger.log(
            phase="Phase 7",
            task_id="test-task-01",
            plan_step=1,
            action_type="TOOL_EXEC",
            action_details={"command": "ls"},
            outcome_status="SUCCESS",
            outcome_message="Command executed.",
            evidence="Test case"
        )

        self.assertTrue(os.path.exists(self.log_path))
        with open(self.log_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            log_data = json.loads(lines[0])
            self.assertEqual(log_data['task']['id'], "test-task-01")
            self.assertEqual(log_data['action']['type'], "TOOL_EXEC")
            self.assertEqual(log_data['outcome']['status'], "SUCCESS")

    def test_log_failure_invalid_data(self):
        """Test that logging fails with a ValidationError for data that violates the schema."""
        with self.assertRaises(ValidationError):
            # Missing required field 'plan_step' inside task object
            self.logger.log(
                phase="Phase 2",
                task_id="invalid-task-02",
                plan_step=None, # This is the error
                action_type="FILE_READ",
                action_details={"path": "/dev/null"},
                outcome_status="SUCCESS"
            )

        # Ensure no log file was written
        self.assertFalse(os.path.exists(self.log_path))

    def test_schema_load_failure(self):
        """Test that the Logger raises an error if the schema file is malformed."""
        bad_schema_path = os.path.join(self.test_dir, "bad_schema.md")
        with open(bad_schema_path, 'w') as f:
            f.write("This is not a valid schema file.")

        with self.assertRaises(IOError):
            Logger(schema_path=bad_schema_path, log_path=self.log_path)

if __name__ == '__main__':
    unittest.main()