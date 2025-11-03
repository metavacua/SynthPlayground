"""
A robust, reliable, and testable Command-Line Interface (CLI) for managing
the Finite Development Cycle (FDC).
"""

import argparse
import os
import sys
from datetime import datetime

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import Logger

def _log_event(task_id: str, event_type: str, details: dict, session_id: str):
    """Helper to log FDC events."""
    logger = Logger(session_id=session_id)
    logger.log(
        phase="Phase 6", # FDC management is a meta-level, "Phase 6" action
        task_id=task_id,
        plan_step=-1,
        action_type=event_type,
        action_details=details,
        outcome_status="SUCCESS",
        outcome_message=f"FDC CLI: {event_type} for task {task_id}."
    )

def start_task(task_id: str, session_id: str):
    """
    Initiates a new FDC task by logging the TASK_START event.
    """
    _log_event(task_id, "TASK_START", {"summary": f"FDC task '{task_id}' initiated."}, session_id)
    print(f"--- FDC: Task '{task_id}' formally started. ---")

def main():
    parser = argparse.ArgumentParser(description="A robust CLI for the Finite Development Cycle.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Initiate a new FDC task.")
    start_parser.add_argument("--task-id", required=True, help="A unique identifier for the task.")
    start_parser.add_argument("--session-id", required=True, help="The session ID for logging.")

    args = parser.parse_args()

    if args.command == "start":
        start_task(args.task_id, args.session_id)

if __name__ == "__main__":
    main()
