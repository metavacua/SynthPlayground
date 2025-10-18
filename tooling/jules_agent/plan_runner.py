"""
A self-executing plan runner for Jules, the AI agent.

This script reads a plan file in a specific format, executes the commands,
verifies their success, and handles failures.
"""

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Optional

# Add the repository root to the Python path to allow for absolute imports
# from the `tooling` directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from tooling.jules_agent import action_logger

# --- Data Structures ---

@dataclass
class ExecutableCommand:
    """Represents a single, parsed command from a self-executing plan."""
    tool_name: str
    args_text: str
    verification_command: Optional[str] = None
    on_failure_plan: Optional[str] = None

# --- Plan Parser ---

def parse_executable_plan(plan_content: str) -> List[ExecutableCommand]:
    """Parses the raw text of a plan into a list of ExecutableCommand objects."""
    commands = []
    plan_blocks = plan_content.strip().split("\n---\n")

    for block in plan_blocks:
        block = block.strip()
        if not block:
            continue

        # Extract the main command (tool name and args)
        command_part_match = re.search(r"^(.*?)(?:\n# VERIFICATION:|\n# ON_FAILURE:|$)", block, re.DOTALL)
        tool_name = ""
        args_text = ""
        if command_part_match:
            command_part = command_part_match.group(1).strip()
            command_lines = [line for line in command_part.split('\n') if not line.strip().startswith("#")]
            if command_lines:
                tool_name = command_lines[0].strip()
                args_text = '\n'.join(command_lines[1:]).strip()

        # Extract the verification command
        verification_command = None
        verification_match = re.search(r"\n# VERIFICATION:\n(.*?)(?:\n# ON_FAILURE:|$)", block, re.DOTALL)
        if verification_match:
            verification_command = verification_match.group(1).strip()

        # Extract the on_failure plan
        on_failure_plan = None
        on_failure_match = re.search(r"\n# ON_FAILURE:\n(.*)", block, re.DOTALL)
        if on_failure_match:
            on_failure_plan = on_failure_match.group(1).strip()

        if tool_name:
            commands.append(ExecutableCommand(
                tool_name=tool_name,
                args_text=args_text,
                verification_command=verification_command,
                on_failure_plan=on_failure_plan
            ))

    return commands

# --- Tool Definitions (Simulated) ---

def run_in_bash_session(command: str):
    """Simulates running a command in a bash session."""
    print(f"$ {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"[STDERR]\n{result.stderr.strip()}")
    return result

def message_user(message: str):
    """Simulates sending a message to the user."""
    print(f"[USER MESSAGE]\n{message}")
    return subprocess.CompletedProcess(args=message, returncode=0, stdout="", stderr="")

TOOL_REGISTRY = {
    "run_in_bash_session": run_in_bash_session,
    "message_user": message_user,
}

# --- Execution Logic ---

def execute_command(command: ExecutableCommand, cwd: str) -> bool:
    """Executes a single command and returns True on success, False on failure."""
    if command.tool_name not in TOOL_REGISTRY:
        action_logger.log_action(f"Unknown tool: {command.tool_name}", cwd)
        return False

    tool_function = TOOL_REGISTRY[command.tool_name]

    try:
        # Execute the main command
        result = tool_function(command.args_text)
        if result.returncode != 0:
            action_logger.log_action(f"Command failed: {command.tool_name} {command.args_text}", cwd)
            return False

        # Execute the verification command if it exists
        if command.verification_command:
            verification_result = run_in_bash_session(command.verification_command)
            if verification_result.returncode != 0:
                action_logger.log_action(f"Verification failed for command: {command.tool_name}", cwd)
                return False

        action_logger.log_action(f"Command succeeded: {command.tool_name}", cwd)
        return True

    except Exception as e:
        action_logger.log_action(f"An unexpected error occurred during execution: {e}", cwd)
        return False

def run_plan(plan_content: str, cwd: str):
    """Parses and executes a plan."""
    commands = parse_executable_plan(plan_content)

    for command in commands:
        success = execute_command(command, cwd)
        if not success:
            if command.on_failure_plan:
                action_logger.log_action("Executing failure plan.", cwd)
                run_plan(command.on_failure_plan, cwd)
            else:
                action_logger.log_action("Command failed and no failure plan was provided. Halting.", cwd)
                break

# --- Main ---

def main():
    """Main function to run the plan runner from the command line."""
    if len(sys.argv) != 2:
        print("Usage: python tooling/jules_agent/plan_runner.py <plan_filepath>")
        sys.exit(1)

    plan_filepath = sys.argv[1]

    try:
        with open(plan_filepath, 'r') as f:
            plan_content = f.read()

        cwd = os.path.dirname(os.path.abspath(plan_filepath))
        run_plan(plan_content, cwd)

    except FileNotFoundError:
        print(f"Error: Plan file not found at '{plan_filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
