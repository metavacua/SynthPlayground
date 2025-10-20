import argparse
import json
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tooling.plan_parser import parse_plan
from tooling.plan_generator import generate_plan

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
            tool_name = cmd.tool_name
            arguments = cmd.args_text

            # Substitute outputs from previous steps.
            for key, value in outputs.items():
                arguments = arguments.replace(f"<{key}>", value)

            if tool_name == "run_in_bash_session":
                command_to_run = arguments
            elif tool_name == "refactor":
                command_to_run = f"python3 tooling/refactor.py {arguments}"
            elif tool_name == "create_file":
                command_to_run = f"python3 tooling/custom_tools/create_file.py {arguments}"
            elif tool_name == "read_file":
                command_to_run = f"python3 tooling/custom_tools/read_file.py {arguments}"
            elif tool_name == "fetch_data":
                command_to_run = f"python3 tooling/custom_tools/fetch_data.py {arguments}"
            elif tool_name == "analyze_data":
                command_to_run = f"python3 tooling/custom_tools/analyze_data.py {arguments}"
            else:
                print(f"Unknown tool: {tool_name}")
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
