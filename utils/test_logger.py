import unittest
import os
import json
import shutil
from utils.logger import Logger


class TestLogger(unittest.TestCase):

    TEST_LOGS_DIR = "test_logs"
    TEST_SCHEMA_DIR = "test_schema"
    LOG_FILE = os.path.join(TEST_LOGS_DIR, "activity.log.jsonl")
    SCHEMA_FILE = os.path.join(TEST_SCHEMA_DIR, "LOGGING_SCHEMA.md")

    def setUp(self):
        """Set up a temporary environment for testing."""
        # Create temporary directories
        os.makedirs(self.TEST_LOGS_DIR, exist_ok=True)
        os.makedirs(self.TEST_SCHEMA_DIR, exist_ok=True)

        # Create a dummy schema file
        dummy_schema = {
            "type": "object",
            "properties": {
                "timestamp": {"type": "string"},
                "task_id": {"type": "string"},
                "action": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "details": {"type": "object"},
                    },
                    "required": ["type", "details"],
                },
                "outcome": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "critic_feedback": {"type": "string"},
                    },
                    "required": ["status"],
                },
            },
            "required": ["timestamp", "action", "outcome"],
        }
        with open(self.SCHEMA_FILE, "w") as f:
            f.write("```json\n")
            f.write(json.dumps(dummy_schema, indent=2))
            f.write("\n```")

        # Point the logger to our test files
        Logger._schema = None  # Reset schema to force reload
        Logger.SCHEMA_FILE_PATH = self.SCHEMA_FILE
        Logger.LOG_FILE_PATH = self.LOG_FILE

        # Ensure the log file is clean before each test
        if os.path.exists(self.LOG_FILE):
            os.remove(self.LOG_FILE)

    def tearDown(self):
        """Clean up the temporary environment."""
        shutil.rmtree(self.TEST_LOGS_DIR)
        shutil.rmtree(self.TEST_SCHEMA_DIR)

    def test_singleton_instance(self):
        """Test that the Logger is a singleton."""
        logger1 = Logger()
        logger2 = Logger()
        self.assertIs(logger1, logger2)

    def test_log_success(self):
        """Test a successful log write."""
        logger = Logger()
        result = logger.log(
            action_type="TEST_ACTION", details={"key": "value"}, status="SUCCESS"
        )
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.LOG_FILE))
        with open(self.LOG_FILE, "r") as f:
            log_entry = json.loads(f.readline())
            self.assertEqual(log_entry["action"]["type"], "TEST_ACTION")

    def test_log_validation_failure(self):
        """Test that a log fails validation if it doesn't match the schema."""
        logger = Logger()
        # 'details' is missing, which is required by our dummy schema
        result = logger.log(
            action_type="INVALID_ACTION",
            details=None,  # This will cause a validation error
        )
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.LOG_FILE))


if __name__ == "__main__":
    unittest.main()
