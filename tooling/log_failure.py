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
