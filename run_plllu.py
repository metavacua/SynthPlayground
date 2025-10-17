import argparse
from lfi_ill.parser import parse
from lfi_ill.interpreter import Interpreter, ParaconsistentTruth

def main():
    parser = argparse.ArgumentParser(description='pLLLU Interpreter')
    parser.add_argument('file', type=str, help='pLLLU file to execute')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        code = f.read()

    ast = parse(code)
    if not ast:
        print("Parsing failed.")
        return

    # For now, we'll use an empty environment.
    # In the future, we could allow setting initial values for atoms.
    interpreter = Interpreter()
    result = interpreter.eval(ast)

    print(f"Result for {args.file}: {result.name}")

if __name__ == '__main__':
    main()