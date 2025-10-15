"""
A tool for performing automated symbol renaming in Python code.

This script provides a command-line interface to find and rename a symbol
(a function or class) and all of its references throughout the repository.

It works in three stages:
1.  **Definition Finding:** It uses Abstract Syntax Trees (AST) to locate the
    exact definition of the target symbol in its source file.
2.  **Reference Finding:** It performs a text-based search across the repository
    to find all files that mention the symbol.
3.  **Plan Generation:** It generates a refactoring plan, which is a sequence of
    `replace_with_git_merge_diff` commands. This plan can be executed by the
    agent's master controller to apply the changes in a controlled and
    verifiable way. The path to this generated plan file is printed to stdout.
"""
import argparse
import ast
import os
import sys
import tempfile


def find_symbol_definition(filepath, symbol_name):
    """Finds the definition of a symbol in a Python file."""
    with open(filepath, "r") as f:
        content = f.read()
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and node.name == symbol_name
        ):
            return node
    return None


def find_references(symbol_name, search_path):
    """Finds all files in a directory that reference a given symbol."""
    references = []
    for root, _, files in os.walk(search_path):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", errors="ignore") as f:
                        if symbol_name in f.read():
                            references.append(filepath)
                except Exception:
                    pass  # Ignore files that can't be read
    return references


def main():
    parser = argparse.ArgumentParser(
        description="A simple refactoring tool to rename a symbol in a Python file."
    )
    parser.add_argument(
        "--filepath",
        required=True,
        help="The path to the file where the symbol is defined.",
    )
    parser.add_argument(
        "--old-name", required=True, help="The current name of the symbol to rename."
    )
    parser.add_argument(
        "--new-name", required=True, help="The new name for the symbol."
    )
    parser.add_argument(
        "--search-path",
        default=".",
        help="The root directory to search for references.",
    )

    args = parser.parse_args()

    # Find the definition of the symbol
    definition = find_symbol_definition(args.filepath, args.old_name)
    if not definition:
        print(
            f"Error: Symbol '{args.old_name}' not found in {args.filepath}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Find all references to the symbol
    reference_files = find_references(args.old_name, args.search_path)
    if args.filepath not in reference_files:
        reference_files.append(args.filepath)

    # Generate a plan to rename the symbol in all referenced files
    plan_content = ""
    for ref_file in set(reference_files):
        with open(ref_file, "r") as f:
            original_content = f.read()

        if args.old_name not in original_content:
            continue

        new_content = original_content.replace(args.old_name, args.new_name)

        diff_content = f"""\
<<<<<<< SEARCH
{original_content}
=======
{new_content}
>>>>>>> REPLACE
"""
        plan_content += f"""\
replace_with_git_merge_diff
{ref_file}
{diff_content}

"""
    # Write the plan to a temporary file
    fd, plan_path = tempfile.mkstemp(suffix=".plan.txt", text=True)
    with os.fdopen(fd, "w") as tmp:
        tmp.write(plan_content)

    print(plan_path)


if __name__ == "__main__":
    main()
