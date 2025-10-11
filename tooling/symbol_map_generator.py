"""
Generates a code symbol map for the repository to aid in contextual understanding.

This script creates a `symbols.json` file in the `knowledge_core` directory,
which acts as a high-level index of the codebase. This map contains information
about key programming constructs like classes and functions, including their
name, location (file path and line number), and language.

The script employs a two-tiered approach for symbol generation:
1.  **Universal Ctags (Preferred):** It first checks for the presence of the
    `ctags` command-line tool. If available, it uses `ctags` to perform a
    comprehensive, multi-language scan of the repository. This is the most
    robust and accurate method.
2.  **AST Fallback (Python-only):** If `ctags` is not found, the script falls
    back to using Python's built-in Abstract Syntax Tree (`ast`) module. This
    method parses all `.py` files and extracts symbol information for Python
    code. While less comprehensive than `ctags`, it ensures that a baseline
    symbol map is always available.

The resulting `symbols.json` artifact is a critical input for the agent's
orientation and planning phases, allowing it to quickly locate relevant code
and understand the structure of the repository without having to read every file.
"""

import os
import json
import glob
import subprocess
import ast


def has_ctags():
    """Check if Universal Ctags is installed and available in the PATH."""
    try:
        subprocess.run(["ctags", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def generate_symbols_with_ctags(root_dir="."):
    """Generates a symbol map using Universal Ctags."""
    print("Attempting to generate symbols with Universal Ctags...")
    output_path = os.path.join("knowledge_core", "symbols.json")

    # The command as specified in the documentation
    command = [
        "ctags",
        "-R",
        "--languages=python,javascript",  # Limiting for now for simplicity
        "--output-format=json",
        "--fields=+nKzSl",
        "-f",
        output_path,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"ctags ran successfully. Symbol map generated at {output_path}")
        # ctags output is not a single JSON object, but one per line. We need to wrap it.
        with open(output_path, "r") as f:
            lines = f.readlines()

        # Check if the file is empty
        if not lines:
            # Create a valid empty JSON object if no symbols were found
            symbols_data = {"symbols": []}
        else:
            # Parse each line as JSON and wrap in a list
            json_lines = [json.loads(line) for line in lines]
            symbols_data = {"symbols": json_lines}

        with open(output_path, "w") as f:
            json.dump(symbols_data, f, indent=2)
        print("Formatted symbols.json successfully.")
        return True

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: ctags command failed or ctags is not installed. Error: {e}")
        return False


def generate_symbols_with_ast(root_dir="."):
    """Fallback to generate a symbol map for Python files using the AST module."""
    print("Falling back to AST-based symbol generation for Python files...")
    symbols = []

    for filepath in glob.glob(os.path.join(root_dir, "**", "*.py"), recursive=True):
        path_components = filepath.split(os.sep)
        if (
            "node_modules" in path_components
            or "test" in path_components
            or "tests" in path_components
        ):
            continue

        try:
            with open(filepath, "r") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                    symbol_entry = {
                        "_type": "tag",
                        "name": node.name,
                        "path": filepath,
                        "language": "Python",
                        "line": node.lineno,
                        "kind": (
                            "function" if isinstance(node, ast.FunctionDef) else "class"
                        ),
                    }
                    symbols.append(symbol_entry)
        except Exception as e:
            print(f"Warning: Could not parse {filepath}. Error: {e}")

    return {"symbols": symbols}


def main():
    """Main function to generate and save the symbol map."""
    print("Generating symbol map...")

    if has_ctags():
        generate_symbols_with_ctags()
    else:
        symbols_data = generate_symbols_with_ast()
        output_path = os.path.join("knowledge_core", "symbols.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(symbols_data, f, indent=2)

        print(f"AST-based symbol map successfully generated at {output_path}")


if __name__ == "__main__":
    main()
