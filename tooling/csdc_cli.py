"""
A command-line tool for managing the Context-Sensitive Development Cycle (CSDC).

This script provides an interface to validate a development plan against a specific
CSDC model (A or B) and a given complexity class (P or EXP). It ensures that a
plan adheres to the strict logical and computational constraints defined by the
CSDC protocol before it is executed.

The tool performs two main checks:
1.  **Complexity Analysis:** It analyzes the plan to determine its computational
    complexity and verifies that it matches the expected complexity class.
2.  **Model Validation:** It validates the plan's commands against the rules of
    the specified CSDC model, ensuring that it does not violate any of the
    model's constraints (e.g., forbidding certain functions).

This serves as a critical gateway for ensuring that all development work within
the CSDC framework is sound, predictable, and compliant with the governing
meta-mathematical principles.
"""

import argparse
import sys
import os

# Adjusting the path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.fdc_cli import analyze_plan
from tooling.csdc_logic import validate_plan
from tooling.master_control import MasterControlGraph


def main():
    parser = argparse.ArgumentParser(
        description="A tool to manage the Context-Sensitive Development Cycle (CSDC)."
    )
    parser.add_argument("plan_file", help="The path to the plan file to validate.")
    parser.add_argument(
        "--model",
        required=True,
        choices=["A", "B"],
        help="The development model to use for validation (A or B).",
    )
    parser.add_argument(
        "--complexity",
        required=True,
        choices=["P", "EXP"],
        help="The expected complexity class of the plan (P for Polynomial, EXP for Exponential).",
    )

    args = parser.parse_args()

    print(f"--- CSDC: Analyzing plan '{args.plan_file}' ---")

    try:
        with open(args.plan_file, "r") as f:
            plan_content = f.read()
    except FileNotFoundError:
        print(f"Error: Plan file not found at {args.plan_file}", file=sys.stderr)
        sys.exit(1)

    analysis_results = analyze_plan(args.plan_file, return_results=True)

    is_valid, error_message = validate_plan(
        plan_content, args.model, args.complexity, analysis_results
    )

    if is_valid:
        print(
            "\nValidation successful! Plan is valid for the specified model and complexity."
        )
    else:
        print(f"\nValidation failed: {error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
