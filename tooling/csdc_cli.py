"""
This script provides a command-line interface for the Context-Sensitive Development Cycle (CSDC).
"""

import argparse
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tooling.fdc_cli import analyze_plan

class LBAValidator:
    """
    A Linear Bounded Automaton for validating plans against CSDC models.
    """
    def __init__(self, model):
        self.model = model

    def validate(self, plan_content):
        """
        Validates a plan against the CSDC model.
        """
        lines = plan_content.split('\n')
        for line in lines:
            if self.model == "A":
                if "define_diagonalization_function" in line:
                    return False, "Model A forbids 'define_diagonalization_function'"
            elif self.model == "B":
                if "define_set_of_names" in line:
                    return False, "Model B forbids 'define_set_of_names'"
        return True, ""

def main():
    parser = argparse.ArgumentParser(description="CSDC Plan Validator.")
    parser.add_argument("plan_file", help="The path to the plan file to validate.")
    parser.add_argument("--model", required=True, choices=["A", "B"], help="The CSDC model to validate against.")
    parser.add_argument("--complexity", required=True, choices=["P", "EXP"], help="The required complexity class.")
    args = parser.parse_args()

    if not os.path.exists(args.plan_file):
        print(f"Error: Plan file not found at {args.plan_file}", file=sys.stderr)
        sys.exit(1)

    # 1. Analyze Complexity
    analysis = analyze_plan(args.plan_file, return_results=True)
    if analysis["complexity_class"] != args.complexity:
        print(f"Error: Complexity mismatch. Plan is {analysis['complexity_class']}, required {args.complexity}.", file=sys.stderr)
        sys.exit(1)

    # 2. Validate against Model
    with open(args.plan_file, "r") as f:
        plan_content = f.read()
    validator = LBAValidator(args.model)
    is_valid, error_msg = validator.validate(plan_content)
    if not is_valid:
        print(f"Error: Model validation failed. {error_msg}", file=sys.stderr)
        sys.exit(1)

    print("Validation successful!")

if __name__ == "__main__":
    main()
