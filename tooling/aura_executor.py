"""
This script serves as the command-line executor for `.aura` files.

It bridges the gap between the high-level Aura scripting language and the
agent's underlying Python-based toolset. The executor is responsible for:
1.  Parsing the `.aura` source code using the lexer and parser from the
    `aura_lang` package.
2.  Setting up an execution environment for the interpreter.
3.  Injecting a "tool-calling" capability into the Aura environment, which
    allows Aura scripts to dynamically invoke registered Python tools
    (e.g., `hdl_prover`, `environmental_probe`).
4.  Executing the parsed program and printing the final result.

This makes it a key component for enabling more expressive and complex
automation scripts for the agent.
"""
import argparse
import sys
from pathlib import Path
import subprocess
import importlib
import sys
from pathlib import Path

# Add the root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from languages.aura.lexer import Lexer
from languages.aura.parser import Parser
from languages.aura.interpreter import evaluate, Environment, Object, Builtin

def main():
    """
    Main entry point for the Aura script executor.
    """
    parser = argparse.ArgumentParser(description="Execute an Aura script.")
    parser.add_argument("filepath", type=str, help="The path to the .aura script file.")
    args = parser.parse_args()

    try:
        with open(args.filepath, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        sys.exit(1)

    l = Lexer(source_code)
    p = Parser(l)
    program = p.parse_program()

    if p.errors:
        for error in p.errors:
            print(f"Parser error: {error}", file=sys.stderr)
        sys.exit(1)

    # --- Set up the execution environment ---
    def builtin_print(*args):
        """A wrapper for the built-in print function that handles Aura objects."""
        output = " ".join(str(arg.value) for arg in args)
        sys.stdout.write(output + "\n")
        return Object(None)  # print returns null

    env = Environment()
    # Inject the print function into the Aura environment
    env.set("print", Builtin(builtin_print))

    # --- Execute the Program ---
    evaluate(program, env)


if __name__ == "__main__":
    main()