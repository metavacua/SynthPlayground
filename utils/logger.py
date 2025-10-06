import json
import uuid
import os
from datetime import datetime
from jsonschema import validate, ValidationError

# Load the schema once when the module is imported
try:
    with open("LOGGING_SCHEMA.md", "r") as f:
        content = f.read()
        start_marker = "```json"
        end_marker = "```"

        start_index = content.find(start_marker)
        if start_index == -1:
            raise ValueError("Could not find the start of the JSON schema in LOGGING_SCHEMA.md")

        # Find the end of the JSON block, starting the search *after* the start marker
        end_index = content.find(end_marker, start_index + len(start_marker))
        if end_index == -1:
            raise ValueError("Could not find the end of the JSON schema in LOGGING_SCHEMA.md")

        # Extract the JSON string
        json_str = content[start_index + len(start_marker) : end_index]
        SCHEMA = json.loads(json_str)
except FileNotFoundError:
    print("ERROR: LOGGING_SCHEMA.md not found. The Logger cannot function without it.")
    SCHEMA = None
except json.JSONDecodeError:
    print("ERROR: Failed to decode JSON from LOGGING_SCHEMA.md.")
    SCHEMA = None


class Logger:
    """
    A class to handle structured logging according to the schema defined in LOGGING_SCHEMA.md.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, session_id=None, log_file="logs/activity.log.jsonl"):
        if self._initialized:
            return

        if not SCHEMA:
            raise RuntimeError("Logger cannot be initialized because the LOGGING_SCHEMA could not be loaded.")

        self.session_id = session_id or str(uuid.uuid4())
        self.log_file = log_file

        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        self._initialized = True
        print(f"Logger initialized. Session ID: {self.session_id}")

    def _validate(self, log_entry):
        """Validate a log entry against the schema."""
        try:
            validate(instance=log_entry, schema=SCHEMA)
            return True, None
        except ValidationError as e:
            return False, e

    def log(self, phase, task_id, plan_step, action_type, action_details, outcome_status, outcome_message, evidence_citation=None):
        """
        Creates, validates, and writes a log entry.
        """
        log_entry = {
            "log_id": str(uuid.uuid4()),
            "session_id": self.session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "phase": phase,
            "task": {
                "id": task_id,
                "plan_step": plan_step
            },
            "action": {
                "type": action_type,
                "details": action_details
            },
            "outcome": {
                "status": outcome_status,
                "message": outcome_message
            }
        }

        if evidence_citation is not None:
            log_entry["evidence_citation"] = evidence_citation

        is_valid, error = self._validate(log_entry)
        if not is_valid:
            # This is a critical internal failure. The logger is producing invalid logs.
            # We should log this failure itself, but that could lead to recursion.
            # For now, print a clear error to stdout.
            print(f"FATAL LOGGER ERROR: Generated log entry failed validation: {error.message}")
            # Optionally, raise an exception to halt execution
            raise ValueError(f"Log validation failed: {error.message}")

        self._write_log(log_entry)
        return log_entry

    def _write_log(self, log_entry):
        """Appends a log entry to the log file."""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except IOError as e:
            print(f"ERROR: Could not write to log file {self.log_file}: {e}")

# Example usage:
# if __name__ == '__main__':
#     try:
#         logger = Logger(session_id="session-example-123")
#         logger.log(
#             phase="Phase 2.5",
#             task_id="bootstrap-logger-01",
#             plan_step=2,
#             action_type="TOOL_EXEC",
#             action_details={"command": "python utils/logger.py", "description": "Testing the logger implementation."},
#             outcome_status="SUCCESS",
#             outcome_message="Logger script executed successfully for testing.",
#             evidence_citation="Agent.md, Phase 1.5"
#         )
#         print(f"Successfully wrote a test log to {logger.log_file}")
#     except (RuntimeError, ValueError) as e:
#         print(f"An error occurred during logger test: {e}")