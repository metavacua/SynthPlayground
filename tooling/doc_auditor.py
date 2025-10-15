import re
import argparse

def audit_documentation(filepath):
    """
    Scans the system documentation file for modules missing docstrings.

    Args:
        filepath: The path to the SYSTEM_DOCUMENTATION.md file.

    Returns:
        A list of file paths for modules that are missing docstrings.
    """
    missing_docstrings = []
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Documentation file not found at {filepath}")
        return missing_docstrings

    # Regex to find the file path header and the "no docstring" message
    # It looks for a line like "### `tooling/builder.py`"
    # followed by a line with "_No module-level docstring found._"
    pattern = re.compile(r"### `(.*?\.py)`\n\n_No module-level docstring found._")

    matches = pattern.findall(content)

    for match in matches:
        missing_docstrings.append(match)

    return missing_docstrings

def main():
    """
    Command-line interface for the documentation auditor.
    """
    parser = argparse.ArgumentParser(description="Documentation Auditor")
    parser.add_argument(
        "--filepath",
        type=str,
        default="knowledge_core/SYSTEM_DOCUMENTATION.md",
        help="Path to the system documentation file to audit."
    )
    args = parser.parse_args()

    undocumented_modules = audit_documentation(args.filepath)

    if undocumented_modules:
        print("The following modules are missing docstrings:")
        for module in undocumented_modules:
            print(f" - {module}")
    else:
        print("All modules have at least a module-level docstring. Well done!")

if __name__ == "__main__":
    main()