"""
A compiler that translates APPL (a simple functional language) to LFI-ILL.

This script takes a Python file containing an APPL AST, and compiles it into
an LFI-ILL AST. The resulting AST is then written to a `.lfi_ill` file.
"""

import argparse
import sys
import os
import importlib.util
from tooling.appl_to_lfi_ill_logic import ApplToLfiIllCompiler

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    parser = argparse.ArgumentParser(description="Compile APPL code to LFI ILL.")
    parser.add_argument("file", help="The APPL file to compile (as a Python file).")
    args = parser.parse_args()

    try:
        module_name = os.path.splitext(os.path.basename(args.file))[0]
        spec = importlib.util.spec_from_file_location(module_name, args.file)
        appl_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(appl_module)
        appl_ast_node = appl_module.APPL_AST
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
        return
    except Exception as e:
        print(f"Error loading APPL module from file: {e}")
        return

    compiler = ApplToLfiIllCompiler()
    lfi_ill_ast = compiler.compile(appl_ast_node.term)

    print("--- COMPILED LFI ILL AST ---")
    print(repr(lfi_ill_ast))

    output_filename = args.file.replace(".py", ".lfi_ill")
    with open(output_filename, "w") as f:
        f.write(repr(lfi_ill_ast))

    print(f"\nSuccessfully compiled to {output_filename}")


if __name__ == "__main__":
    main()
