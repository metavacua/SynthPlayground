"""
This module defines the RefactoringEngine, a key component of the CRE.
It uses the RefactoringRegistry to find and execute transformations (morphisms)
between language classes.
"""

import subprocess
import argparse
import shutil
import os
import json
import sys

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.refactoring_registry import RefactoringRegistry
from utils.logger import Logger

class RefactoringEngine:
    def __init__(self, registry: RefactoringRegistry):
        self.registry = registry

    def find_and_execute(self, source_file: str, source_class: str, target_class: str) -> str:
        """
        Finds a morphism in the registry and executes the associated tool on a copy of the source file.
        """
        morphism = self.registry.find_morphism(source_class, target_class)
        if not morphism:
            raise ValueError(f"No morphism found from {source_class} to {target_class}")

        tool_path = morphism['tool']

        temp_file = source_file.replace(".py", "_temp.py")
        shutil.copy(source_file, temp_file)

        command = ["python", tool_path, temp_file]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            os.remove(temp_file)
            raise RuntimeError(f"Refactoring tool failed: {result.stderr}")

        output_path = source_file.replace(".py", "_refactored.py")
        shutil.move(temp_file, output_path)

        return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--source-class", required=True)
    parser.add_argument("--target-class", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--session-id", required=True)
    args = parser.parse_args()

    logger = Logger(session_id=args.session_id)
    action_details = {
        "tool": "refactoring_engine.py",
        "file": args.file,
        "source_class": args.source_class,
        "target_class": args.target_class
    }

    try:
        registry = RefactoringRegistry()
        registry.scan()

        engine = RefactoringEngine(registry)

        output_file = engine.find_and_execute(args.file, args.source_class, args.target_class)

        output = {"refactored_file": output_file}

        logger.log(
            phase="Phase 3",
            task_id=args.task_id,
            plan_step=2,
            action_type="TOOL_EXEC",
            action_details=action_details,
            outcome_status="SUCCESS",
            outcome_message=f"Refactored file to '{output_file}'"
        )

        print(json.dumps(output))

    except Exception as e:
        logger.log(
            phase="Execution",
            task_id=args.task_id,
            plan_step=2,
            action_type="TOOL_EXEC",
            action_details=action_details,
            outcome_status="FAILURE",
            error_details={"error": str(e)}
        )
        sys.exit(1)
