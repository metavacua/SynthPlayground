"""
Performs static analysis on a Python file to map its contextual role.

This script acts as a code intelligence tool. Given a Python file, it performs
a static analysis to understand its connections to the rest of the codebase.
It generates a detailed JSON report that includes:

1.  **Defined Symbols:** All functions and classes defined within the target file,
    along with their line numbers.
2.  **Imported Symbols:** All modules and symbols that the target file imports
    from other modules.
3.  **Cross-Repository References:** For each function and class defined in the
    target file, it finds all other Python files in the repository that
    reference that symbol.

The resulting report provides a comprehensive "contextual awareness map" for a
single file, showing what it provides to the system and what it consumes from
it. This is invaluable for understanding the impact of potential changes.
"""
import argparse
import ast
import json
import os
import sys


def get_defined_symbols(filepath):
    """Parses a Python file to find all defined functions and classes."""
    with open(filepath, "r") as f:
        content = f.read()

    tree = ast.parse(content)
    symbols = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            symbols.append(
                {"type": "function", "name": node.name, "lineno": node.lineno}
            )
        elif isinstance(node, ast.ClassDef):
            symbols.append({"type": "class", "name": node.name, "lineno": node.lineno})
    return symbols


def get_imported_symbols(filepath):
    """Parses a Python file to find all imported modules and symbols."""
    with open(filepath, "r") as f:
        content = f.read()

    tree = ast.parse(content)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {"type": "module", "name": alias.name, "lineno": node.lineno}
                )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or "."
            for alias in node.names:
                imports.append(
                    {
                        "type": "symbol",
                        "name": f"{module}.{alias.name}",
                        "lineno": node.lineno,
                    }
                )
    return imports


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

    # 2. Get defined symbols
    defined_symbols = get_defined_symbols(target_file)

    # 3. Get imported symbols
    imported_symbols = get_imported_symbols(target_file)

    # 4. Find references to the defined symbols
    for symbol in defined_symbols:
        symbol["references"] = find_references(symbol["name"], search_path)

    report = {
        "file_path": target_file,
        "content": content,
        "defined_symbols": defined_symbols,
        "imported_symbols": imported_symbols,
    }

    output_filename = f"{os.path.basename(target_file)}.json"
    with open(output_filename, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report generated: {output_filename}")


if __name__ == "__main__":
    main()
