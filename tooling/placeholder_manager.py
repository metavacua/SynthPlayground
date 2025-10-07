import argparse
import os
import re
import sys

# Regex to find structured TODOs: TODO[task-id]: Description
STRUCTURED_TODO_REGEX = re.compile(r"TODO\[([a-zA-Z0-9_-]+)\]:\s*(.*)")

# Regex to find any kind of TODO, case-insensitive
GENERIC_TODO_REGEX = re.compile(r"todo", re.IGNORECASE)

# Directories and file extensions to ignore during scans
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "env"}
IGNORE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".so",
    ".egg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
}


def scan_for_placeholders(root_dir="."):
    """
    Scans the repository for all structured placeholders and returns them.
    """
    found_placeholders = []
    for root, dirs, files in os.walk(root_dir):
        # Prune ignored directories from the walk
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if any(file.endswith(ext) for ext in IGNORE_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        for match in STRUCTURED_TODO_REGEX.finditer(line):
                            found_placeholders.append(
                                {
                                    "file": file_path,
                                    "line": line_num,
                                    "task_id": match.group(1),
                                    "description": match.group(2).strip(),
                                }
                            )
            except Exception as e:
                print(
                    f"Warning: Could not read file {file_path}. Error: {e}",
                    file=sys.stderr,
                )

    return found_placeholders


def validate_placeholders(root_dir="."):
    """
    Validates that all TODOs in the repository conform to the structured format.
    Returns a list of non-compliant TODOs.
    """
    non_compliant = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if any(file.endswith(ext) for ext in IGNORE_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        # Find any generic "todo"
                        if GENERIC_TODO_REGEX.search(line):
                            # Check if it's a valid, structured one
                            if not STRUCTURED_TODO_REGEX.search(line):
                                non_compliant.append(
                                    {
                                        "file": file_path,
                                        "line": line_num,
                                        "content": line.strip(),
                                    }
                                )
            except Exception as e:
                print(
                    f"Warning: Could not read file {file_path}. Error: {e}",
                    file=sys.stderr,
                )

    return non_compliant


def main():
    """
    Main function to run the placeholder manager CLI.
    """
    parser = argparse.ArgumentParser(
        description="A tool to scan and validate TODO placeholders in the codebase."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )

    # --- Scan command ---
    scan_parser = subparsers.add_parser("scan", help="Scans for all structured TODOs.")
    scan_parser.add_argument(
        "--root", default=".", help="The root directory to scan from."
    )

    # --- Validate command ---
    validate_parser = subparsers.add_parser(
        "validate", help="Validates that all TODOs follow the required format."
    )
    validate_parser.add_argument(
        "--root", default=".", help="The root directory to validate."
    )

    args = parser.parse_args()

    if args.command == "scan":
        print(f"Scanning '{args.root}' for structured placeholders...")
        placeholders = scan_for_placeholders(args.root)
        if not placeholders:
            print("\nNo structured placeholders found.")
        else:
            print(f"\nFound {len(placeholders)} structured placeholder(s):")
            for p in placeholders:
                print(
                    f"  - [{p['task_id']}] {p['description']} ({p['file']}:{p['line']})"
                )

    elif args.command == "validate":
        print(f"Validating placeholders in '{args.root}'...")
        non_compliant_todos = validate_placeholders(args.root)
        if not non_compliant_todos:
            print("\nValidation successful: All TODOs conform to the required format.")
            sys.exit(0)
        else:
            print(
                f"\nValidation FAILED: Found {len(non_compliant_todos)} "
                "non-compliant TODO(s):"
            )
            for todo in non_compliant_todos:
                print(f"  - {todo['file']}:{todo['line']}")
                print(f"    > {todo['content']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
