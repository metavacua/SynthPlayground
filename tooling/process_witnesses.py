"""
This module provides functionality for...
"""

import argparse
import os
import subprocess
import sys

def run_command(command):
    """Runs a command and prints its output."""
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    result.check_returncode()

def main():
    """
    Processes a witness file through the language theory and knowledge management toolchains.
    """
    parser = argparse.ArgumentParser(
        description="Processes a witness file through the toolchains."
    )
    parser.add_argument("witness_file", help="Path to the witness file to process.")
    args = parser.parse_args()

    witness_file = args.witness_file
    witness_name = os.path.splitext(os.path.basename(witness_file))[0]
    ast_file = f"knowledge_core/asts/{witness_file}.json"

    # --- Language Theory Toolchain ---
    print("--- Running Language Theory Toolchain ---")

    # 1. Generate AST
    print("\n--- Generating AST ---")
    run_command(["python3", "tooling/builder.py", "--target", "ast-generate"])

    # 2. Classify
    print("\n--- Classifying Grammar ---")
    run_command(["python3", "-m", "language_theory.toolchain.classifier", ast_file])

    # 3. Analyze Complexity
    print("\n--- Analyzing Complexity ---")
    run_command(["python3", "-m", "language_theory.toolchain.complexity", witness_name])

    # 4. Refactor (if applicable)
    if witness_name == "v_theory_decider":
        print("\n--- Refactoring ---")
        run_command(["python3", "-m", "language_theory.toolchain.refactor", witness_file, "decider_generator"])

    # --- Knowledge Management Toolchain ---
    print("\n--- Running Knowledge Management Toolchain ---")
    run_command(["python3", "tooling/builder.py", "--target", "knowledge-integrate"])

    print("\n--- Witness Processing Complete ---")

if __name__ == "__main__":
    main()
