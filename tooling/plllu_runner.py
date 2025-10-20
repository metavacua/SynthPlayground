"""
A command-line runner for pLLLU files.

This script provides an entry point for executing `.plllu` files. It
integrates the pLLLU lexer, parser, and interpreter to execute the logic
defined in a given pLLLU source file and print the result.
"""

import argparse
import sys
import os

# Add the parent directory to the path to allow imports from lfi_ill
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lfi_ill.lexer import lexer
from lfi_ill.parser import parser
from lfi_ill.interpreter import Interpreter


def main():
    """
    This tool provides a command-line interface for running .plllu files.
    It integrates the pLLLU lexer, parser, and interpreter to execute
    the logic defined in a given pLLLU source file.
    """
    arg_parser = argparse.ArgumentParser(
        description="pLLLU file runner. This tool executes .plllu files."
    )
    arg_parser.add_argument("file", help="The .plllu file to execute.")
    args = arg_parser.parse_args()

    try:
        with open(args.file, "r") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
        sys.exit(1)

    # Create a new parser instance for each run
    # This is important because the parser object is stateful.
    plllu_parser = parser

    # Create an interpreter with the parser
    interpreter = Interpreter(plllu_parser)

    try:
        # The parse method now takes the data directly
        ast = plllu_parser.parse(data, lexer=lexer)
        if ast is None:
            # This can happen if the file is empty or there's a syntax error at EOF
            print("Syntax error: Could not parse the file.")
            sys.exit(1)

        result = interpreter.visit(ast)
        print(f"Result: {result}")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
