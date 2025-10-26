"""
A compiler that translates AURA code to LFI-ILL.

This script takes an AURA file, parses it, and compiles it into an LFI-ILL
AST. The resulting AST is then written to a `.lfi_ill` file.
"""

import argparse
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aura_lang.lexer import Lexer as AuraLexer
from aura_lang.parser import Parser as AuraParser
from tooling.aura_to_lfi_ill_logic import AuraToLfiIllCompiler


def main():
    parser = argparse.ArgumentParser(description="Compile AURA code to LFI ILL.")
    parser.add_argument("file", help="The AURA file to compile.")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            aura_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
        return

    lexer = AuraLexer(aura_code)
    parser = AuraParser(lexer)
    aura_program = parser.parse_program()

    if parser.errors:
        print("AURA parsing errors:")
        for error in parser.errors:
            print(error)
        return

    compiler = AuraToLfiIllCompiler()
    lfi_ill_ast = compiler.compile(aura_program)

    print("--- COMPILED LFI ILL AST ---")
    print(repr(lfi_ill_ast))

    output_filename = args.file.replace(".aura", ".lfi_ill")
    with open(output_filename, "w") as f:
        f.write(repr(lfi_ill_ast))

    print(f"\nSuccessfully compiled to {output_filename}")


if __name__ == "__main__":
    main()
