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

# --- Path Correction ---
# To ensure that imports from sibling directories (like aura_lang) and
# modules within the tooling package work correctly, we need to add the
# project's root directory to the Python path. This is especially important
# when the script is executed directly.
import sys
from pathlib import Path
# Add the project root directory (the parent of 'tooling') to the path
sys.path.append(str(Path(__file__).resolve().parent.parent))
# --- End Path Correction ---

import argparse
import subprocess
from tooling.aura_logic import dynamic_agent_call_tool


from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
from aura_lang.interpreter import evaluate, Environment, Object, Builtin


def main():
    """
    Main entry point for the Aura script executor.
    """
    parser = argparse.ArgumentParser(description="Execute an Aura script.")
    parser.add_argument("filepath", type=str, help="The path to the .aura script file.")
    args = parser.parse_args()

    try:
        with open(args.filepath, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"Executing Aura script: {args.filepath}")
    l = Lexer(source_code)
    p = Parser(l)
    program = p.parse_program()

    if p.errors:
        for error in p.errors:
            print(f"Parser error: {error}", file=sys.stderr)
        return

    # --- Set up the execution environment ---
    def builtin_print(*args):
        """A wrapper for the built-in print function that handles Aura objects."""
        output = " ".join(str(arg.inspect()) for arg in args)
        print(output)
        return Object(None)  # print returns null

    env = Environment()
    # Inject the tool-calling and print functions into the Aura environment
    env.set("agent_call_tool", Builtin(dynamic_agent_call_tool))
    env.set("print", Builtin(builtin_print))

    # --- Execute the Program ---
    result = evaluate(program, env)

    # Print the final result of the script, if any
    if result:
        print(result.inspect())


if __name__ == "__main__":
    main()
