import json

def verify_symbols():
    with open('knowledge_core/symbols.json', 'r') as f:
        data = json.load(f)

    symbols = data['symbols']
    errors = []

    for symbol in symbols:
        filepath = symbol['path']
        line_number = symbol['line']
        name = symbol['name']

        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
                if line_number > len(lines):
                    errors.append(f"Error: Line number {line_number} is out of range for file {filepath}")
                    continue

                line = lines[line_number - 1]
                if name not in line:
                    errors.append(f"Error: Symbol '{name}' not found on line {line_number} in file {filepath}")
        except FileNotFoundError:
            errors.append(f"Error: File not found: {filepath}")

    if errors:
        print("Symbol verification failed with the following errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Symbol verification successful!")

if __name__ == '__main__':
    verify_symbols()
