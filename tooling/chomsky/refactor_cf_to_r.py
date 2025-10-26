"""
A tool for refactoring context-free Python code into regular components.
"""

import argparse
import ast
import os
import sys

def is_lexer_like(node):
    """
    Determines if a function definition node is lexer-like.
    A function is considered lexer-like if it iterates over a string and
    yields tokens.
    """
    if not isinstance(node, ast.FunctionDef):
        return False

    has_loop = False
    has_yield = False
    for sub_node in ast.walk(node):
        if isinstance(sub_node, (ast.For, ast.While)):
            has_loop = True
        if isinstance(sub_node, ast.Yield):
            has_yield = True

    return has_loop and has_yield

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Refactor a context-free Python file into a regular component."
    )
    parser.add_argument("filepath", help="The path to the Python file to refactor.")
    args = parser.parse_args(argv)

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        sys.exit(1)

    with open(args.filepath, "r") as f:
        content = f.read()

    tree = ast.parse(content)
    lexer_functions = []
    other_nodes = []

    for node in tree.body:
        if is_lexer_like(node):
            lexer_functions.append(node)
        else:
            other_nodes.append(node)

    if not lexer_functions:
        print("No lexer-like functions found to refactor.")
        return

    # Create the new lexer file
    lexer_filepath = args.filepath.replace(".py", "_lexer.py")
    with open(lexer_filepath, "w") as f:
        for node in lexer_functions:
            f.write(ast.unparse(node))
            f.write("\n\n")

    # Modify the original file
    with open(args.filepath, "w") as f:
        # Add the import statement
        import_statement = f"from {os.path.basename(lexer_filepath).replace('.py', '')} import {', '.join([f.name for f in lexer_functions])}"
        f.write(import_statement)
        f.write("\n\n")

        # Write the other nodes
        for node in other_nodes:
            f.write(ast.unparse(node))
            f.write("\n\n")

if __name__ == "__main__":
    main()
