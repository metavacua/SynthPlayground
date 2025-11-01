import argparse
import json
import os
import subprocess


def classify_ast(ast_file):
    """Classifies a single AST file and returns the result."""
    command = ["python3", "-m", "language_theory.toolchain.classifier", ast_file]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error classifying {ast_file}: {result.stderr}"

    # Extract the classification from the output
    for line in result.stdout.splitlines():
        if line.startswith("Result:"):
            return line.split(":", 1)[1].strip()
    return "Classification not found"


def main():
    """
    Scans the repository's ASTs, classifies them, and generates a report.
    """
    parser = argparse.ArgumentParser(
        description="Classifies all source code in the repository."
    )
    parser.add_argument(
        "--ast-dir",
        default="knowledge_core/asts",
        help="The directory containing the generated ASTs.",
    )
    parser.add_argument(
        "--output-file",
        default="knowledge_core/source_classification_report.json",
        help="The file to save the classification report to.",
    )
    args = parser.parse_args()

    report = {}
    for root, _, files in os.walk(args.ast_dir):
        for file in files:
            if file.endswith(".json"):
                ast_path = os.path.join(root, file)
                source_path = os.path.relpath(ast_path, args.ast_dir)[
                    :-5
                ]  # Remove .json
                classification = classify_ast(ast_path)
                report[source_path] = classification

    with open(args.output_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Classification report generated at {args.output_file}")


if __name__ == "__main__":
    main()
