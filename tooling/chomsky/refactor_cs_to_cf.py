"""
A tool for refactoring context-sensitive Python code into context-free components.
"""

import argparse
import ast
import os
import sys

def is_pure(node):
    """
    Determines if a function definition node is pure.
    A function is considered pure if it does not perform any side effects.
    """
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Call):
            if isinstance(sub_node.func, ast.Name):
                if sub_node.func.id in ["open", "print"]:
                    return False
            elif isinstance(sub_node.func, ast.Attribute):
                if sub_node.func.value.id in ["os", "sys", "subprocess", "requests"]:
                    return False
    return True

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Refactor a context-sensitive Python file into a context-free component."
    )
    parser.add_argument("filepath", help="The path to the Python file to refactor.")
    args = parser.parse_args(argv)

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        sys.exit(1)

    with open(args.filepath, "r") as f:
        content = f.read()

    tree = ast.parse(content)
    pure_functions = []
    impure_functions = []
    other_nodes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if is_pure(node):
                pure_functions.append(node)
            else:
                impure_functions.append(node)
        else:
            other_nodes.append(node)

    if not pure_functions:
        print("No pure functions found to refactor.")
        return

    # Create the new logic file
    logic_filepath = args.filepath.replace(".py", "_logic.py")
    with open(logic_filepath, "w") as f:
        for node in pure_functions:
            f.write(ast.unparse(node))
            f.write("\n\n")

    # Modify the original file
    with open(args.filepath, "w") as f:
        # Add the import statement
        import_statement = f"from {os.path.basename(logic_filepath).replace('.py', '')} import {', '.join([f.name for f in pure_functions])}"
        f.write(import_statement)
        f.write("\n\n")

        # Write the other nodes
        for node in other_nodes:
            f.write(ast.unparse(node))
            f.write("\n\n")

        # Write the impure functions
        for node in impure_functions:
            f.write(ast.unparse(node))
            f.write("\n\n")

if __name__ == "__main__":
    main()
