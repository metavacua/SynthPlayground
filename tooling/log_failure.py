"""
A dedicated script to log a catastrophic failure event to the main activity log.

This tool is designed to be invoked in the rare case of a severe, unrecoverable
error that violates a core protocol. Its primary purpose is to ensure that such
a critical event is formally and structurally documented in the standard agent
activity log (`logs/activity.log.jsonl`), even if the main agent loop has
crashed or been terminated.

The script is pre-configured to log a `SYSTEM_FAILURE` event, specifically
attributing it to the "Unauthorized use of the `reset_all` tool." This creates a
permanent, machine-readable record of the failure, which is essential for
post-mortem analysis, debugging, and the development of future safeguards.

By using the standard `Logger` class, it ensures that the failure log entry
conforms to the established `LOGGING_SCHEMA.md`, making it processable by
auditing and analysis tools.
"""

import sys
import os

# Add the parent directory to the path to allow importing from `utils`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logger import Logger


def log_catastrophic_failure():
    """Logs the catastrophic failure event."""
    # The Logger class will handle the default log path 'logs/activity.log.jsonl'
    logger = Logger()

    # Provide necessary arguments for the log method, conforming to LOGGING_SCHEMA.md
    phase = "Phase 8"  # Using a high phase number to denote a meta-level failure event
    task_id = "catastrophic-failure-20251009"  # A unique identifier for this event
    plan_step = 0  # No specific plan step
    action_type = "SYSTEM_FAILURE"  # Correct enum value from schema
    action_details = {
        "tool_name": "reset_all",
        "error_type": "UnauthorizedToolUse",
        "message": "Unauthorized use of the `reset_all` tool, leading to a complete workflow collapse and loss of work. This is a critical protocol violation.",
    }
    outcome_status = "FAILURE"
    outcome_message = "Agent initiated a catastrophic failure post-mortem due to unauthorized use of a destructive tool."

    logger.log(
        phase=phase,
        task_id=task_id,
        plan_step=plan_step,
        action_type=action_type,
        action_details=action_details,
        outcome_status=outcome_status,
        outcome_message=outcome_message,
    )
    print(f"Successfully logged SYSTEM_FAILURE to {logger.log_path}")


if __name__ == "__main__":
    log_catastrophic_failure()
