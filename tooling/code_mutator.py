import argparse
import random

def mutate_code(filepath):
    """
    Performs a simple mutation on a file by replacing a common keyword.
    This is a placeholder for a more sophisticated mutation engine.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # A simple, non-destructive mutation
    mutations = {
        '==': '!=',
        '!=': '==',
        '>': '<',
        '<': '>',
        '>=': '<=',
        '<=': '>=',
    }

    possible_mutations = {k: v for k, v in mutations.items() if k in content}
    if not possible_mutations:
        print("No possible mutations found.")
        return

    operator_to_replace = random.choice(list(possible_mutations.keys()))
    replacement = possible_mutations[operator_to_replace]

    mutated_content = content.replace(operator_to_replace, replacement, 1)

    with open(filepath, 'w') as f:
        f.write(mutated_content)

    print(f"Mutated file: {filepath}")
    print(f"Replaced '{operator_to_replace}' with '{replacement}'")


def main():
    parser = argparse.ArgumentParser(description='A simple code mutation tool.')
    parser.add_argument('filepath', type=str, help='The path to the file to mutate.')
    args = parser.parse_args()
    mutate_code(args.filepath)

if __name__ == "__main__":
    main()
