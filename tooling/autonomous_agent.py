"""
This module provides functionality for...
"""

import argparse
import json
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tooling.plan_parser import parse_plan
from tooling.plan_generator import generate_plan
from tooling.autonomous_agent_logic import generate_command_from_plan_step

class AutonomousAgent:
    def __init__(self, task):
        self.task = task
        self.plan = None

    def generate_plan(self):
        """Generates a plan to accomplish the task."""
        self.plan = generate_plan(self.task)

    def execute_plan(self):
        """Executes the generated plan."""
        if not self.plan:
            print("No plan to execute.")
            return

        commands = parse_plan(self.plan)
        outputs = {}

        for cmd in commands:
            command_to_run = generate_command_from_plan_step(cmd, outputs)

            if not command_to_run:
                print(f"Unknown tool: {cmd.tool_name}")
                continue

            print(f"$ {command_to_run}")
            result = subprocess.run(
                command_to_run,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.stdout:
                try:
                    output_json = json.loads(result.stdout)
                    for key, value in output_json.items():
                        outputs[key] = value
                except json.JSONDecodeError:
                    pass # Not all tools will output JSON.

                print(result.stdout.strip())
            if result.stderr:
                print(f"[STDERR]\n{result.stderr.strip()}")

    def run(self):
        """Runs the agent's main loop."""
        print(f"Starting agent with task: {self.task}")
        self.generate_plan()
        self.execute_plan()
        print("Agent has completed its task.")

def main():
    parser = argparse.ArgumentParser(description="An autonomous agent for repository development.")
    parser.add_argument("task", help="The high-level task for the agent to perform.")
    args = parser.parse_args()

    agent = AutonomousAgent(args.task)
    agent.run()

if __name__ == "__main__":
    main()
