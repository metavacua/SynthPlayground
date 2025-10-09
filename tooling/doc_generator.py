import ast
import os
from typing import List, Dict, Optional

# Directories to scan for Python source files.
SCAN_DIRECTORIES = ["tooling/", "utils/"]
# The output file for the generated documentation.
OUTPUT_FILE = "knowledge_core/SYSTEM_DOCUMENTATION.md"
# The title of the generated documentation.
DOC_TITLE = "# System Documentation"


def find_python_files(directories: List[str]) -> List[str]:
    """Finds all Python files in the given directories."""
    py_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))
    return sorted(py_files)


def extract_docstring(filepath: str) -> Optional[str]:
    """
    Extracts the module-level docstring from a Python file by manually parsing
    the Abstract Syntax Tree (AST). This is more reliable than ast.get_docstring
    in some environments.

    Args:
        filepath: The path to the Python file.

    Returns:
        The docstring as a string, or None if no docstring is found.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)

            # The docstring is the 'value' of the first 'Expr' node in the module body.
            if not (tree.body and isinstance(tree.body[0], ast.Expr)):
                return None

            value = tree.body[0].value

            # In modern Python (3.8+), the docstring is a Constant.
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                return value.value

            # In older Python versions, it was a Str node.
            # This is included for compatibility.
            elif isinstance(value, ast.Str):
                return value.s  # type: ignore

            return None
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None


def generate_documentation(files: List[str]) -> str:
    """
    Generates markdown documentation from a list of Python files.

    Args:
        files: A list of file paths to Python scripts.

    Returns:
        A single string containing the generated documentation in Markdown format.
    """
    doc_parts = [DOC_TITLE]

    # Group files by their parent directory (e.g., "tooling/", "utils/")
    grouped_files: Dict[str, List[str]] = {}
    for file in files:
        directory = os.path.dirname(file) + "/"
        if directory not in grouped_files:
            grouped_files[directory] = []
        grouped_files[directory].append(file)

    for directory, file_list in sorted(grouped_files.items()):
        doc_parts.append(f"\n---\n\n## `{directory}` Directory")
        for filepath in file_list:
            filename = os.path.basename(filepath)
            doc_parts.append(f"\n### `{filepath}`\n")

            docstring = extract_docstring(filepath)
            if docstring:
                doc_parts.append(docstring.strip())
            else:
                doc_parts.append("_No module-level docstring found._")

    return "\n".join(doc_parts)


def main():
    """
    Main function to generate the system documentation.
    """
    print("--> Finding Python files...")
    python_files = find_python_files(SCAN_DIRECTORIES)

    print(f"--> Found {len(python_files)} Python files to document.")

    print("--> Generating documentation from docstrings...")
    documentation = generate_documentation(python_files)

    print(f"--> Writing documentation to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(documentation)
        print("--> Documentation generated successfully.")
    except IOError as e:
        print(f"Error writing to file {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    main()