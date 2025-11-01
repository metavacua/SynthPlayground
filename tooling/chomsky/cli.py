"""
A unified command-line interface for the Chomsky toolchain.

This script provides a single entry point for all the tools related to the
Chomsky hierarchy and decidability. It orchestrates the functionality of the
various components of the toolchain, such as the code analyzer and the
refactoring tools, providing a clear and contextually visible interface for
both human and agentic use.
"""

import argparse
import json
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from tooling.chomsky.analyzer import CodeAnalyzer
from tooling.chomsky.refactor import CodeRefactorer
from tooling.chomsky.lba_validator import LBAValidator
from tooling.chomsky import refactor_cs_to_cf, refactor_cf_to_r
from tooling.fdc_cli import analyze_plan


def analyze_file(filepath):
    """
    Analyzes a Python file and prints the results.
    """
    with open(filepath, "r") as f:
        source_code = f.read()

    analyzer = CodeAnalyzer(source_code)
    analysis = analyzer.analyze()

    print(json.dumps(analysis, indent=2))


def refactor_file(filepath, strategy):
    """
    Refactors a Python file using a specified strategy.
    """
    if strategy == "general-to-primitive":
        with open(filepath, "r") as f:
            source_code = f.read()
        refactorer = CodeRefactorer(source_code)
        new_source = refactorer.refactor_to_decidable()
        print(new_source)
    elif strategy == "cs-to-cf":
        refactor_cs_to_cf.main([filepath])
    elif strategy == "cf-to-r":
        refactor_cf_to_r.main([filepath])
    else:
        print(f"Error: Unknown refactoring strategy '{strategy}'", file=sys.stderr)
        sys.exit(1)


def validate_plan_file(filepath, model, complexity):
    """
    Validates a plan file against a CSDC model and complexity.
    """
    with open(filepath, "r") as f:
        plan_content = f.read()

    analysis_results = analyze_plan(filepath, return_results=True)

    if analysis_results["complexity_class"] != complexity:
        print(
            f"Validation failed: Plan complexity mismatch. Expected '{complexity}', but found '{analysis_results['complexity_class']}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    validator = LBAValidator()
    is_valid, error_message = validator.validate(plan_content, model)

    if is_valid:
        print(
            "Validation successful! Plan is valid for the specified model and complexity."
        )
    else:
        print(f"Validation failed: {error_message}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="A toolchain for analyzing and refactoring Python code based on the Chomsky hierarchy."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'analyze' command
    parser_analyze = subparsers.add_parser("analyze", help="Analyze a Python file.")
    parser_analyze.add_argument(
        "filepath", help="The path to the Python file to analyze."
    )

    # 'refactor' command
    parser_refactor = subparsers.add_parser(
        "refactor", help="Refactor a Python file using a specific strategy."
    )
    parser_refactor.add_argument(
        "filepath", help="The path to the Python file to refactor."
    )
    parser_refactor.add_argument(
        "--strategy",
        required=True,
        choices=["general-to-primitive", "cs-to-cf", "cf-to-r"],
        help="The refactoring strategy to use.",
    )

    # 'validate-plan' command
    parser_validate = subparsers.add_parser(
        "validate-plan", help="Validate a plan against a CSDC model."
    )
    parser_validate.add_argument(
        "filepath", help="The path to the plan file to validate."
    )
    parser_validate.add_argument(
        "--model", required=True, choices=["A", "B"], help="The CSDC model to use."
    )
    parser_validate.add_argument(
        "--complexity",
        required=True,
        choices=["P", "EXP"],
        help="The expected complexity class.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_file(args.filepath)
    elif args.command == "refactor":
        refactor_file(args.filepath, args.strategy)
    elif args.command == "validate-plan":
        validate_plan_file(args.filepath, args.model, args.complexity)


if __name__ == "__main__":
    main()
