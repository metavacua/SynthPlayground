import sys
from .parser import parse
from .interpreter import Interpreter, Truth

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m plllu.run_plllu <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        sys.exit(1)

    ast = parse(source_code)
    if not ast:
        print("Parsing failed.")
        sys.exit(1)

    interpreter = Interpreter()
    result = interpreter.eval(ast)

    print(f"Source:\n{source_code}")
    print(f"\nAST:\n{ast}")
    print(f"\nResult: {result.name}")

if __name__ == "__main__":
    main()