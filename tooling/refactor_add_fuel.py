"""
A tool for refactoring a Python function to use a "fuel"-based approach to recursion.
This tool is designed to be idempotent and handle nested while loops.
"""

import argparse
import os
import ast


class FuelTransformer(ast.NodeTransformer):
    """
    An AST transformer that injects a 'fuel' mechanism into functions and while loops.
    """

    def visit_FunctionDef(self, node):
        """
        Adds a 'fuel' keyword argument to a function definition if it doesn't already exist.
        """
        # Check if 'fuel' argument already exists to ensure idempotency.
        for arg in node.args.kwonlyargs:
            if arg.arg == "fuel":
                # If it exists, do nothing to this function's signature.
                # Still need to visit the body for while loops.
                self.generic_visit(node)
                return node

        # If 'fuel' argument is not found, add it.
        node.args.kwonlyargs.append(ast.arg(arg="fuel"))
        node.args.kw_defaults.append(ast.Constant(value=100))

        # Process the rest of the function body.
        self.generic_visit(node)
        return node

    def visit_While(self, node):
        """
        Transforms a 'while' loop to include a fuel check and decrement.
        Recursively transforms nested loops first (bottom-up).
        """
        # First, ensure any nested loops within this loop's body are transformed.
        self.generic_visit(node)

        # Create the AST nodes for the fuel mechanism.
        fuel_check = ast.Compare(
            left=ast.Name(id="fuel", ctx=ast.Load()),
            ops=[ast.LtE()],
            comparators=[ast.Constant(value=0)],
        )

        fuel_decrement = ast.Assign(
            targets=[ast.Name(id="fuel", ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Name(id="fuel", ctx=ast.Load()),
                op=ast.Sub(),
                right=ast.Constant(value=1),
            ),
        )

        # Prepend the fuel decrement to the original loop body.
        new_body = [fuel_decrement] + node.body

        # Combine the fuel check with the original loop condition.
        new_test = ast.BoolOp(
            op=ast.And(),
            values=[
                ast.UnaryOp(op=ast.Not(), operand=fuel_check),
                node.test,
            ],
        )

        # Create the new, fuel-limited while loop.
        new_loop = ast.While(
            test=new_test,
            body=new_body,
            orelse=node.orelse,  # Preserve the original else block
        )

        # Copy the original node's location for source mapping.
        return ast.copy_location(new_loop, node)


def main():
    parser = argparse.ArgumentParser(
        description="Refactors a Python function to use a 'fuel'-based approach."
    )
    parser.add_argument("filepath", help="The path to the Python file to refactor.")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        return

    with open(args.filepath, "r") as f:
        source = f.read()

    tree = ast.parse(source)
    transformer = FuelTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    with open(args.filepath, "w") as f:
        f.write(ast.unparse(new_tree))

    print(f"Successfully refactored {args.filepath} to use a 'fuel'-based approach.")


if __name__ == "__main__":
    main()
