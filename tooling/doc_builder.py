"""
A unified documentation builder for the project.
...
"""

import os
import argparse
import sys
from typing import List, Dict

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.file_system_utils import find_files
from tooling.doc_builder_logic import (
    parse_file_for_docs,
    generate_system_docs_content,
    generate_pages_content,
    generate_tool_readme_content,
    generate_tooling_readme_content,
)

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def find_python_files(directories: List[str]) -> List[str]:
    py_files = []
    for directory in directories:
        # Ensure the directory path is absolute
        abs_dir = os.path.join(ROOT_DIR, directory)
        files = [os.path.join(abs_dir, f) for f in find_files("*.py", base_dir=abs_dir)]
        py_files.extend(files)
    return sorted([f for f in py_files if not os.path.basename(f).startswith("test_")])


def generate_system_docs(source_dirs: List[str], output_file: str):
    """Generates the detailed SYSTEM_DOCUMENTATION.md."""
    print("--> Finding Python files for system documentation...")
    python_files = find_python_files(source_dirs)
    print(f"--> Found {len(python_files)} Python files.")
    all_docs = []
    for f in python_files:
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
        all_docs.append(parse_file_for_docs(f, content))

    all_docs_filtered = [doc for doc in all_docs if doc]
    final_content = generate_system_docs_content(all_docs_filtered)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"--> System documentation written to {output_file}")


# --- GitHub Pages Generator ---
def generate_pages(readme_path: str, agents_md_path: str, output_file: str):
    """Generates the index.html for GitHub Pages."""
    try:
        with open(readme_path, "r") as f:
            readme_md = f.read()
        with open(agents_md_path, "r") as f:
            agents_md = f.read()
    except FileNotFoundError as e:
        print(
            f"Error: Source file not found for pages generation: {e}", file=sys.stderr
        )
        return

    final_html = generate_pages_content(readme_md, agents_md)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"--> GitHub Pages HTML written to {output_file}")


# --- Main CLI ---
def generate_tool_readme(source_file: str, output_file: str):
    """Generates a README.md for a single tool from its docstring."""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Source file: {source_file}")
    print(f"Output file: {output_file}")
    try:
        with open(source_file, "r", encoding="utf-8") as f:
            content = f.read()
        module_doc = parse_file_for_docs(source_file, content)
        if module_doc and module_doc.docstring:
            docstring = module_doc.docstring
        else:
            docstring = "No docstring found."
        filename = os.path.basename(source_file)
        final_content = generate_tool_readme_content(filename, docstring)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"--> Tool README written to {output_file}")
    except FileNotFoundError:
        print(f"Error: Source file not found at {source_file}", file=sys.stderr)


def generate_tooling_readme(source_dir: str, output_file: str):
    """Generates a single README.md for the tooling directory."""
    py_files = find_python_files([source_dir])
    docstrings: Dict[str, str] = {}
    for filepath in py_files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            module_doc = parse_file_for_docs(filepath, content)
            if module_doc and module_doc.docstring:
                docstrings[filename] = module_doc.docstring
            else:
                docstrings[filename] = "No docstring found."
        except FileNotFoundError:
            docstrings[filename] = "File not found."

    final_content = generate_tooling_readme_content(docstrings)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"--> Tooling README written to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Unified documentation builder.")
    parser.add_argument(
        "--format",
        required=True,
        choices=["system", "pages", "tooling-readme"],
    )
    parser.add_argument(
        "--source-file", help="Source file for 'readme' or 'pages' format."
    )
    parser.add_argument("--output-file", help="Output file for any format.")
    parser.add_argument(
        "--source-dir",
        action="append",
        help="Source directory for 'system' or 'tooling-readme' format. Can be specified multiple times.",
    )
    args = parser.parse_args()

    print(f"--- Running Documentation Builder (Format: {args.format.upper()}) ---")
    if args.format == "system":
        source_dirs = (
            args.source_dir
            if args.source_dir
            else [os.path.join(ROOT_DIR, "tooling/"), os.path.join(ROOT_DIR, "utils/")]
        )
        output_file = args.output_file or os.path.join(
            ROOT_DIR, "knowledge_core", "SYSTEM_DOCUMENTATION.md"
        )
        generate_system_docs(source_dirs, output_file)
    elif args.format == "pages":
        readme_file = args.source_file or os.path.join(ROOT_DIR, "README.md")
        agents_file = os.path.join(os.path.dirname(readme_file), "AGENTS.md")
        output_file = args.output_file or os.path.join(ROOT_DIR, "index.html")
        generate_pages(readme_file, agents_file, output_file)
    elif args.format == "tooling-readme":
        if not args.source_dir:
            parser.error("--source-dir is required for 'tooling-readme' format.")
        output_file = args.output_file or os.path.join(args.source_dir, "README.md")
        generate_tooling_readme(args.source_dir, output_file)
    print("--- Documentation Builder Finished ---")


if __name__ == "__main__":
    main()
