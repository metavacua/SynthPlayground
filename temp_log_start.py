import json
import datetime
import uuid
import os

LOG_FILE_PATH = os.path.join('logs', 'activity.log.jsonl')

def log_event(log_entry):
    """Appends a new log entry to the activity log, ensuring it's on a new line."""
    content_to_write = json.dumps(log_entry) + '\n'
    with open(LOG_FILE_PATH, 'a+') as f:
        f.seek(0, os.SEEK_END)
        if f.tell() > 0:
            f.seek(f.tell() - 1)
            if f.read(1) != '\n':
                f.write('\n')
        f.write(content_to_write)

def main():
    """Logs the start of the meta-analysis task."""
    task_id = "meta-analysis-of-failures-01"

    log_entry = {
        "log_id": str(uuid.uuid4()),
        "session_id": os.getenv("JULES_SESSION_ID", "unknown-session"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "Phase 2", # Task Ingestion
        "task": {
            "id": task_id,
            "plan_step": 1
        },
        "action": {
            "type": "TASK_START",
            "details": {
                "origin": "user_directive",
                "description": "Perform a comparative analysis of two development cycles to identify common failure patterns and propose protocol improvements."
            }
        },
        "outcome": {
            "status": "SUCCESS",
            "message": f"Task '{task_id}' initiated successfully."
        }
    }

    log_event(log_entry)
    print(f"Successfully logged the start of task: {task_id}")

if __name__ == "__main__":
    main()