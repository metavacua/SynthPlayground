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
        print(f"Error: File not found at {args.filepath}")
        return

    print(f"Executing Aura script: {args.filepath}")
    l = lexer.Lexer(source_code)
    p = parser.Parser(l)
    program = p.parse_program()

    if p.errors:
        for error in p.errors:
            print(f"Parser error: {error}")
        return

    # --- Tooling and Execution Environment ---
    from aura_lang import interpreter
    from tooling import hdl_prover # Import the tool we want to expose
    from logic_system.src import diagram, lj, formulas, proof

    # --- Tooling and Execution Environment ---

    def dynamic_agent_call_tool(tool_name, *args):
        """
        Dynamically calls an agent tool and wraps the result in an Aura object.
        """
        print(f"[Aura Executor]: Received call for tool '{tool_name}' with args {args}")
        try:
            # For simplicity, we'll use a hardcoded map.
            # A real implementation would use a more dynamic discovery mechanism.
            if tool_name == "hdl_prover.prove_sequent":
                result = hdl_prover.prove_sequent(args[0])
                return interpreter.Object(result)
            elif tool_name == "environmental_probe.probe_network":
                from tooling import environmental_probe
                result = environmental_probe.probe_network()
                return interpreter.Object(result)
            elif tool_name == "diagram.translate":
                # Expects: proof_obj, start_logic_str, end_logic_str
                proof_obj, start_logic_str, end_logic_str = args

                # Convert string representations of logics to Enum members
                start_logic = diagram.Logic[start_logic_str]
                end_logic = diagram.Logic[end_logic_str]

                d = diagram.Diagram()
                translated_proof = d.translate(proof_obj, start_logic, end_logic)
                return interpreter.Object(translated_proof.to_dict())
            elif tool_name == "lj.axiom":
                prop_name = args[0]
                prop = formulas.Prop(prop_name)
                axiom_proof = lj.axiom(prop)
                return interpreter.Object(axiom_proof)
            else:
                print(f"Error: Tool '{tool_name}' not found.")
                return interpreter.Object(None)
        except Exception as e:
            print(f"Error executing tool '{tool_name}': {e}")
            return interpreter.Object(None)

    # --- Execute the Program ---
    env = interpreter.Environment()

    # Execute the script
    interpreter.evaluate(program, env)

if __name__ == "__main__":
    main()