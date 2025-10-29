import argparse
import json
import os

def find_definitions_in_ast(ast_data):
    """Finds all function and class definitions in an AST."""
    definitions = []

    def find_in_node(node):
        node_type = node.get('type')
        if node_type in ('function_definition', 'class_definition'):
            name_node = None
            for child in node.get('children', []):
                if child.get('field') == 'name':
                    name_node = child
                    break

            if name_node:
                symbol_name = name_node.get('text')
                definitions.append({
                    'name': symbol_name,
                    'type': node_type,
                    'start_point': node.get('start_point'),
                    'end_point': node.get('end_point'),
                })

        for child in node.get('children', []):
            find_in_node(child)

    find_in_node(ast_data)
    return definitions

def main():
    parser = argparse.ArgumentParser(
        description="Extracts function and class definitions from ASTs to create a symbol map."
    )
    parser.add_argument(
        "--asts-dir",
        default="knowledge_core/asts",
        help="The directory containing the generated ASTs in JSON format.",
    )
    parser.add_argument(
        "--output-file",
        default="knowledge_core/symbol_map.json",
        help="The path to the output symbol map JSON file.",
    )
    args = parser.parse_args()

    symbol_map = {}

    if not os.path.isdir(args.asts_dir):
        print(f"Error: ASTs directory not found at '{args.asts_dir}'")
        return

    for root, _, files in os.walk(args.asts_dir):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                original_filepath = os.path.relpath(filepath, args.asts_dir).replace('.json', '')

                with open(filepath, "r") as f:
                    try:
                        ast_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse JSON from {filepath}")
                        continue

                definitions = find_definitions_in_ast(ast_data)

                for definition in definitions:
                    symbol_name = definition['name']
                    if symbol_name not in symbol_map:
                        symbol_map[symbol_name] = []

                    symbol_map[symbol_name].append({
                        'filepath': original_filepath,
                        'type': definition['type'],
                        'start_point': definition['start_point'],
                        'end_point': definition['end_point'],
                    })

    output_dir = os.path.dirname(args.output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(args.output_file, "w") as f:
        json.dump(symbol_map, f, indent=2)

    print(f"Symbol map successfully generated at {args.output_file}")

if __name__ == "__main__":
    main()
