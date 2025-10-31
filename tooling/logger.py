"""
This module provides a centralized logging utility for the agent toolchain.
"""

import json
import os
from datetime import datetime, timezone
import uuid

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE_PATH = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")

def create_log_entry(task_id, action_type, details, plan_step=-1, session_id="unknown"):
    """Creates a structured log entry."""
    return {
        "log_id": str(uuid.uuid4()),
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": "Phase 6",  # Placeholder
        "task": {"id": task_id, "plan_step": plan_step},
        "action": {"type": action_type, "details": details},
        "outcome": {"status": "SUCCESS", "message": f"Logged action: {action_type}"},
    }

def log_event(log_entry):
    """Appends a new log entry to the activity log."""
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    content_to_write = json.dumps(log_entry) + "\n"
    with open(LOG_FILE_PATH, "a+") as f:
        f.write(content_to_write)
