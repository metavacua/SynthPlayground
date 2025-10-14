import sys
from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
from aura_lang.interpreter import evaluate, Environment, BUILTINS, Function as AuraFunction
from aura_lang import ast

def main():
    if len(sys.argv) < 2:
        print("Usage: python aura.py <filename>")
        return

    filepath = sys.argv[1]

    try:
        with open(filepath, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return

    # 1. Lexing & Parsing
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    if parser.errors:
        print("Parser errors:")
        for err in parser.errors:
            print(err)
        return

    # 2. Interpretation
    env = Environment()

    # Load built-ins
    for name, builtin in BUILTINS.items():
        env.set(name, builtin)

    # Explicit Definition Pass
    for statement in program.statements:
        if isinstance(statement, ast.FunctionDefinition):
            evaluate(statement, env)

    # 3. Execution Pass
    main_func = env.get("main")

    if not main_func or not isinstance(main_func, AuraFunction):
        print("Error: 'main' function not found or is not a function.")
        return

    main_env = Environment(outer=main_func.env)
    evaluate(main_func.body, main_env)


if __name__ == "__main__":
    main()