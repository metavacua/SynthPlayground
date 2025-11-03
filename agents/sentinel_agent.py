"""
This script defines the Sentinel Agent, a high-level autonomous agent designed
for anti-fragility. It uses the Categorical Reasoning Engine (CRE) as its
core "Brain" for formal reasoning and task execution.
"""

import argparse
import sys
import os
import subprocess
import re

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.cre_agent import CRE_Agent
from tooling.tool_registry import ToolRegistry

import uuid

class SentinelAgent:
    def __init__(self, task_name: str, file_path: str):
        self.task_name = task_name
        self.file_path = file_path
        self.task_id = f"sentinel_{task_name}_{os.path.basename(file_path)}"
        self.session_id = str(uuid.uuid4())
        self.brain = CRE_Agent(task_name, file_path, task_id=self.task_id, session_id=self.session_id)
        self.tool_registry = ToolRegistry()
        self.tool_registry.scan()

    def run(self):
        """
        Executes the agent's main loop with an anti-fragility mechanism.
        """
        print(f"--- Sentinel Agent: Activating for task '{self.task_id}' ---")

        try:
            self._start_fdc()
            self.brain.run()
            print(f"--- Sentinel Agent: Task '{self.task_id}' completed successfully. ---")
        except Exception as e:
            print(f"\n--- Sentinel Agent: An error was encountered! ---", file=sys.stderr)
            print(f"Error: {e}", file=sys.stderr)
            print("--- Initiating Anti-Fragility Protocol... ---")
        finally:
            # Always generate a post-mortem and attempt lesson compilation
            self._generate_postmortem_and_compile_lesson()

    def _start_fdc(self):
        """Initiates the FDC using the repository's formal CLI."""
        print("\nStep 1: Initiating FDC...")
        self._run_command(["python3", "tooling/fdc_cli.py", "start", "--task-id", self.task_id, "--session-id", self.session_id])

    def _generate_postmortem_and_compile_lesson(self):
        """
        Generates a post-mortem and, if it exists, compiles a lesson from it.
        """
        print("\nStep 2: Generating Post-Mortem and Compiling Lessons...")
        postmortem_path = None
        try:
            postmortem_path = self._run_command(
                ["python3", "tooling/postmortem_generator.py", "--task-id", self.task_id, "--session-id", self.session_id],
                capture_output=True
            )
            if postmortem_path:
                print(f"  - Post-mortem generated at: {postmortem_path}")
            else:
                print("  - No post-mortem was generated (no task events found).")
                return # No further action needed
        except Exception as e:
            print(f"!!! Warning: Post-mortem generation failed: {e} !!!", file=sys.stderr)
            return # Cannot proceed if generation fails

        # If a report was created, attempt to compile lessons
        try:
            compiler_tool = self.tool_registry.find_tool_by_capability("Extract Lesson from Failure")
            if not compiler_tool:
                raise RuntimeError("Could not find the 'Extract Lesson from Failure' tool.")

            print("  - Compiling lessons from post-mortem...")
            self._run_command([
                "python3", compiler_tool['tool'], "--source-path", postmortem_path
            ])
            print("  - Lesson compilation complete.")
        except Exception as e:
            print(f"!!! Warning: Lesson compilation failed: {e} !!!", file=sys.stderr)

    def _run_command(self, command: list, capture_output: bool = False) -> str:
        """Helper to run a subprocess and check for errors."""
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {' '.join(command)}. STDERR: {result.stderr.strip()}")
        if not capture_output:
            print(result.stdout.strip())
        return result.stdout.strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Autonomous Sentinel Agent")
    parser.add_argument("task_name", help="The formal task to perform (e.g., 'prove_purity').")
    parser.add_argument("file_path", help="The path to the target file for the task.")
    args = parser.parse_args()

    agent = SentinelAgent(args.task_name, args.file_path)
    agent.run()
