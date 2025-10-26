"""
A tool for converting Python code to UDC assembly-like code.
"""

import argparse
import os
import ast


class PythonToUdcConverter(ast.NodeVisitor):
    def __init__(self):
        self.udc_code = []
        self.label_counter = 0

    def visit_While(self, node):
        start_label = f"LOOP_START_{self.label_counter}"
        end_label = f"LOOP_END_{self.label_counter}"
        self.label_counter += 1

        self.udc_code.append(f"LABEL {start_label}")

        # Try to convert the loop condition to a CMP instruction
        if isinstance(node.test, ast.Compare):
            left = ast.unparse(node.test.left)
            right = ast.unparse(node.test.comparators[0])
            op = node.test.ops[0]

            self.udc_code.append(f"CMP {left}, {right}")

            if isinstance(op, ast.Lt):
                self.udc_code.append(f"JGE {end_label}")
            elif isinstance(op, ast.Gt):
                self.udc_code.append(f"JLE {end_label}")
            elif isinstance(op, ast.Eq):
                self.udc_code.append(f"JNE {end_label}")
            elif isinstance(op, ast.NotEq):
                self.udc_code.append(f"JE {end_label}")

        # The body of the loop would be here
        self.udc_code.append(f"JMP {start_label}")
        self.udc_code.append(f"LABEL {end_label}")

        self.generic_visit(node)


def main():
    parser = argparse.ArgumentParser(
        description="Converts a Python file to a UDC file."
    )
    parser.add_argument("filepath", help="The path to the Python file to convert.")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File not found at {args.filepath}")
        return

    with open(args.filepath, "r") as f:
        source = f.read()

    tree = ast.parse(source)
    converter = PythonToUdcConverter()
    converter.visit(tree)

    udc_filepath = os.path.splitext(args.filepath)[0] + ".udc"
    with open(udc_filepath, "w") as f:
        f.write("# This is a simplified UDC representation of the Python file.\n")
        f.write("\n".join(converter.udc_code))

    print(f"Successfully converted {args.filepath} to {udc_filepath}")


if __name__ == "__main__":
    main()
