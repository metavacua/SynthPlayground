import sys
from lfi_ill.interpreter import Interpreter

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run_lfi_ill.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    # The lfi_ill parser seems to be designed to parse line by line
    lines = code.splitlines()

    from lfi_ill.lexer import lexer
    from lfi_ill.parser import parser

    print(f"Running tests from: {filename}\\n")

    for line in lines:
        line = line.strip().split('--')[0].strip()
        if not line:
            continue

        try:
            ast = parser.parse(line, lexer=lexer)

            interpreter = Interpreter(parser=None)
            result = interpreter.visit(ast)
            print(f"Input:  {line}")
            print(f"Result: {result}\\n")
        except Exception as e:
            print(f"Error processing line: '{line}'")
            print(f"Error: {e}\\n")