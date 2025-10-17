"""
A unified documentation builder for the project.
...
"""
import ast
import os
import re
import json
import argparse
import markdown
import sys
from typing import List, Dict, Optional

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.file_system_utils import find_files

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --- Data Extraction & Parsing Backend ---

def get_module_docstring(filepath: str) -> str:
    """Parses a Python file and extracts its module-level docstring."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
            tree = ast.parse(source, filename=filepath)
            docstring = ast.get_docstring(tree, clean=True)
            return docstring or "_No module-level docstring found._"
    except (FileNotFoundError, SyntaxError) as e:
        return f"_Error parsing file: {e}_"

def get_protocol_summary(agents_md_path: str) -> List[str]:
    """Parses an AGENTS.md file and extracts a list of protocol summaries."""
    if not os.path.exists(agents_md_path):
        return [f"_Error: `{agents_md_path}` not found._"]
    try:
        with open(agents_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        protocol_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
        parts = []
        for block in protocol_blocks:
            try:
                protocol = json.loads(block)
                protocol_id = protocol.get("protocol_id")
                description = protocol.get("description")
                if protocol_id and description:
                    parts.append(f"- **`{protocol_id}`**: {description}")
            except json.JSONDecodeError:
                continue
        return parts if parts else ["_No protocols found in this module._"]
    except IOError as e:
        return [f"_Error reading `{agents_md_path}`: {e}_"]

# --- System Documentation Logic (from doc_generator.py) ---

class FunctionDoc:
    def __init__(self, name: str, signature: str, docstring: Optional[str]):
        self.name = name
        self.signature = signature
        self.docstring = docstring.strip() if docstring else ""

class ClassDoc:
    def __init__(self, name: str, docstring: Optional[str], methods: List[FunctionDoc]):
        self.name = name
        self.docstring = docstring.strip() if docstring else ""
        self.methods = sorted(methods, key=lambda m: m.name)

class ModuleDoc:
    def __init__(self, name: str, docstring: Optional[str], classes: List[ClassDoc], functions: List[FunctionDoc]):
        self.name = name
        self.docstring = docstring.strip() if docstring else ""
        self.classes = sorted(classes, key=lambda c: c.name)
        self.functions = sorted(functions, key=lambda f: f.name)

def _format_default_value(node: ast.expr) -> str:
    if isinstance(node, ast.Constant): return repr(node.value)
    if isinstance(node, ast.Name): return node.id
    return "..."

def format_args(args: ast.arguments) -> str:
    parts = []
    pos_defaults_offset = len(args.posonlyargs) + len(args.args) - len(args.defaults)
    for i, arg in enumerate(args.posonlyargs):
        if i >= pos_defaults_offset:
            default_val = _format_default_value(args.defaults[i - pos_defaults_offset])
            parts.append(f"{arg.arg}={default_val}")
        else:
            parts.append(arg.arg)
    if args.posonlyargs and args.args: parts.append("/")
    for i, arg in enumerate(args.args):
        arg_idx_in_defaults = i + len(args.posonlyargs) - pos_defaults_offset
        if arg_idx_in_defaults >= 0:
            default_val = _format_default_value(args.defaults[arg_idx_in_defaults])
            parts.append(f"{arg.arg}={default_val}")
        else:
            parts.append(arg.arg)
    if args.vararg: parts.append(f"*{args.vararg.arg}")
    if args.kwonlyargs and not args.vararg: parts.append("*")
    for i, kwarg in enumerate(args.kwonlyargs):
        if args.kw_defaults[i]:
            default_val = _format_default_value(args.kw_defaults[i])
            parts.append(f"{kwarg.arg}={default_val}")
        else:
            parts.append(kwarg.arg)
    if args.kwarg: parts.append(f"**{args.kwarg.arg}")
    return ", ".join(parts)

class DocVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes: List[ClassDoc] = []
        self.functions: List[FunctionDoc] = []
        self._current_class_methods: Optional[List[FunctionDoc]] = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name.startswith("_") and not node.name.startswith("__"): return
        signature = f"def {node.name}({format_args(node.args)})"
        docstring = ast.get_docstring(node)
        func_doc = FunctionDoc(name=node.name, signature=signature, docstring=docstring)
        if self._current_class_methods is not None:
            self._current_class_methods.append(func_doc)
        else:
            self.functions.append(func_doc)
        return

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name.startswith("_"): return
        docstring = ast.get_docstring(node)
        previous_methods_list = self._current_class_methods
        self._current_class_methods = []
        self.generic_visit(node)
        class_doc = ClassDoc(name=node.name, docstring=docstring, methods=self._current_class_methods)
        self.classes.append(class_doc)
        self._current_class_methods = previous_methods_list

def parse_file_for_docs(filepath: str) -> Optional[ModuleDoc]:
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            source = f.read()
            tree = ast.parse(source, filename=filepath)
            module_docstring = ast.get_docstring(tree, clean=True)
            visitor = DocVisitor()
            visitor.visit(tree)
            return ModuleDoc(name=filepath, docstring=module_docstring, classes=visitor.classes, functions=visitor.functions)
        except Exception as e:
            print(f"    -! Error parsing {filepath}: {e}")
            return None

def generate_documentation_for_module(mod_doc: ModuleDoc) -> List[str]:
    parts = [f"\n### `{mod_doc.name}`\n"]
    parts.append(mod_doc.docstring or "_No module-level docstring found._")
    if mod_doc.functions:
        parts.append("\n\n**Public Functions:**\n")
        for func in mod_doc.functions:
            parts.append(f"\n- #### `{func.signature}`\n")
            if func.docstring: parts.append(f"  > {func.docstring.replace(os.linesep, f'{os.linesep}  > ')}\n")
    if mod_doc.classes:
        parts.append("\n\n**Public Classes:**\n")
        for cls in mod_doc.classes:
            parts.append(f"\n- #### `class {cls.name}`\n")
            if cls.docstring: parts.append(f"  > {cls.docstring.replace(os.linesep, f'{os.linesep}  > ')}\n")
            if cls.methods:
                parts.append("\n  **Methods:**\n")
                for meth in cls.methods:
                    parts.append(f"  - ##### `{meth.signature}`\n")
                    if meth.docstring: parts.append(f"    > {meth.docstring.replace(os.linesep, f'{os.linesep}    > ')}\n")
    return parts

def find_python_files(directories: List[str]) -> List[str]:
    py_files = []
    for directory in directories:
        files = [os.path.join(directory, f) for f in find_files("*.py", base_dir=directory)]
        py_files.extend(files)
    return sorted([f for f in py_files if not os.path.basename(f).startswith("test_")])

def generate_system_docs(source_dirs: List[str], output_file: str):
    """Generates the detailed SYSTEM_DOCUMENTATION.md."""
    print("--> Finding Python files for system documentation...")
    python_files = find_python_files(source_dirs)
    print(f"--> Found {len(python_files)} Python files.")
    all_docs = [parse_file_for_docs(f) for f in python_files]
    all_docs_filtered = [doc for doc in all_docs if doc]

    doc_parts = ["# System Documentation"]
    grouped_docs: Dict[str, List[ModuleDoc]] = {}
    for mod_doc in all_docs_filtered:
        directory = os.path.dirname(mod_doc.name) + "/"
        if directory not in grouped_docs: grouped_docs[directory] = []
        grouped_docs[directory].append(mod_doc)
    for directory, doc_list in sorted(grouped_docs.items()):
        doc_parts.append(f"\n---\n\n## `{directory}` Directory")
        for mod_doc in sorted(doc_list, key=lambda d: d.name):
            doc_parts.extend(generate_documentation_for_module(mod_doc))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(doc_parts))
    print(f"--> System documentation written to {output_file}")


# --- README Generator ---
def generate_readme(agents_md_path: str, output_file: str):
    """Generates the high-level README.md for a module."""
    template = "# Module Documentation\n\n## Overview\n\nThis document provides a human-readable summary of the protocols and key components defined within this module. It is automatically generated.\n\n## Core Protocols\n\n{core_protocols}\n\n## Key Components\n\n{key_components}"

    protocol_md = "\n".join(get_protocol_summary(agents_md_path))

    tooling_dir = os.path.join(os.path.dirname(output_file), "tooling")
    if os.path.isdir(tooling_dir):
        key_files = find_files("*.py", base_dir=tooling_dir)
        key_files = [f for f in key_files if not os.path.basename(f).startswith("test_")]
        if key_files:
            components_parts = []
            for filename in sorted(key_files):
                filepath = os.path.join(tooling_dir, filename)
                docstring = get_module_docstring(filepath)
                components_parts.append(f"- **`tooling/{os.path.basename(filename)}`**:\n\n  > {docstring.replace(os.linesep, f'{os.linesep}  > ')}")
            components_md = "\n\n".join(components_parts)
        else:
            components_md = "_No key component scripts found in the `tooling/` directory._"
    else:
        components_md = "_This module does not contain a `tooling/` directory._"

    final_content = template.format(core_protocols=protocol_md, key_components=components_md).strip()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"--> README.md written to {output_file}")


# --- GitHub Pages Generator ---
def generate_pages(readme_path: str, agents_md_path: str, output_file: str):
    """Generates the index.html for GitHub Pages."""
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Project Documentation</title>
    <style>body {{ font-family: sans-serif; margin: 2em; }}</style>
</head>
<body>
{body_content}
</body>
</html>
"""
    try:
        with open(readme_path, "r") as f: readme_md = f.read()
        with open(agents_md_path, "r") as f: agents_md = f.read()
    except FileNotFoundError as e:
        print(f"Error: Source file not found for pages generation: {e}", file=sys.stderr)
        return
    full_md = f"# README\n\n{readme_md}\n\n<hr>\n\n# AGENTS.md\n\n{agents_md}"
    html_body = markdown.markdown(full_md, extensions=['fenced_code', 'tables'])
    final_html = html_template.format(body_content=html_body)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"--> GitHub Pages HTML written to {output_file}")


# --- Main CLI ---
def main():
    parser = argparse.ArgumentParser(description="Unified documentation builder.")
    parser.add_argument("--format", required=True, choices=["system", "readme", "pages"])
    parser.add_argument("--source-file", help="Source file for 'readme' or 'pages' format.")
    parser.add_argument("--output-file", help="Output file for any format.")
    parser.add_argument("--source-dir", action="append", help="Source directory for 'system' format.")
    args = parser.parse_args()

    print(f"--- Running Documentation Builder (Format: {args.format.upper()}) ---")
    if args.format == "system":
        source_dirs = args.source_dir or [os.path.join(ROOT_DIR, "tooling/"), os.path.join(ROOT_DIR, "utils/")]
        output_file = args.output_file or os.path.join(ROOT_DIR, "knowledge_core", "SYSTEM_DOCUMENTATION.md")
        generate_system_docs(source_dirs, output_file)
    elif args.format == "readme":
        source_file = args.source_file or os.path.join(ROOT_DIR, "AGENTS.md")
        output_file = args.output_file or os.path.join(ROOT_DIR, "README.md")
        generate_readme(source_file, output_file)
    elif args.format == "pages":
        readme_file = args.source_file or os.path.join(ROOT_DIR, "README.md")
        agents_file = os.path.join(os.path.dirname(readme_file), "AGENTS.md")
        output_file = args.output_file or os.path.join(ROOT_DIR, "index.html")
        generate_pages(readme_file, agents_file, output_file)
    print("--- Documentation Builder Finished ---")

if __name__ == "__main__":
    main()