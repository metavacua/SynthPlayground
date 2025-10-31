"""
This script generates a symbol map for the repository.
...
"""

import argparse
import ast
import json
import os
import shutil
import subprocess

def has_ctags():
    """Checks if Universal Ctags is installed and available in the PATH."""
    return shutil.which("ctags") is not None

def generate_symbols_with_ctags(search_path, output_file):
    """Generates a symbol map using Universal Ctags."""
    print("Attempting to generate symbols with Universal Ctags...")
    ctags_output_file = "ctags_output.json"
    command = [
        "ctags",
        "-R",
        "--languages=python,javascript",
        "--output-format=json",
        "--fields=+nKzSl",
        f"-f",
        ctags_output_file,
        search_path,
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        with open(ctags_output_file, "r") as f:
            symbols = [json.loads(line) for line in f]
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump({"symbols": symbols}, f, indent=2)
        os.remove(ctags_output_file)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_symbols_with_ast(search_path):
    """Generates a symbol map for Python files using the AST module."""
    print("Falling back to AST-based symbol generation for Python files...")
    symbols = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    content = f.read()
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        symbols.append({
                            "name": node.name,
                            "path": filepath,
                            "kind": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                            "docstring": ast.get_docstring(node)
                        })
    return {"symbols": symbols}

def main():
    parser = argparse.ArgumentParser(description="Generates a symbol map for the repository.")
    parser.add_argument("--output", default="knowledge_core/symbols.json", help="The output file for the symbol map.")
    args = parser.parse_args()

    print("Generating symbol map...")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    if has_ctags():
        if not generate_symbols_with_ctags(".", args.output):
            symbols_data = generate_symbols_with_ast(".")
            with open(args.output, "w") as f:
                json.dump(symbols_data, f, indent=2)
            print(f"AST-based symbol map successfully generated at {args.output}")
    else:
        symbols_data = generate_symbols_with_ast(".")
        with open(args.output, "w") as f:
            json.dump(symbols_data, f, indent=2)
        print(f"AST-based symbol map successfully generated at {args.output}")

if __name__ == "__main__":
    main()
