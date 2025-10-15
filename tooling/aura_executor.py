import argparse
import sys
import os

# Add the project root to the Python path to allow imports from aura_lang
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aura_lang import lexer, parser

def main():
    """
    Parses and executes an Aura script.
    """
    arg_parser = argparse.ArgumentParser(description="Aura Executor")
    arg_parser.add_argument("filepath", type=str, help="Path to the .aura file to execute.")
    args = arg_parser.parse_args()

    try:
        with open(args.filepath, "r") as f:
            source_code = f.read()
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
    # Manually load built-ins into the environment for now.
    for key, value in interpreter.BUILTINS.items():
        env.set(key, value)

    # Inject the real tool-calling function into the interpreter's context
    # by replacing the placeholder on the agent object.
    agent_obj = env.get("agent")
    agent_obj.call_tool = interpreter.Builtin(dynamic_agent_call_tool)

    print("Starting execution...")
    result = interpreter.evaluate(program, env)
    print(f"Execution finished. Final result: {result}")

if __name__ == "__main__":
    main()