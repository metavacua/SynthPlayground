import json
import os
from datetime import datetime
from jsonschema import validate
import jsonschema  # Keep for potential future use, but address unused import for now.


# Assuming LOGGING_SCHEMA.md is at the root. A more robust implementation
# would use a config or environment variable for this path.
SCHEMA_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'LOGGING_SCHEMA.md')
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'activity.log.jsonl')


class Logger:
    """
    A utility for structured, schema-enforced logging.
    """
    _instance = None
    _schema = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance._load_schema()
        return cls._instance

    def _load_schema(self):
        """Loads the logging schema from the specified markdown file."""
        try:
            with open(SCHEMA_FILE_PATH, 'r') as f:
                # This is a simple parser. It assumes the schema is in a JSON code block.
                in_schema = False
                schema_str = ""
                for line in f:
                    if line.strip() == "```json":
                        in_schema = True
                        continue
                    if line.strip() == "```" and in_schema:
                        break
                    if in_schema:
                        schema_str += line
                self._schema = json.loads(schema_str)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # In a real application, this should probably be a fatal error.
            print(f"CRITICAL: Could not load or parse logging schema: {e}")
            self._schema = None

    def log(self, action_type, details, status="SUCCESS", critic_feedback="", task_id="N/A"):
        """
        Records a log entry after validating it against the schema.

        Args:
            action_type (str): The type of action being logged (e.g., 'TOOL_EXEC').
            details (dict): A dictionary with details about the action.
            status (str): The status of the action ('SUCCESS', 'FAILURE', 'INFO').
            critic_feedback (str): Any feedback from the internal critic.
            task_id (str): The ID of the task this log entry pertains to.

        Returns:
            bool: True if the log was successfully written, False otherwise.
        """
        if not self._schema:
            print("Logging failed: Schema not loaded.")
            return False

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": task_id,
            "action": {
                "type": action_type,
                "details": details
            },
            "outcome": {
                "status": status,
                "critic_feedback": critic_feedback
            }
        }

        try:
            validate(instance=log_entry, schema=self._schema)
            with open(LOG_FILE_PATH, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            return True
        except jsonschema.ValidationError as e:
            # This indicates a programming error - the code tried to log something
            # that doesn't conform to the schema.
            print(f"Log validation error: {e.message}")
            return False
        except IOError as e:
            print(f"Failed to write to log file: {e}")
            return False
