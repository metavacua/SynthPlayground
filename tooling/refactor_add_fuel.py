"""
A tool for refactoring a Python function to use a "fuel"-based approach to recursion.
"""

import argparse
import os
import ast


class FuelTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Add 'fuel' as a keyword argument with a default value
        node.args.kwonlyargs.append(ast.arg(arg="fuel"))
        node.args.kw_defaults.append(ast.Constant(value=100))
        self.generic_visit(node)
        return node

    def visit_While(self, node):
        # This is a simplified example that only transforms the first while loop it finds.
        # A more robust implementation would handle nested loops and other complexities.

        # Create the fuel check
        fuel_check = ast.Compare(
            left=ast.Name(id="fuel", ctx=ast.Load()),
            ops=[ast.LtE()],
            comparators=[ast.Constant(value=0)],
        )

        # Create the fuel decrement
        fuel_decrement = ast.Assign(
            targets=[ast.Name(id="fuel", ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Name(id="fuel", ctx=ast.Load()),
                op=ast.Sub(),
                right=ast.Constant(value=1),
            ),
        )

        # Create the new loop body
        new_body = [fuel_decrement] + node.body

        # Create the new while loop
        new_loop = ast.While(
            test=ast.BoolOp(
                op=ast.And(),
                values=[
                    ast.UnaryOp(op=ast.Not(), operand=fuel_check),
                    node.test,
                ],
            ),
            body=new_body,
            orelse=[],
        )

        return ast.copy_location(new_loop, node)


def main():
    parser = argparse.ArgumentParser(
        description="Refactors a Python function to use a 'fuel'-based approach."
    )
    parser.add_argument("filepath", help="The path to the Python file to refactor.")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}")
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
