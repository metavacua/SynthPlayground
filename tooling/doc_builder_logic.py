import ast
import os
import re
import json
import markdown
from typing import List, Dict, Optional


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


def _format_default_value(node: ast.expr) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
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
    if args.posonlyargs and args.args:
        parts.append("/")
    for i, arg in enumerate(args.args):
        arg_idx_in_defaults = i + len(args.posonlyargs) - pos_defaults_offset
        if arg_idx_in_defaults >= 0:
            default_val = _format_default_value(args.defaults[arg_idx_in_defaults])
            parts.append(f"{arg.arg}={default_val}")
        else:
            parts.append(arg.arg)
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    if args.kwonlyargs and not args.vararg:
        parts.append("*")
    for i, kwarg in enumerate(args.kwonlyargs):
        if args.kw_defaults[i]:
            default_val = _format_default_value(args.kw_defaults[i])
            parts.append(f"{kwarg.arg}={default_val}")
        else:
            parts.append(kwarg.arg)
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")
    return ", ".join(parts)


class DocVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes: List[ClassDoc] = []
        self.functions: List[FunctionDoc] = []
        self._current_class_methods: Optional[List[FunctionDoc]] = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name.startswith("_") and not node.name.startswith("__"):
            return
        signature = f"def {node.name}({format_args(node.args)})"
        docstring = ast.get_docstring(node)
        func_doc = FunctionDoc(name=node.name, signature=signature, docstring=docstring)
        if self._current_class_methods is not None:
            self._current_class_methods.append(func_doc)
        else:
            self.functions.append(func_doc)
        return

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name.startswith("_"):
            return
        docstring = ast.get_docstring(node)
        previous_methods_list = self._current_class_methods
        self._current_class_methods = []
        self.generic_visit(node)
        class_doc = ClassDoc(
            name=node.name, docstring=docstring, methods=self._current_class_methods
        )
        self.classes.append(class_doc)
        self._current_class_methods = previous_methods_list


def parse_file_for_docs(filepath: str, content: str) -> Optional[ModuleDoc]:
    try:
        tree = ast.parse(content, filename=filepath)
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


def generate_documentation_for_module(mod_doc: ModuleDoc) -> List[str]:
    parts = [f"\n### `{mod_doc.name}`\n"]
    parts.append(mod_doc.docstring or "_No module-level docstring found._")
    if mod_doc.functions:
        parts.append("\n\n**Public Functions:**\n")
        for func in mod_doc.functions:
            parts.append(f"\n- #### `{func.signature}`\n")
            if func.docstring:
                parts.append(
                    f"  > {func.docstring.replace(os.linesep, f'{os.linesep}  > ')}\n"
                )
    if mod_doc.classes:
        parts.append("\n\n**Public Classes:**\n")
        for cls in mod_doc.classes:
            parts.append(f"\n- #### `class {cls.name}`\n")
            if cls.docstring:
                parts.append(
                    f"  > {cls.docstring.replace(os.linesep, f'{os.linesep}  > ')}\n"
                )
            if cls.methods:
                parts.append("\n  **Methods:**\n")
                for meth in cls.methods:
                    parts.append(f"  - ##### `{meth.signature}`\n")
                    if meth.docstring:
                        parts.append(
                            f"    > {meth.docstring.replace(os.linesep, f'{os.linesep}    > ')}\n"
                        )
    return parts


def generate_system_docs_content(all_docs: List[ModuleDoc]) -> str:
    doc_parts = ["# System Documentation"]
    grouped_docs: Dict[str, List[ModuleDoc]] = {}
    for mod_doc in all_docs:
        directory = os.path.dirname(mod_doc.name) + "/"
        if directory not in grouped_docs:
            grouped_docs[directory] = []
        grouped_docs[directory].append(mod_doc)
    for directory, doc_list in sorted(grouped_docs.items()):
        doc_parts.append(f"\n---\n\n## `{directory}` Directory")
        for mod_doc in sorted(doc_list, key=lambda d: d.name):
            doc_parts.extend(generate_documentation_for_module(mod_doc))
    return "\n".join(doc_parts)


def generate_readme_content(
    protocol_summaries: List[str], component_docstrings: Dict[str, str]
) -> str:
    template = "# Module Documentation\n\n## Overview\n\nThis document provides a human-readable summary of the protocols and key components defined within this module. It is automatically generated.\n\n## Core Protocols\n\n{core_protocols}\n\n## Key Components\n\n{key_components}"

    protocol_md = "\n".join(protocol_summaries)

    if component_docstrings:
        components_parts = []
        for filename, docstring in sorted(component_docstrings.items()):
            components_parts.append(
                f"- **`tooling/{filename}`**:\n\n  > {docstring.replace(os.linesep, f'{os.linesep}  > ')}"
            )
        components_md = "\n\n".join(components_parts)
    else:
        components_md = "_No key component scripts found in the `tooling/` directory._"

    return template.format(
        core_protocols=protocol_md, key_components=components_md
    ).strip()


def generate_pages_content(readme_md: str, agents_md: str) -> str:
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
    full_md = f"# README\n\n{readme_md}\n\n<hr>\n\n# AGENTS.md\n\n{agents_md}"
    html_body = markdown.markdown(full_md, extensions=["fenced_code", "tables"])
    return html_template.format(body_content=html_body)


def generate_tool_readme_content(filename: str, docstring: str) -> str:
    return f"# Tool: `{filename}`\n\n{docstring}"


def generate_tooling_readme_content(
    docstrings: Dict[str, str]
) -> str:
    parts = [
        "# Tooling Directory Documentation\n\nThis document provides an overview of the tools available in the `tooling/` directory. It is automatically generated from the docstrings of the tools.\n"
    ]

    for filename, docstring in sorted(docstrings.items()):
        parts.append(f"\n---\n\n## `{filename}`\n\n{docstring}\n")

    return "".join(parts)


def generate_main_readme_content(
    template_content: str, witness_docs: Dict[str, str]
) -> str:
    """Generates the content for the main README.md file."""
    witness_parts = []
    for filename, docstring in sorted(witness_docs.items()):
        witness_parts.append(f"\n---\n\n## `{filename}`\n\n{docstring}\n")
        witness_parts.append(f"### How to Run\n```bash\npython {filename}\n```\n")

    return template_content.format(witness_docs="".join(witness_parts))


def get_protocol_description(file_path: str) -> Optional[str]:
    """Extracts the protocol description from a YAML file."""
    import yaml

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("description")
    except (IOError, yaml.YAMLError) as e:
        print(f"    -! Error processing {file_path}: {e}")
        return None


def generate_main_readme_v2_content(
    template_content: str,
    protocol_docs: Dict[str, str],
    tool_docs: Dict[str, str],
) -> str:
    """Generates the content for the v2 README.md file."""
    protocol_parts = []
    for filename, description in sorted(protocol_docs.items()):
        protocol_parts.append(f"- **`{filename}`**: {description}")

    tool_parts = []
    for filename, docstring in sorted(tool_docs.items()):
        tool_parts.append(f"- **`{filename}`**: {docstring}")

    return template_content.format(
        protocol_docs="\n".join(protocol_parts),
        tool_docs="\n".join(tool_parts),
    )
