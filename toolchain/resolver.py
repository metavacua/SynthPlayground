import json
import ast
import os

def resolve_contradiction(config_path='config.json'):
    """
    Resolves a constructive contradiction between two code versions based on a declared stance.

    This function reads a configuration file, selects a code version based on the
    'resolve_with_stance' key, and then uses the Abstract Syntax Tree (AST)
    to parse the selected file and write it to the resolved output path. This
    ensures the final output is always syntactically valid Python code.

    Args:
        config_path (str): The path to the JSON configuration file.
    """
    print(f"Starting resolution process with config: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    stance = config.get('resolve_with_stance')
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
    # 1. Parse the source code into an AST
    parsed_ast = ast.parse(source_code)
    print("Successfully parsed source code into AST.")

    # (In a more advanced tool, one could modify the AST here)

    # 2. Unparse the AST back into source code
    resolved_code = ast.unparse(parsed_ast)
    print("Successfully unparsed AST back into source code.")
    # --- END OF AST-BASED LOGIC ---

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(resolved_path), exist_ok=True)

    # Write the resolved code to the output file
    with open(resolved_path, 'w') as resolved_file:
        resolved_file.write(resolved_code)

    print(f"Resolution complete. Output written to: {resolved_path}")


if __name__ == "__main__":
    # This allows the script to be run directly from the command line.
    # It assumes the config file is in the same directory.
    try:
        resolve_contradiction('config.json')
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")