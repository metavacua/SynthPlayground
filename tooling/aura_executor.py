import argparse
import sys
from pathlib import Path

# Add the parent directory to the path to allow imports from aura_lang
sys.path.append(str(Path(__file__).resolve().parent.parent))

import importlib

from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
import aura_lang.interpreter as interpreter

def dynamic_agent_call_tool(tool_name, *args):
    """
    Dynamically imports and calls a tool from the 'tooling' directory.
    Tool name should be the module name, without .py.
    """
    try:
        # Sanitize the tool_name to prevent directory traversal
        if '..' in tool_name or '/' in tool_name or '.py' in tool_name:
            raise ValueError("Invalid tool name. Should be module name without path or extension.")

        module_name = f"tooling.{tool_name}"
        func_name = "main"
        tool_module = importlib.import_module(module_name)
        tool_func = getattr(tool_module, func_name)

        original_argv = sys.argv
        sys.argv = [f"tooling/{tool_name}.py"] + list(args)

        print(f"[Aura Executor]: Calling tool '{tool_name}' with args {args}...")
        result = tool_func()

        sys.argv = original_argv
        return result
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error calling tool '{tool_name}': {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred when calling tool '{tool_name}': {e}", file=sys.stderr)
        return None


def main():
    """
    Main entry point for the Aura script executor.
    """
    parser = argparse.ArgumentParser(description="Execute an Aura script.")
    parser.add_argument("filepath", type=str, help="The path to the .aura script file.")
    args = parser.parse_args()

    try:
        with open(args.filepath, 'r') as f:
            script_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {args.filepath}", file=sys.stderr)
        sys.exit(1)

    # Directly replace the function in the interpreter's BUILTINS object.
    # This is the most reliable way to ensure the correct function is called.
    interpreter.BUILTINS["agent"].call_tool.fn = dynamic_agent_call_tool

    lexer = Lexer(script_content)
    parser = Parser(lexer)
    program = parser.parse_program()

    if parser.errors:
        for error in parser.errors:
            print(f"Parser Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Create a global environment for the script
    env = interpreter.Environment()

    # Execute the script
    interpreter.evaluate(program, env)

if __name__ == "__main__":
    main()