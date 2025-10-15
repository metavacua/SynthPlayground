"""
This script provides a simple, automated refactoring tool for renaming symbols.

It is designed to be used from the command line to rename a Python function or
class and all of its references throughout the repository.

The process is as follows:
1.  **Find Definition:** It first locates the definition of the target symbol
    (the "old name") in the specified file.
2.  **Find References:** It then searches the entire repository for any files
    that mention the old name.
3.  **Generate Plan:** For each file where the name is found, it generates a
    `replace_with_git_merge_diff` command. This command encapsulates the change
    from the old content to the new content (with the name replaced).
4.  **Output Plan File:** It writes all these commands into a single, temporary
    plan file.

The path to this generated plan file is printed to standard output. The agent's
master controller can then be instructed to execute this plan, applying the
refactoring changes in a controlled and verifiable way.
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