import os
import json
import argparse

class SymbolExtractor:
    def __init__(self, ast_dir='knowledge_core/asts', symbol_map_file='knowledge_core/symbol_map.json'):
        self.ast_dir = ast_dir
        self.symbol_map_file = symbol_map_file
        self.symbol_map = self._load_symbol_map()

    def _load_symbol_map(self):
        if os.path.exists(self.symbol_map_file):
            with open(self.symbol_map_file, 'r') as f:
                return json.load(f)
        return {}

    def get_symbols_from_file(self, file_path):
        ast_path = os.path.join(self.ast_dir, f"{file_path}.json")
        if not os.path.exists(ast_path):
            return []

        with open(ast_path, 'r') as f:
            ast_data = json.load(f)

        return self._find_definitions_in_ast(ast_data)

    def find_all_references(self, symbol_name):
        return self.symbol_map.get(symbol_name, [])

    def _find_definitions_in_ast(self, ast_data):
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

    def generate_symbol_map(self):
        symbol_map = {}
        if not os.path.isdir(self.ast_dir):
            print(f"Error: ASTs directory not found at '{self.ast_dir}'")
            return

        for root, _, files in os.walk(self.ast_dir):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    original_filepath = os.path.relpath(filepath, self.ast_dir).replace('.json', '')

                    with open(filepath, "r") as f:
                        try:
                            ast_data = json.load(f)
                        except json.JSONDecodeError:
                            print(f"Warning: Could not parse JSON from {filepath}")
                            continue

                    definitions = self._find_definitions_in_ast(ast_data)

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

        output_dir = os.path.dirname(self.symbol_map_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(self.symbol_map_file, "w") as f:
            json.dump(symbol_map, f, indent=2)

        print(f"Symbol map successfully generated at {self.symbol_map_file}")
        self.symbol_map = symbol_map


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

    extractor = SymbolExtractor(ast_dir=args.asts_dir, symbol_map_file=args.output_file)
    extractor.generate_symbol_map()

if __name__ == '__main__':
    main()
