"""
Generates detailed system documentation from Python source files.

This script scans specified directories for Python files, parses their
Abstract Syntax Trees (ASTs), and extracts documentation for the module,
classes, and functions. The output is a structured Markdown file.

This is a key component of the project's self-documentation capabilities,
powering the `SYSTEM_DOCUMENTATION.md` artifact in the `knowledge_core`.

The script is configured via top-level constants:
- `SCAN_DIRECTORIES`: A list of directories to search for .py files.
- `OUTPUT_FILE`: The path where the final Markdown file will be written.
- `DOC_TITLE`: The main title for the generated documentation file.

It uses Python's `ast` module to reliably parse source files without
importing them, which avoids issues with dependencies or script side-effects.
"""

import ast
import os
from typing import List, Dict, Optional

# Directories to scan for Python source files.
SCAN_DIRECTORIES = ["tooling/", "utils/"]
# The output file for the generated documentation.
OUTPUT_FILE = "knowledge_core/SYSTEM_DOCUMENTATION.md"
# The title of the generated documentation.
DOC_TITLE = "# System Documentation"

# --- Data Structures for Documentation ---


class FunctionDoc:
    """Holds documentation for a single function or method."""

    def __init__(self, name: str, signature: str, docstring: Optional[str]):
        self.name = name
        self.signature = signature
        self.docstring = docstring.strip() if docstring else ""


class ClassDoc:
    """Holds documentation for a single class."""

    def __init__(self, name: str, docstring: Optional[str], methods: List[FunctionDoc]):
        self.name = name
        self.docstring = docstring.strip() if docstring else ""
        self.methods = sorted(methods, key=lambda m: m.name)


class ModuleDoc:
    """Holds all documentation for a single Python module."""

    def __init__(
        self,
        name: str,
        docstring: Optional[str],
        classes: List[ClassDoc],
        functions: List[FunctionDoc],
    ):
        self.name = name
        self.docstring = docstring.strip() if docstring else ""
        self.classes = sorted(classes, key=lambda c: c.name)
        self.functions = sorted(functions, key=lambda f: f.name)


# --- AST Parsing Logic ---


def _format_default_value(node: ast.expr) -> str:
    """Safely formats a default argument value from an AST node."""
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    # Fallback for more complex expressions (e.g., calls, dicts)
    # This is a simplified representation.
    return "..."


def format_args(args: ast.arguments) -> str:
    """Formats ast.arguments into a printable string, including defaults."""
    parts = []

    # Calculate the offset for default arguments
    pos_defaults_offset = len(args.posonlyargs) + len(args.args) - len(args.defaults)

    # Positional-only arguments
    for i, arg in enumerate(args.posonlyargs):
        if i >= pos_defaults_offset:
            default_val = _format_default_value(args.defaults[i - pos_defaults_offset])
            parts.append(f"{arg.arg}={default_val}")
        else:
            parts.append(arg.arg)

    if args.posonlyargs and args.args:
        parts.append("/")  # Separator for pos-only args

    # Regular arguments
    for i, arg in enumerate(args.args):
        arg_idx_in_defaults = i + len(args.posonlyargs) - pos_defaults_offset
        if arg_idx_in_defaults >= 0:
            default_val = _format_default_value(args.defaults[arg_idx_in_defaults])
            parts.append(f"{arg.arg}={default_val}")
        else:
            parts.append(arg.arg)

    # Vararg (*args)
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")

    # Keyword-only arguments
    if args.kwonlyargs and not args.vararg:
        parts.append("*")

    for i, kwarg in enumerate(args.kwonlyargs):
        if args.kw_defaults[i]:
            default_val = _format_default_value(args.kw_defaults[i])
            parts.append(f"{kwarg.arg}={default_val}")
        else:
            parts.append(kwarg.arg)

    # Kwarg (**kwargs)
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")

    return ", ".join(parts)


class DocVisitor(ast.NodeVisitor):
    """
    AST visitor to extract documentation from classes and functions.
    It navigates the tree and builds lists of discovered documentation objects.
    """

    def __init__(self):
        self.classes: List[ClassDoc] = []
        self.functions: List[FunctionDoc] = []
        self._current_class_methods: Optional[List[FunctionDoc]] = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Skip private functions/methods (simple convention)
        if node.name.startswith("_") and not node.name.startswith("__"):
            return

        signature = f"def {node.name}({format_args(node.args)})"
        docstring = ast.get_docstring(node)
        func_doc = FunctionDoc(name=node.name, signature=signature, docstring=docstring)

        if self._current_class_methods is not None:
            self._current_class_methods.append(func_doc)
        else:
            self.functions.append(func_doc)

        # Don't visit nested functions
        return

    def visit_ClassDef(self, node: ast.ClassDef):
        # Skip private classes
        if node.name.startswith("_"):
            return

        docstring = ast.get_docstring(node)

        # Prepare to collect methods for this class
        previous_methods_list = self._current_class_methods
        self._current_class_methods = []

        # Visit the body of the class to find methods
        self.generic_visit(node)

        class_doc = ClassDoc(
            name=node.name, docstring=docstring, methods=self._current_class_methods
        )
        self.classes.append(class_doc)

        # Restore the previous state
        self._current_class_methods = previous_methods_list


def parse_file_for_docs(filepath: str) -> Optional[ModuleDoc]:
    """
    Parses a Python file and extracts documentation for its module, classes,
    and functions.
    """
    print(f"  - Parsing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            source = f.read()
            tree = ast.parse(source, filename=filepath)
            module_docstring = ast.get_docstring(tree, clean=True)

            visitor = DocVisitor()
            visitor.visit(tree)

            return ModuleDoc(
                name=filepath,
                docstring=module_docstring,
                classes=visitor.classes,
                functions=visitor.functions,
            )
        except Exception as e:
            print(f"    -! Error parsing {filepath}: {e}")
            return None


# --- Markdown Generation ---


def generate_documentation_for_module(mod_doc: ModuleDoc) -> List[str]:
    """Generates Markdown content for a single module."""
    parts = []

    # Module Header
    parts.append(f"\n### `{mod_doc.name}`\n")
    if mod_doc.docstring:
        parts.append(mod_doc.docstring)
    else:
        parts.append("_No module-level docstring found._")

    # Functions
    if mod_doc.functions:
        parts.append("\n\n**Public Functions:**\n")
        for func in mod_doc.functions:
            parts.append(f"\n- #### `{func.signature}`\n")
            if func.docstring:
                # Indent docstring for better readability
                indented_doc = "\n".join(
                    [f"  > {line}" for line in func.docstring.splitlines()]
                )
                parts.append(indented_doc + "\n")

    # Classes
    if mod_doc.classes:
        parts.append("\n\n**Public Classes:**\n")
        for cls in mod_doc.classes:
            parts.append(f"\n- #### `class {cls.name}`\n")
            if cls.docstring:
                indented_doc = "\n".join(
                    [f"  > {line}" for line in cls.docstring.splitlines()]
                )
                parts.append(indented_doc + "\n")

            if cls.methods:
                parts.append("\n  **Methods:**\n")
                for meth in cls.methods:
                    parts.append(f"  - ##### `{meth.signature}`\n")
                    if meth.docstring:
                        indented_doc = "\n".join(
                            [f"    > {line}" for line in meth.docstring.splitlines()]
                        )
                        parts.append(indented_doc + "\n")
    return parts


def generate_documentation(all_docs: List[ModuleDoc]) -> str:
    """
    Generates a single Markdown string from a list of ModuleDoc objects.
    """
    doc_parts = [DOC_TITLE]

    # Group docs by their parent directory
    grouped_docs: Dict[str, List[ModuleDoc]] = {}
    for mod_doc in all_docs:
        directory = os.path.dirname(mod_doc.name) + "/"
        if directory not in grouped_docs:
            grouped_docs[directory] = []
        grouped_docs[directory].append(mod_doc)

    for directory, doc_list in sorted(grouped_docs.items()):
        doc_parts.append(f"\n---\n\n## `{directory}` Directory")
        # Sort modules by filename
        for mod_doc in sorted(doc_list, key=lambda d: d.name):
            doc_parts.extend(generate_documentation_for_module(mod_doc))

    return "\n".join(doc_parts)


# --- Main Execution Logic ---


def find_python_files(directories: List[str]) -> List[str]:
    """Finds all Python files in the given directories, ignoring test files."""
    py_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    py_files.append(os.path.join(root, file))
    return sorted(py_files)


def main():
    """Main function to find files, parse them, and write documentation."""
    print("--> Finding Python files...")
    python_files = find_python_files(SCAN_DIRECTORIES)
    print(f"--> Found {len(python_files)} Python files to document.")

    print("--> Parsing files and extracting docstrings...")
    all_docs = [parse_file_for_docs(f) for f in python_files]
    all_docs_filtered = [doc for doc in all_docs if doc]

    if not all_docs_filtered:
        print("--> No valid documentation could be parsed. Exiting.")
        return

    print("--> Generating documentation from parsed data...")
    documentation = generate_documentation(all_docs_filtered)

    # Ensure the output directory exists
    output_dir = os.path.dirname(OUTPUT_FILE)
    if not os.path.exists(output_dir):
        print(f"--> Creating directory: {output_dir}")
        os.makedirs(output_dir)

    print(f"--> Writing documentation to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(documentation)
        print("--> Documentation generated successfully.")
    except IOError as e:
        print(f"Error writing to file {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    main()
