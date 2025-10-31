"""
A tool for performing automated symbol renaming in Python code.

This script provides a command-line interface to find a specific symbol
(a function or a class) in a given Python file and rename it, along with all of
its textual references throughout the entire repository. This provides a safe
and automated way to perform a common refactoring task, reducing the risk of
manual errors.
"""

import argparse
import json
import os
import sys

from tooling.ast_generator import get_parser_for_language


def find_references(symbol_name, search_path):
    """Finds all files in a directory that reference a given symbol."""
    references = {}
    ast_dir = os.path.join(search_path, 'knowledge_core', 'asts')
    for root, _, files in os.walk(ast_dir):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                original_filepath = filepath.replace(
                    ast_dir + '/', '').replace('.json', '')
                with open(filepath, "r") as f:
                    ast_data = json.load(f)

                def find_in_ast(node):
                    if (node.get('type') == 'identifier' or node.get('type') == 'string_literal') and node.get('text') == symbol_name:
                        if original_filepath not in references:
                            references[original_filepath] = []
                        references[original_filepath].append(node)
                    for child in node.get('children', []):
                        find_in_ast(child)
                find_in_ast(ast_data)
    return references


def main():
    parser = argparse.ArgumentParser(
        description="A simple refactoring tool to rename a symbol in a Python file."
    )
    parser.add_argument(
        "--old-name", required=True, help="The current name of the symbol to rename."
    )
    parser.add_argument(
        "--new-name", required=True, help="The new name for the symbol."
    )
    parser.add_argument(
        "--search-path",
        default=".",
        help="The root directory to search for references.",
    )
    parser.add_argument(
        "--root-dir",
        default=".",
        help="The root directory of the repository.",
    )

    args = parser.parse_args()

    # Find all references to the symbol
    reference_files = find_references(args.old_name, args.search_path)

    # Rename the symbol in all referenced files
    for ref_file, nodes in reference_files.items():
        filepath = os.path.join(args.root_dir, ref_file)
        with open(filepath, "r") as f:
            original_content = f.read()

        nodes.sort(key=lambda x: x['start_byte'], reverse=True)

        new_content = list(original_content)
        for node in nodes:
            start = node['start_byte']
            end = node['end_byte']
            new_content[start:end] = args.new_name

        with open(filepath, "w") as f:
            f.write("".join(new_content))


if __name__ == "__main__":
    main()
