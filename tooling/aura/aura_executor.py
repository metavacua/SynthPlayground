# tooling/aura/aura_executor.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import argparse
from functools import partial
from tooling.aura.aura_api import agent_call_tool, registry

from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
from aura_lang.interpreter import evaluate, Environment, Object, Builtin

def main():
    parser = argparse.ArgumentParser(description="Execute an Aura script.")
    parser.add_argument("filepath", type=str, help="The path to the .aura script file.")
    args = parser.parse_args()

    try:
        with open(args.filepath, "r") as f:
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
        return

    def builtin_print(*args):
        output = " ".join(str(arg.inspect()) for arg in args)
        print(output)
        return Object(None)

    env = Environment()
    api_call = partial(agent_call_tool, registry)
    env.set("agent_call_tool", Builtin(api_call))
    env.set("print", Builtin(builtin_print))

    result = evaluate(program, env)

    if result:
        print(result.inspect())

if __name__ == "__main__":
    main()
