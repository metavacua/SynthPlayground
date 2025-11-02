"""
A simple plan executor for simulating agent behavior.

This script reads a plan file, parses it, and executes the commands in a
simplified, simulated environment. It supports a limited set of tools
(`message_user` and `run_in_bash_session`) to provide a basic demonstration
of how an agent would execute a plan.
"""

import subprocess
import sys
import os

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.plan_parser import parse_plan


def execute_plan(filepath: str):
    """
    Executes a plan file, simulating the agent's execution loop.

    Args:
        filepath: The path to the plan file.
    """
    try:
        with open(filepath, "r") as f:
            plan_content = f.read()

        commands = parse_plan(plan_content)

        for cmd in commands:
            tool_name = cmd.tool_name
            arguments = cmd.args_text

            print(f"Executing tool: {tool_name} with args: {arguments}")
            if tool_name == "message_user":
                print(f"[USER MESSAGE]\n{arguments}")
            elif tool_name == "run_in_bash_session":
                command_to_run = arguments
                print(f"$ {command_to_run}")
                result = subprocess.run(
                    command_to_run,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                if result.stdout:
                    print(result.stdout.strip())
                if result.stderr:
                    print(f"[STDERR]\n{result.stderr.strip()}")
            else:
                import shlex
                command_to_run = [sys.executable, tool_name] + shlex.split(arguments)
                print(f"$ {' '.join(command_to_run)}")
                result = subprocess.run(
                    command_to_run,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                if result.stdout:
                    print(result.stdout.strip())
                if result.stderr:
                    print(f"[STDERR]\n{result.stderr.strip()}")

    except FileNotFoundError:
        print(f"Error: Plan file not found at '{filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


def main():
    """
    Main function to run the plan executor from the command line.
    """
    if len(sys.argv) != 2:
        print("Usage: python tooling/plan_executor.py <plan_filepath>")
        sys.exit(1)

    plan_filepath = sys.argv[1]
    execute_plan(plan_filepath)


if __name__ == "__main__":
    main()
