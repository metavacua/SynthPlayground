#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import subprocess
import uuid

# --- Constants ---
LOG_FILE_PATH = "logs/activity.log.jsonl"

def log_action(action_type, details):
    """Appends a structured log entry to the activity log."""
    # Ensure the directory for the log file exists.
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "action_type": action_type,
        "details": details
    }
    with open(LOG_FILE_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def handle_start(args):
    """Handles the logic for starting a new standard task."""
    task_id = str(uuid.uuid4())
    branch_name = f"feature/task-{task_id}"

    print(f"Starting new task: {task_id}")
    print(f"Description: {args.description}")
    print(f"Stance: {args.stance}")

    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True, text=True)
        print(f"Successfully created and checked out branch: {branch_name}")

        log_action("TASK_START", {
            "task_id": task_id,
            "branch": branch_name,
            "description": args.description,
            "stance": args.stance
        })
        print("Task start logged.")

    except subprocess.CalledProcessError as e:
        print(f"Error creating git branch: {e.stderr}")
    except FileNotFoundError:
        print("Error: git command not found. Is git installed and in your PATH?")

def create_parser():
    """Creates and returns the ArgumentParser object for the CLI."""
    parser = argparse.ArgumentParser(description="Finite Development Cycle (FDC) Command-Line Tool.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Start Command ---
    parser_start = subparsers.add_parser("start", help="Start a new development task.")
    parser_start.add_argument("description", type=str, help="A brief description of the task.")
    parser_start.add_argument("--stance", type=str, default="Standard", choices=["Standard", "Cautious", "Harvester"], help="The operational stance for this task.")

    return parser

def main():
    """Main function to parse arguments and call handlers."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "start":
        handle_start(args)

if __name__ == "__main__":
    main()