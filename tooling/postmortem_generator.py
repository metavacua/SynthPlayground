"""
Generates a structured, data-driven post-mortem report from an activity log.
"""

import argparse
import json
import uuid
from datetime import datetime
import os

LOG_FILE = "logs/activity.log.jsonl"
POSTMORTEM_DIR = "postmortems"

def generate_postmortem(task_id: str, session_id: str) -> str:
    """
    Analyzes the activity log to generate a structured post-mortem for a specific task and session.
    """
    task_events = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get("task", {}).get("id") == task_id and event.get("session_id") == session_id:
                        task_events.append(event)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"Error: Log file not found at '{LOG_FILE}'")
        return None

    if not task_events:
        print(f"Warning: No events found for task_id '{task_id}' in session '{session_id}'.")
        return None

    final_event = task_events[-1]
    final_status = final_event.get("outcome", {}).get("status", "UNKNOWN")

    # --- Content Generation ---
    executive_summary = "This report is an automated analysis of the execution of task `{task_id}`. The task concluded with a status of **{final_status}**."

    timeline = ""
    for event in task_events:
        timeline += f"- `{event.get('timestamp')}` - {event.get('outcome', {}).get('message', 'No message.')}\n"

    objective = "The agent's objective was to complete the task as defined by its input arguments."
    outcome = f"The final outcome of the task was: {final_status}."
    discrepancy = "No discrepancy." if final_status == "SUCCESS" else "The final outcome deviated from the objective."

    # For this version, Causal Analysis and Structured Lessons will be placeholders.
    # A more advanced agent would be required to perform true root cause analysis.
    causal_analysis = "### Issue 1: Task Outcome\n*   **Observation:** The task completed with status: `{final_status}`.\n*   **Immediate Cause:** See final log message.\n*   **Root Cause:** To be determined by a future, more advanced analysis agent.\n*   **Log Evidence:** See timeline."

    lesson = {
      "lesson_id": str(uuid.uuid4()),
      "task_id": task_id,
      "date": datetime.utcnow().strftime("%Y-%m-%d"),
      "category": "Process",
      "severity": "Medium" if final_status == "FAILURE" else "Low",
      "description": f"The task '{task_id}' completed with status '{final_status}'.",
      "actionable_change": { "type": "REVIEW", "details": { "target_file": "N/A", "change_description": "A human or advanced agent should review the outcome of this task." } },
      "status": "pending"
    }

    report = f"""# Structured Post-Mortem and Lesson Generation

**Task ID:** `{task_id}`
**Completion Date:** `{datetime.utcnow().isoformat()}`
**Final Status:** `{final_status}`

---

## 1. Executive Summary
{executive_summary.format(task_id=task_id, final_status=final_status)}

---

## 2. Impact Assessment
- **User Impact:** No direct user impact. This was an autonomous agent task.
- **System Impact:** System performed as expected.
- **Business Impact:** N/A

---

## 3. Timeline of Events
{timeline}
---

## 4. Objective vs. Outcome Analysis
**Stated Objective:**
{objective}

**Final Outcome:**
{outcome}

**Discrepancy Analysis:**
{discrepancy}

---

## 5. Causal Analysis of Failures and Inefficiencies
{causal_analysis.format(final_status=final_status)}
---

## 6. Generation of Structured Lessons
### Lesson 1:
```json
{json.dumps(lesson, indent=2)}
```
---

## 7. General Reflections
This automated report provides a baseline for future, more sophisticated analysis.
"""

    os.makedirs(POSTMORTEM_DIR, exist_ok=True)
    safe_task_id = task_id.replace("/", "_").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{safe_task_id}.md"
    filepath = os.path.join(POSTMORTEM_DIR, filename)

    with open(filepath, "w") as f:
        f.write(report)

    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a structured post-mortem report.")
    parser.add_argument("--task-id", required=True, help="The task ID to analyze.")
    parser.add_argument("--session-id", required=True, help="The session ID to filter logs by.")
    args = parser.parse_args()

    report_path = generate_postmortem(args.task_id, args.session_id)
    if report_path:
        print(report_path)
