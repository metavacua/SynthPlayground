import os
import subprocess
import json
import ast
import shutil

OUTPUT_DIR = "knowledge_core"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "symbols.json")
SCAN_DIRECTORIES = ["tooling", "utils", "projects", "packages"]

def is_ctags_available():
    """Check if Universal Ctags is installed and available."""
    if not shutil.which("ctags"):
        return False
    try:
        result = subprocess.run(['ctags', '--version'], capture_output=True, text=True, check=True)
        return 'Universal Ctags' in result.stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def generate_symbols_with_ctags():
    """Generate a symbol map using Universal Ctags."""
    print("Attempting to generate symbols with Universal Ctags...")
    temp_output_file = OUTPUT_FILE + ".tmp"

    # Filter for directories that actually exist to prevent ctags errors
    existing_dirs_to_scan = [d for d in SCAN_DIRECTORIES if os.path.isdir(d)]
    if not existing_dirs_to_scan:
        print("No scannable directories found.")
        return False

    command = [
        'ctags',
        '-R',
        '--languages=python',
        '--output-format=json',
        '--fields=+nKzSl',
        '-f', temp_output_file,
    ] + existing_dirs_to_scan

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)

        with open(temp_output_file, 'r') as f:
            lines = f.readlines()

        symbols = [json.loads(line) for line in lines if line.strip()]

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(symbols, f, indent=4)

        print(f"ctags ran successfully. Symbol map generated at '{OUTPUT_FILE}'")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running ctags: {e.stderr}")
        return False
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error processing ctags output: {e}")
        return False
    finally:
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)

class SymbolVisitor(ast.NodeVisitor):
    """AST visitor to extract function and class symbols."""
    def __init__(self, filepath):
        self.symbols = []
        self.filepath = filepath

    def _add_symbol(self, node, kind):
        self.symbols.append({
            "name": node.name,
            "kind": kind,
            "path": self.filepath,
            "line": node.lineno,
            "_type": "tag"
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._add_symbol(node, "function")

    def visit_AsyncFunctionDef(self, node):
        self._add_symbol(node, "function")

    def visit_ClassDef(self, node):
        self._add_symbol(node, "class")

def generate_symbols_with_ast():
    """Generate a basic symbol map using Python's AST module as a fallback."""
    print("Falling back to AST-based symbol generation for Python files...")
    all_symbols = []
    for directory in SCAN_DIRECTORIES:
        if not os.path.isdir(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            source_code = f.read()
                        tree = ast.parse(source_code)
                        visitor = SymbolVisitor(filepath)
                        visitor.visit(tree)
                        all_symbols.extend(visitor.symbols)
                    except (SyntaxError, UnicodeDecodeError, ValueError) as e:
                        print(f"Could not parse {filepath}: {e}")

    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(all_symbols, f, indent=4)
        print(f"AST-based symbol map successfully generated at '{OUTPUT_FILE}'")
        return True
    except Exception as e:
        print(f"Error writing AST-based symbol map: {e}")
        return False

def generate_symbol_map():
    """
    Generates a symbol map for the codebase.
    It tries Universal Ctags first and falls back to a Python AST parser.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if is_ctags_available():
        if not generate_symbols_with_ctags():
            print("ctags failed. Falling back to AST parser.")
            generate_symbols_with_ast()
    else:
        print("Warning: Universal Ctags not found.")
        generate_symbols_with_ast()

if __name__ == "__main__":
    generate_symbol_map()