"""
A tool for performing static analysis on a Python file to understand its context.

This script provides a "contextual awareness" scan of a specified Python file
to help an agent (or a human) understand its role, dependencies, and connections
within a larger codebase. This is crucial for planning complex changes or
refactoring efforts, as it provides a snapshot of the potential impact of
modifying a file.

The scanner performs three main functions:
1.  **Symbol Definition Analysis:** It uses Python's Abstract Syntax Tree (AST)
    module to parse the target file and identify all the functions and classes
    that are defined within it.
2.  **Import Analysis:** It also uses the AST to find all modules and symbols
    that the target file imports, revealing its dependencies on other parts of
    the codebase or external libraries.
3.  **Reference Finding:** It performs a repository-wide search to find all other
    files that reference the symbols defined in the target file. This helps to
    understand how the file is used by the rest of the system.

The final output is a detailed JSON report containing all of this information,
which can be used as a foundational artifact for automated planning or human review.
"""

import argparse
import json
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.file_system_utils import find_files
from tooling.context_awareness_scanner_logic import analyze_python_file, generate_report


def find_references(symbol_name, search_path):
    """Finds all files in a directory that reference a given symbol."""
    references = []
    python_files = find_files("*.py", base_dir=search_path)
    for file in python_files:
        filepath = os.path.join(search_path, file)
        try:
            with open(filepath, "r", errors="ignore") as f:
                if symbol_name in f.read():
                    references.append(filepath)
        except Exception:
            pass  # Ignore files that can't be read
    return references


def main():
    parser = argparse.ArgumentParser(
        description="Scans a file to determine its contextual awareness within the repository."
    )
    parser.add_argument("filepath", help="The path to the file to scan.")
    parser.add_argument(
        "--search-path",
        default=".",
        help="The root directory to search for references.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        sys.exit(1)

    target_file = args.filepath
    search_path = args.search_path

    print(f"Scanning {target_file}...")

    # 1. Get file content
    with open(target_file, "r") as f:
        content = f.read()

    # 2. Analyze the file
    defined_symbols, imported_symbols = analyze_python_file(content)

    # 3. Find references to the defined symbols
    for symbol in defined_symbols:
        symbol["references"] = find_references(symbol["name"], search_path)

    # 4. Generate the report
    report = generate_report(target_file, content, defined_symbols, imported_symbols)

    output_filename = f"{os.path.basename(target_file)}.json"
    with open(output_filename, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report generated: {output_filename}")


if __name__ == "__main__":
    main()
