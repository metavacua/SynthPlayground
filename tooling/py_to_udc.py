"""
A tool for converting Python code to UDC assembly-like code.
"""

import argparse
import os
import ast


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
    udc_code = []
    label_counter = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            start_label = f"LOOP_START_{label_counter}"
            end_label = f"LOOP_END_{label_counter}"
            label_counter += 1

            udc_code.append(f"LABEL {start_label}")
            # A simple CMP to represent the loop condition
            udc_code.append("CMP R1, 0")
            udc_code.append(f"JE {end_label}")
            # The body of the loop would be here
            udc_code.append(f"JMP {start_label}")
            udc_code.append(f"LABEL {end_label}")

    udc_filepath = os.path.splitext(args.filepath)[0] + ".udc"
    with open(udc_filepath, "w") as f:
        f.write("\n".join(udc_code))

    print(f"Successfully converted {args.filepath} to {udc_filepath}")


if __name__ == "__main__":
    main()
