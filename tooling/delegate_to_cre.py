"""
This tool serves as the formal delegation interface for the primary LLM agent
to invoke the autonomous Categorical Reasoning Engine (CRE) agent.
"""

import subprocess
import argparse
import sys

def delegate_to_cre(task_name: str, file_path: str):
    """
    Invokes the CRE agent to perform a specific, formal task.

    Args:
        task_name: The formal task for the CRE to perform (e.g., 'prove_termination').
        file_path: The path to the target file for the task.
    """
    print(f"--- Delegating task '{task_name}' for file '{file_path}' to CRE Agent ---")

    command = ["python3", "agents/cre_agent.py", task_name, file_path]

    # We use a Popen here to stream the output in real-time, which is better for
    # observing the progress of the autonomous agent.
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        # Stream stdout
        if proc.stdout:
            for line in proc.stdout:
                print(line, end='')

        # Stream stderr
        if proc.stderr:
            for line in proc.stderr:
                print(line, end='', file=sys.stderr)

    if proc.returncode != 0:
        print("\n--- Delegation failed: CRE Agent exited with an error. ---", file=sys.stderr)
    else:
        print("\n--- Delegation successful: CRE Agent completed its task. ---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Delegation interface for the CRE Agent.")
    parser.add_argument("task_name", help="The formal task to delegate (e.g., 'prove_termination').")
    parser.add_argument("file_path", help="The path to the target file for the task.")
    args = parser.parse_args()

    delegate_to_cre(args.task_name, args.file_path)
