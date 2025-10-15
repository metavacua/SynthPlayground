"""
This script serves as the command-line executor for `.aura` files.

It bridges the gap between the high-level Aura scripting language and the
agent's underlying Python-based toolset. The executor is responsible for:
1.  Parsing the `.aura` source code using the lexer and parser from the
    `aura_lang` package.
2.  Setting up an execution environment for the interpreter.
3.  Injecting a "tool-calling" capability into the Aura environment, which
    allows Aura scripts to dynamically invoke registered Python tools.
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
import aura_lang.interpreter as interpreter

from tooling.tool_registry import TOOL_REGISTRY

def dynamic_agent_call_tool(tool_name, *args):
    """
    Dynamically imports and calls a tool from the tool registry.
    """
    if tool_name not in TOOL_REGISTRY:
        print(f"Error: Tool '{tool_name}' not found in registry.", file=sys.stderr)
        return None

    try:
        module_name = TOOL_REGISTRY[tool_name]
        func_name = "main"
        tool_module = importlib.import_module(module_name)
        tool_func = getattr(tool_module, func_name)

        original_argv = sys.argv
        sys.argv = [module_name.replace('.', '/') + ".py"] + list(args)

        print(f"[Aura Executor]: Calling tool '{tool_name}' with args {args}...")
        result = tool_func()

        sys.argv = original_argv
        return interpreter.Object(result)
    except ModuleNotFoundError:
        # Re-raise this specific error for testing purposes
        raise
    except (AttributeError) as e:
        print(f"Error calling tool '{tool_name}': {e}", file=sys.stderr)
        return interpreter.Object(None)
    except Exception as e:
        print(f"An unexpected error occurred when calling tool '{tool_name}': {e}", file=sys.stderr)
        return interpreter.Object(None)


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
        print(f"Error: File not found at {args.filepath}")
        return

    print(f"Executing Aura script: {args.filepath}")
    l = Lexer(script_content)
    p = Parser(l)
    program = p.parse_program()

    if p.errors:
        for error in p.errors:
            print(f"Parser error: {error}")
        return

    # --- Tooling and Execution Environment ---
    env = interpreter.Environment()
    env.set("call_tool", interpreter.Builtin(dynamic_agent_call_tool))

    # Execute the script
    result = interpreter.evaluate(program, env)

    if result is not None:
        print(result.inspect())


if __name__ == "__main__":
    main()