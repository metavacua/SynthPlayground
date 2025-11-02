"""
This module defines the RefactoringEngine, a key component of the CRE.
It uses the RefactoringRegistry to find and execute transformations (morphisms)
between language classes.
"""

import subprocess
import argparse
import shutil
import os
from tooling.refactoring_registry import RefactoringRegistry

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

        # Create a temporary copy of the source file to ensure the original is not modified.
        temp_file = source_file.replace(".py", "_temp.py")
        shutil.copy(source_file, temp_file)

        command = ["python", tool_path, temp_file]
        print(f"Executing refactoring: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            # Clean up the temporary file on failure
            os.remove(temp_file)
            raise RuntimeError(f"Refactoring tool failed: {result.stderr}")

        # The tool modifies the temp_file in-place. We rename it to the final output path.
        output_path = source_file.replace(".py", "_refactored.py")
        shutil.move(temp_file, output_path)

        return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--source-class", required=True)
    parser.add_argument("--target-class", required=True)
    args = parser.parse_args()

    # Add the repository root to the Python path for imports
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    registry = RefactoringRegistry()
    registry.scan()

    engine = RefactoringEngine(registry)

    output_file = engine.find_and_execute(args.file, args.source_class, args.target_class)

    print(f"Refactoring complete. Output written to {output_file}")
