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
import importlib

# Add the parent directory to the path to allow imports from aura_lang
sys.path.append(str(Path(__file__).resolve().parent.parent))

from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
from aura_lang.interpreter import evaluate, Environment, Object, Builtin

# A dictionary to cache imported tool modules
_TOOL_CACHE = {}

def dynamic_agent_call_tool(tool_name_obj: Object, *args: Object) -> Object:
    """
    Dynamically imports and calls a tool from the 'tooling' directory and wraps the result.

    This function provides a secure, in-process bridge between the Aura scripting
    environment and the Python-based agent tools.

    Args:
        tool_name_obj: An Aura Object containing the tool's module name (e.g., 'hdl_prover').
        *args: A variable number of Aura Objects to be passed as arguments to the tool's main function.

    Returns:
        An Aura `Object` containing the tool's return value.
    """
    try:
        tool_name = tool_name_obj.value
        # Sanitize the tool_name to prevent directory traversal or other malicious imports.
        if not tool_name.isidentifier() or tool_name.startswith('_'):
            raise ValueError(f"Invalid or insecure tool name: '{tool_name}'")

        if tool_name in _TOOL_CACHE:
            tool_module = _TOOL_CACHE[tool_name]
        else:
            # Import the tool module from the 'tooling' directory
            tool_module = importlib.import_module(f"tooling.{tool_name}")
            _TOOL_CACHE[tool_name] = tool_module

        # Assume the tool has a 'main' function
        if not hasattr(tool_module, "main"):
            raise AttributeError(f"Tool '{tool_name}' does not have a 'main' function.")

        tool_function = getattr(tool_module, "main")
        unwrapped_args = [arg.value for arg in args]

        print(f"[Aura Executor]: Calling tool '{tool_name}' with args: {unwrapped_args}")
        result = tool_function(*unwrapped_args)

        # Wrap the result in an Aura Object
        return Object(result)

    except (ModuleNotFoundError, ValueError, AttributeError) as e:
        error_msg = f"Error preparing or calling tool '{tool_name}': {e}"
        print(error_msg, file=sys.stderr)
        return Object(f"Error: {error_msg}")
    except Exception as e:
        error_msg = f"An unexpected error occurred when calling tool '{tool_name}': {e}"
        print(error_msg, file=sys.stderr)
        return Object(f"Error: {error_msg}")


def execute_aura_script(filepath: str, tool_env: dict = None) -> Object:
    """
    Parses and executes an Aura script from a given file.

    Args:
        filepath: The path to the .aura script file.
        tool_env: An optional dictionary of pre-injected tools/functions.

    Returns:
        The final result of the script execution as an Aura Object.
    """
    try:
        with open(filepath, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        # In a library context, we should raise an exception, not exit.
        raise

    print(f"Executing Aura script: {filepath}")
    l = Lexer(source_code)
    p = Parser(l)
    program = p.parse_program()

    if p.errors:
        for error in p.errors:
            print(f"Parser error: {error}", file=sys.stderr)
        # In a library context, we should raise an exception, not exit.
        raise ValueError("Aura parsing failed.")

    # --- Set up the execution environment ---
    def builtin_print(*args: Object):
        """A wrapper for the built-in print function that handles Aura objects."""
        # The interpreter passes Aura Objects, so we need to get their .value
        output = " ".join(str(arg.value) for arg in args)
        print(output)
        return Object(None)  # print returns null

    env = Environment()
    # Inject the default tool-calling and print functions
    env.set("agent_call_tool", Builtin(dynamic_agent_call_tool))
    env.set("print", Builtin(builtin_print))

    # Allow for overriding or adding tools for testing or other purposes
    if tool_env:
        for name, func in tool_env.items():
            env.set(name, func)

    # --- Execute the Program ---
    result = evaluate(program, env)
    return result

def main():
    """
    Main command-line entry point for the Aura script executor.
    """
    parser = argparse.ArgumentParser(description="Execute an Aura script.")
    parser.add_argument("filepath", type=str, help="The path to the .aura script file.")
    args = parser.parse_args()

    try:
        result = execute_aura_script(args.filepath)

        # Print the final result of the script, if any
        if result:
            # The result of evaluate is an Aura Object, we print its primitive value
            print(f"\nScript Result: {result.value}")
    except (ValueError, FileNotFoundError) as e:
        # Exit gracefully if there's a parsing or file error.
        # The specific error will have already been printed.
        sys.exit(1)


if __name__ == "__main__":
    main()