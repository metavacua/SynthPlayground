"""
This module provides functionality for...
"""

import datetime
import json
import os
import uuid

ACTION_TYPE_MAP = {
    "set_plan": "plan_op",
    "plan_step_complete": "step_op",
    "submit": "submit_op",
    "create_file_with_block": "write_op",
    "overwrite_file_with_block": "write_op",
    "replace_with_git_merge_diff": "write_op",
    "read_file": "read_op",
    "list_files": "read_op",
    "grep": "read_op",
    "delete_file": "delete_op",
    "rename_file": "move_op",
    "run_in_bash_session": "tool_exec",
    "for_each_file": "loop_op",
    "define_set_of_names": "define_names_op",
    "define_diagonalization_function": "define_diag_op",
}


def create_log_entry(task_id, action_type, details):
    """Creates a structured log entry dictionary."""
    return {
        "log_id": str(uuid.uuid4()),
        "session_id": os.getenv("JULES_SESSION_ID", "unknown"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "Phase 6",
        "task": {"id": task_id, "plan_step": -1},
        "action": {"type": action_type, "details": details},
        "outcome": {
            "status": "SUCCESS",
            "message": f"FDC CLI: {action_type} for task {task_id}.",
        },
    }


def analyze_plan_content(plan_lines_with_indent):
    """Analyzes the content of a plan file to determine its complexity class and modality."""
    plan_lines = [line.strip() for line in plan_lines_with_indent if line.strip()]

    # --- Complexity Analysis ---
    loop_indents = []
    for line in plan_lines_with_indent:
        if line.strip().startswith("for_each_file"):
            indent = len(line) - len(line.lstrip(" "))
            loop_indents.append(indent)

    if not loop_indents:
        complexity_class = "P"
        complexity_string = "Constant (O(1))"
    elif max(loop_indents) > min(loop_indents):
        complexity_class = "EXP"
        complexity_string = "Exponential (EXPTIME-Class)"
    else:
        complexity_class = "P"
        complexity_string = "Polynomial (P-Class)"

    # --- Modality Analysis ---
    has_write_op = False
    write_ops = {"write_op", "delete_op", "move_op"}
    for line in plan_lines:
        command = line.split()[0]
        action_type = ACTION_TYPE_MAP.get(command)
        if action_type in write_ops:
            has_write_op = True
            break

    modality = "Construction (Read-Write)" if has_write_op else "Analysis (Read-Only)"

    return {
        "complexity_class": complexity_class,
        "complexity_string": complexity_string,
        "modality": modality,
    }
