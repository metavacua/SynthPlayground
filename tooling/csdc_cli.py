import argparse
import sys
import os

# Adjusting the path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.fdc_cli import analyze_plan
from tooling.master_control import MasterControlGraph

def main():
    parser = argparse.ArgumentParser(
        description="A tool to manage the Context-Sensitive Development Cycle (CSDC)."
    )
    parser.add_argument(
        "plan_file", help="The path to the plan file to validate."
    )
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
    analysis_results = analyze_plan(args.plan_file, return_results=True)

    if analysis_results["complexity_class"] != args.complexity:
        print(
            f"Error: Plan complexity mismatch. Expected '{args.complexity}', but found '{analysis_results['complexity_class']}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Complexity check passed: Plan is in class {analysis_results['complexity_class']}.")

    print(f"\n--- CSDC: Validating plan against Model {args.model} ---")

    try:
        with open(args.plan_file, "r") as f:
            plan_content = f.read()
    except FileNotFoundError:
        print(f"Error: Plan file not found at {args.plan_file}", file=sys.stderr)
        sys.exit(1)

    validator = MasterControlGraph()
    is_valid, error_message = validator.validate_plan_for_model(plan_content, args.model)

    if is_valid:
        print("\nValidation successful! Plan is valid for the specified model and complexity.")
    else:
        print(f"\nValidation failed: {error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()