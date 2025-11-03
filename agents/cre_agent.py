"""
This script is the primary entry point for the autonomous Categorical Reasoning Engine (CRE) agent.
It now features an upgraded cognitive cycle with true decision-making, allowing it to
choose between formal transformations and delegation to external tools.
"""

import subprocess
import argparse
import sys
import os
import json
from tooling.witness_registry import WitnessRegistry
from tooling.refactoring_registry import RefactoringRegistry
from tooling.tool_registry import ToolRegistry
from tooling.problem_classifier import classify_file
from tooling.refactoring_engine import RefactoringEngine
from tooling.proof_synthesizer import ProofSynthesizer
from logic_system.functor import CorrespondenceFunctor

from utils.logger import Logger
import uuid

class CRE_Agent:
    def __init__(self, task_name: str, file_path: str, task_id: str, session_id: str):
        self.task_name = task_name
        self.file_path = file_path
        self.task_id = task_id
        self.session_id = session_id
        self.logger = Logger()
        self.logger.session_id = session_id

        self.witness_registry = WitnessRegistry()
        self.refactoring_registry = RefactoringRegistry()
        self.tool_registry = ToolRegistry()

        self.witness_registry.scan()
        self.refactoring_registry.scan()
        self.tool_registry.scan()

        self.refactoring_engine = RefactoringEngine(self.refactoring_registry)

    def run(self):
        print(f"--- CRE Agent: Initializing for task '{self.task_id}' ---")
        try:
            self._run_cognitive_cycle()
            print(f"--- CRE Agent: Task '{self.task_id}' completed successfully. ---")
        except Exception as e:
            print(f"--- CRE Agent: Task '{self.task_id}' failed: {e} ---", file=sys.stderr)
            raise

    def _run_cognitive_cycle(self):
        print("\nStep 1: Classifying problem...")
        classification = self._classify_problem(self.file_path)
        source_class = classification.get('classification_name')
        problem_type = classification.get('problem_type')
        print(f"  - Classified artifact. Class: '{source_class}', Problem: '{problem_type}'")

        if self.task_name == 'prove_termination':
            target_class = "Recursive Languages"
            morphism = self.refactoring_registry.find_morphism(source_class, target_class)
            if morphism:
                print("\nDecision: Formal transformation path found for termination. Executing morphism.")
                self._execute_formal_transformation(source_class, target_class, 'termination')
            else:
                raise NotImplementedError(f"No available morphism for termination from class: {source_class}")

        elif self.task_name == 'prove_purity':
            if problem_type == "Impurity Detected":
                target_class = "Pure Functions"
                morphism = self.refactoring_registry.find_morphism(source_class, target_class)
                if morphism:
                    print("\nDecision: Impurity detected. Executing purity refactoring morphism.")
                    self._execute_formal_transformation(source_class, target_class, 'purity')
                else:
                    raise RuntimeError(f"An impurity was detected, but no refactoring morphism was found to transform '{source_class}' to '{target_class}'. This is a solvable failure.")
            else:
                print("\nDecision: No impurity detected. Proceeding directly to proof.")
                self._execute_proof_synthesis("Pure Functions", 'purity', self.file_path)

        elif self.task_name == 'dialogue' or problem_type == "Natural Language Task":
            print("\nDecision: No formal transformation path. Searching for a capable tool.")
            self._delegate_to_tool("Natural Language Processing")

        else:
            raise NotImplementedError(f"No cognitive cycle path defined for task '{self.task_name}' and problem type '{problem_type}'")

        print("\nCognitive cycle complete.")

    def _classify_problem(self, file_path: str) -> dict:
        result = self._run_command(
            ["python3", "tooling/problem_classifier.py", "--file", file_path, "--task-id", self.task_id, "--task-name", self.task_name, "--session-id", self.session_id],
            capture_output=True
        )
        return json.loads(result)

    def _execute_formal_transformation(self, source_class: str, target_class: str, property_to_prove: str):
        print("  - Invoking Refactoring Engine...")
        refactoring_result = self._run_command(
            ["python3", "tooling/refactoring_engine.py", "--source-class", source_class, "--target-class", target_class, "--file", self.file_path, "--task-id", self.task_id, "--session-id", self.session_id],
            capture_output=True
        )
        refactored_file = json.loads(refactoring_result)['refactored_file']
        print(f"    - Refactored artifact to '{refactored_file}'")

        self._execute_proof_synthesis(target_class, property_to_prove, refactored_file)

    def _execute_proof_synthesis(self, lang_class: str, property_to_prove: str, file_path: str):
        print("  - Invoking Proof Synthesizer...")
        self._run_command(
            ["python3", "tooling/proof_synthesizer.py", "--lang-class-name", lang_class, "--property", property_to_prove, "--file", file_path, "--task-id", self.task_id, "--session-id", self.session_id]
        )
        print(f"    - Synthesized {property_to_prove} proof for '{file_path}'")

    def _delegate_to_tool(self, capability: str):
        print(f"  - Searching for a tool with capability: '{capability}'...")
        tool = self.tool_registry.find_tool_by_capability(capability)

        if not tool:
            raise RuntimeError(f"No tool found with the required capability: {capability}")

        print(f"    - Found tool: '{tool['name']}'.")

        # Prepare the command. The file_path is a common argument.
        command = [
            "python3",
            tool['tool'],
            "Refactor this function to be more efficient by using a memoization cache.",
            "--session-id", self.session_id
        ]

        print("  - Executing delegated tool...")
        self._run_command(command)
        print(f"    - Tool '{tool['name']}' executed successfully.")

    def _run_command(self, command: list, capture_output: bool = False):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {' '.join(command)}. STDERR: {result.stderr.strip()}")
        if not capture_output and result.stdout:
            print(result.stdout.strip())
        return result.stdout.strip() if capture_output else None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Autonomous Categorical Reasoning Engine Agent")
    parser.add_argument("task_name", help="The formal task to perform (e.g., 'prove_termination').")
    parser.add_argument("file_path", help="The path to the target file for the task.")
    parser.add_argument("--task-id", required=False, help="The overarching task ID, provided by a parent agent.")
    parser.add_argument("--session-id", required=False, help="The session ID, provided by a parent agent.")
    args = parser.parse_args()

    task_id = args.task_id if args.task_id else f"cre_{args.task_name}_{os.path.basename(args.file_path)}"
    session_id = args.session_id if args.session_id else str(uuid.uuid4())

    agent = CRE_Agent(args.task_name, args.file_path, task_id, session_id)
    agent.run()
