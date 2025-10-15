import sys
from parser import parse
from type_checker import type_check
from interpreter import interpret

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    try:
        ast = parse(code)
        type_check(ast)
        result = interpret(ast)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)