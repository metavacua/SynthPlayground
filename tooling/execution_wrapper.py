import argparse
import os
import sys
import json
import subprocess
import traceback
from typing import Dict, Any, List

# Add parent directory to path to allow imports from utils
# This ensures that the script can be run from the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import Logger

# --- Tool Implementations ---

def _list_files(path: str = ".") -> List[str]:
    """Corresponds to the `list_files` tool. Uses `ls` for consistency."""
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directory not found: {path}")
    result = subprocess.run(
        ['ls', '-1F', '--group-directories-first', path],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip().split('\n') if result.stdout else []

def _read_file(filepath: str) -> str:
    """Corresponds to the `read_file` tool."""
    with open(filepath, 'r') as f:
        return f.read()

def _create_file_with_block(filepath: str, content: str):
    """Corresponds to the `create_file_with_block` tool."""
    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

def _delete_file(filepath: str):
    """Corresponds to the `delete_file` tool."""
    os.remove(filepath)

def _rename_file(filepath: str, new_filepath: str):
    """Corresponds to the `rename_file` tool."""
    os.rename(filepath, new_filepath)

import shlex

def _run_in_bash_session(*command_parts: str) -> str:
    """Corresponds to the `run_in_bash_session` tool."""
    # Reconstruct the command from its parts.
    command = shlex.join(command_parts)
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    # Return a structured dictionary for clearer results
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}

def _replace_with_git_merge_diff(filepath: str, search_block: str, replace_block: str) -> str:
    """A simplified implementation of the `replace_with_git_merge_diff` tool."""
    original_content = _read_file(filepath)
    if search_block not in original_content:
        raise ValueError("Search block not found in file.")
    new_content = original_content.replace(search_block, replace_block)
    _create_file_with_block(filepath, new_content) # Use create to handle paths
    return "File content replaced successfully."

# --- Tool Dispatcher ---

TOOL_DISPATCHER = {
    'list_files': _list_files,
    'read_file': _read_file,
    'create_file_with_block': _create_file_with_block,
    'overwrite_file_with_block': _create_file_with_block, # Alias to the same function
    'delete_file': _delete_file,
    'rename_file': _rename_file,
    'run_in_bash_session': _run_in_bash_session,
    'replace_with_git_merge_diff': _replace_with_git_merge_diff,
}

# --- Main Execution Logic ---

def execute_and_log_action(tool_name: str, args_list: List[Any], task_id: str, plan_step: int):
    """
    Executes a tool by name with given arguments and logs the entire process.
    """
    logger = Logger()

    if tool_name not in TOOL_DISPATCHER:
        # For agent-facing tools not in the dispatcher, we just log the call.
        # This is a compromise for tools that we cannot re-implement here.
        log_details = {"tool_name": tool_name, "arguments": args_list, "message": "This is an agent-facing tool and is not executed by the wrapper."}
        logger.log("Phase 3", task_id, plan_step, "AGENT_TOOL_CALL", log_details, "SUCCESS")
        print(json.dumps({"status": "logged", "message": "Agent-facing tool call logged."}))
        return

    action_details = {"tool_name": tool_name, "arguments": args_list}

    logger.log("Phase 3", task_id, plan_step, "TOOL_EXEC", action_details, "IN_PROGRESS")

    try:
        tool_function = TOOL_DISPATCHER[tool_name]
        result = tool_function(*args_list)

        outcome_message = json.dumps(result) if result is not None else "Action completed successfully."
        logger.log("Phase 3", task_id, plan_step, "TOOL_EXEC", action_details, "SUCCESS", outcome_message)

        if result is not None:
            print(json.dumps(result))

    except Exception as e:
        error_details = {"message": str(e), "stack_trace": traceback.format_exc()}
        logger.log("Phase 3", task_id, plan_step, "TOOL_EXEC", action_details, "FAILURE", str(e), error_details)
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="A wrapper to execute and log tool actions.")
    parser.add_argument("--tool", required=True, help="The name of the tool to execute.")
    parser.add_argument("--args", default='[]', help="A JSON string representing the list of arguments.")
    parser.add_argument("--task-id", required=True, help="The current task ID.")
    parser.add_argument("--plan-step", required=True, type=int, help="The current plan step number.")

    args = parser.parse_args()

    try:
        args_list = json.loads(args.args)
        if not isinstance(args_list, list):
            raise ValueError("--args must be a JSON array (list).")
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({"error": f"Invalid --args format: {e}"}), file=sys.stderr)
        sys.exit(1)

    execute_and_log_action(args.tool, args_list, args.task_id, args.plan_step)

if __name__ == "__main__":
    main()