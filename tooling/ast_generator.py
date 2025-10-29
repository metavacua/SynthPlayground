import os
import json
import importlib
import argparse
from tree_sitter import Language, Parser

# Mapping from file extensions to tree-sitter language names
LANGUAGE_MAPPING = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.rb': 'ruby',
    '.go': 'go',
    '.rs': 'rust',
}

# Mapping from language name to the grammar module
LANGUAGE_GRAMMARS = {
    'python': 'tree_sitter_python',
    'javascript': 'tree_sitter_javascript',
    'typescript': 'tree_sitter_typescript',
    'tsx': 'tree_sitter_typescript',  # tsx is handled by the typescript parser
    'ruby': 'tree_sitter_ruby',
    'go': 'tree_sitter_go',
    'rust': 'tree_sitter_rust',
}


# Directories to exclude from AST generation
EXCLUDE_DIRS = {'.git', 'knowledge_core', 'node_modules', '.venv'}


def node_to_dict(node):
    """
    Recursively convert a tree-sitter Node to a JSON-serializable dictionary,
    including field names for children.
    """
    result = {
        'type': node.type,
        'start_byte': node.start_byte,
        'end_byte': node.end_byte,
        'start_point': node.start_point,
        'end_point': node.end_point,
    }

    children = []
    for i, child_node in enumerate(node.children):
        child_dict = node_to_dict(child_node)
        field_name = node.field_name_for_child(i)
        if field_name:
            child_dict['field'] = field_name
        children.append(child_dict)

    result['children'] = children

    if not node.children:
        result['text'] = node.text.decode('utf8')
    return result


def get_parser_for_language(language_name):
    """
    Dynamically loads a tree-sitter parser for a given language.
    """
    if language_name not in LANGUAGE_GRAMMARS:
        return None

    grammar_module_name = LANGUAGE_GRAMMARS[language_name]
    try:
        # The tree-sitter-languages package installs individual packages like
        # tree_sitter_python, tree_sitter_javascript, etc.
        # We can dynamically import them.
        grammar_module = importlib.import_module(grammar_module_name)

        if language_name == 'tsx':
            language = Language(grammar_module.language_tsx())
        else:
            language = Language(grammar_module.language())

        parser = Parser(language)
        return parser
    except (ImportError, AttributeError) as e:
        print(f"Could not load grammar for {language_name}: {e}")
        return None


def generate_asts_for_repo(root_dir='.', output_dir='knowledge_core/asts'):
    """
    Traverses a repository, generates ASTs for supported files, and saves them.
    """
    print(f"Starting AST generation for repository at '{root_dir}'")

    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Modify dirs in-place to prune the search
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file_name in files:
            file_ext = os.path.splitext(file_name)[1]

            if file_ext in LANGUAGE_MAPPING:
                language_name = LANGUAGE_MAPPING[file_ext]
                parser = get_parser_for_language(language_name)

                if not parser:
                    continue

                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    tree = parser.parse(bytes(code, "utf8"))
                    root_node = tree.root_node
                    ast_dict = node_to_dict(root_node)

                    # Create the mirrored directory structure in the output directory
                    relative_path = os.path.relpath(file_path, root_dir)
                    output_file_path = os.path.join(
                        output_dir, f"{relative_path}.json")
                    output_file_dir = os.path.dirname(output_file_path)

                    if not os.path.exists(output_file_dir):
                        os.makedirs(output_file_dir)

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(ast_dict, f, indent=2)

                    print(f"Successfully generated AST for: {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    print("AST generation complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Generates ASTs for all supported source files in a repository."
    )
    parser.add_argument(
        "--root-dir",
        default=".",
        help="The root directory of the repository to scan.",
    )
    parser.add_argument(
        "--output-dir",
        default="knowledge_core/asts",
        help="The directory to save the generated ASTs.",
    )
    args = parser.parse_args()

    generate_asts_for_repo(root_dir=args.root_dir, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
