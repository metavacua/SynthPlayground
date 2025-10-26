"""
A tool for managing the complexity of the codebase by orchestrating various analysis and refactoring tools.
"""

import argparse
import os
import subprocess
import json


def main():
    parser = argparse.ArgumentParser(
        description="Orchestrates complexity analysis and refactoring tools."
    )
    parser.add_argument("filepath", help="The path to the file to analyze.")
    parser.add_argument(
        "--refactor",
        action="store_true",
        help="Attempt to refactor the file to reduce complexity.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}")
        return

    udc_filepath = os.path.splitext(args.filepath)[0] + ".udc"

    print(f"Converting {args.filepath} to {udc_filepath}...")
    subprocess.run(["python", "tooling/py_to_udc.py", args.filepath])

    print(f"Analyzing {udc_filepath} for termination risk...")
    result = subprocess.run(
        [
            "python",
            "tooling/halting_heuristic_analyzer.py",
            udc_filepath,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error running halting heuristic analyzer: {result.stderr}")
        return

    try:
        analysis = json.loads(result.stdout)
        print(json.dumps(analysis, indent=2))

        if args.refactor and analysis["estimated_risk"] in ["MEDIUM", "HIGH"]:
            print("Attempting to refactor the file...")
            # Attempt to refactor using the "add fuel" strategy
            subprocess.run(
                [
                    "python",
                    "tooling/refactor_add_fuel.py",
                    args.filepath,
                ]
            )
            print("Refactoring complete.")

    except json.JSONDecodeError:
        print(f"Error parsing analysis output: {result.stdout}")


if __name__ == "__main__":
    main()
