import json
import ast
import os
import argparse


def resolve_contradiction(config_path='config.json', stance_override=None):
    """
    Resolves a constructive contradiction between two code versions based on a declared stance.

    This function reads a configuration file, selects a code version based on the
    'resolve_with_stance' key (or a command-line override), and then uses the
    Abstract Syntax Tree (AST) to parse the selected file and write it to the
    resolved output path. This ensures the final output is always syntactically valid Python code.

    Args:
        config_path (str): The path to the JSON configuration file.
        stance_override (str, optional): A stance provided to override the config file.
    """
    print(f"Starting resolution process with config: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Use the override if provided, otherwise use the value from the config file
    stance = stance_override if stance_override else config.get('resolve_with_stance')
    versions = config.get('versions')
    resolved_path = config.get('resolved_path')

    if not stance or not versions or not resolved_path:
        raise ValueError("Configuration file is missing required keys.")

    print(f"Resolution Stance: {stance}")

    source_file_path = None
    if stance == "Completeness":
        source_file_path = versions.get('version-A')
    elif stance == "Safety":
        source_file_path = versions.get('version-B')
    else:
        raise ValueError(f"Unknown stance for resolution: {stance}")

    if not source_file_path or not os.path.exists(source_file_path):
        raise FileNotFoundError(f"Source file for stance '{stance}' not found at path: {source_file_path}")

    print(f"Selected source file: {source_file_path}")

    # Read the chosen source code
    with open(source_file_path, 'r') as source_file:
        source_code = source_file.read()

    # --- CORE AST-BASED LOGIC ---
    parsed_ast = ast.parse(source_code)
    print("Successfully parsed source code into AST.")
    resolved_code = ast.unparse(parsed_ast)
    print("Successfully unparsed AST back into source code.")
    # --- END OF AST-BASED LOGIC ---

    os.makedirs(os.path.dirname(resolved_path), exist_ok=True)

    with open(resolved_path, 'w') as resolved_file:
        resolved_file.write(resolved_code)
        resolved_file.write('\n')  # Add newline at end of file

    print(f"Resolution complete. Output written to: {resolved_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Resolve code contradictions based on a stance.'
    )
    parser.add_argument(
        '--config', default='config.json', help='Path to the configuration file.'
    )
    parser.add_argument(
        '--stance',
        help='The resolution stance to use (e.g., "Safety", "Completeness"). Overrides the config file.'
    )
    args = parser.parse_args()

    try:
        resolve_contradiction(config_path=args.config, stance_override=args.stance)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
