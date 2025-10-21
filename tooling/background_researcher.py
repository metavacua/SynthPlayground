"""
This script performs a simulated research task in the background.
It takes a task ID as a command-line argument and writes its findings
to a temporary file that the main agent can poll.
"""

import time
import sys


def perform_research(task_id: str):
    """Simulates a research task and writes the result to a file."""
    print(f"[BackgroundResearcher] Starting research for task: {task_id}")
    # Simulate a long-running research task
    time.sleep(5)
    result_content = f"This is the research result for task {task_id}."
    result_path = f"/tmp/{task_id}.result"
    with open(result_path, "w") as f:
        f.write(result_content)
    print(f"[BackgroundResearcher] Research complete. Result written to {result_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tooling/background_researcher.py <task_id>")
        sys.exit(1)
    task_id = sys.argv[1]
    perform_research(task_id)
