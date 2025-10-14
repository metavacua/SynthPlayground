"""
Provides a standardized, schema-validated logger for producing structured JSONL logs.

This module contains the `Logger` class, which is responsible for creating all
entries in the `logs/activity.log.jsonl` file. This is a critical component for
maintaining an auditable, machine-readable record of the agent's actions.

The logger enforces a strict structure on all log entries by validating them
against a formal JSON schema, which is extracted from the `LOGGING_SCHEMA.md`
document. This ensures that every log entry, regardless of its source, is
consistent and contains the required fields.

Key features of the `Logger` class:
- **Schema Validation:** Each log entry is validated against the official
  project schema before being written to disk, preventing data corruption.
- **Structured Data:** Logs are written in JSONL format, where each line is a
  valid JSON object, making them easy to parse and query.
- **Session Management:** It automatically assigns a unique `session_id` to
  all logs generated during its lifecycle, allowing actions to be traced back
  to a specific run.
- **Automatic Timestamps:** It injects a UTC timestamp into every log entry,
  providing a precise timeline of events.

This centralized logger is the sole mechanism by which the agent should record
its activities, ensuring a single source of truth for all post-mortem analysis
and self-improvement activities.
"""

import json
import uuid
import os
from datetime import datetime, timezone
from jsonschema import validate


class Logger:
    """
    A class to handle structured logging to a JSONL file, validated against a schema.
    """

    def __init__(
        self, schema_path="LOGGING_SCHEMA.md", log_path="logs/activity.log.jsonl"
    ):
        """
        Initializes the Logger, loading the schema and setting up the session.

        Args:
            schema_path (str): The path to the Markdown file containing the logging schema.
            log_path (str): The path to the log file to be written.
        """
        self.log_path = log_path
        self.schema = self._load_schema(schema_path)
        self.session_id = str(uuid.uuid4())
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _load_schema(self, schema_path):
        """
        Loads the JSON schema from the specified Markdown file.

        It assumes the schema is in a JSON code block.

        Args:
            schema_path (str): The path to the Markdown file containing the schema.

        Returns:
            dict: The loaded JSON schema.
        """
        try:
            with open(schema_path, "r") as f:
                content = f.read()

            # Extract the JSON part from the Markdown code block
            json_str = content.split("```json\n")[1].split("\n```")[0]
            return json.loads(json_str)
        except (FileNotFoundError, IndexError, json.JSONDecodeError) as e:
            # If schema doesn't exist or is malformed, operate without validation
            print(
                f"Warning: Could not load or parse schema from {schema_path}. Logger will operate without schema validation. Error: {e}"
            )
            return None

    def log(
        self,
        phase,
        task_id,
        plan_step,
        action_type,
        action_details,
        outcome_status,
        outcome_message="",
        error_details=None,
        evidence="",
    ):
        """
        Constructs, validates, and writes a log entry.

        Args:
            phase (str): The current protocol phase (e.g., "Phase 7").
            task_id (str): The ID of the current task.
            plan_step (int): The current plan step number.
            action_type (str): The type of action (e.g., "TOOL_EXEC").
            action_details (dict): Details specific to the action.
            outcome_status (str): The outcome of the action ("SUCCESS", "FAILURE").
            outcome_message (str, optional): A message describing the outcome. Defaults to "".
            error_details (dict, optional): Structured error info if the outcome is a failure. Defaults to None.
            evidence (str, optional): Citation for the action. Defaults to "".

        Raises:
            ValidationError: If the generated log entry does not conform to the schema.
        """
        log_entry = {
            "log_id": str(uuid.uuid4()),
            "session_id": self.session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": phase,
            "task": {"id": task_id, "plan_step": plan_step},
            "action": {"type": action_type, "details": action_details},
            "outcome": {"status": outcome_status, "message": outcome_message},
            "evidence_citation": evidence,
        }

        if error_details and outcome_status == "FAILURE":
            log_entry["outcome"]["error"] = error_details

        if self.schema:
            validate(instance=log_entry, schema=self.schema)

        # Ensure the log directory exists before writing
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
