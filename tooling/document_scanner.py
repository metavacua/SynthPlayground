"""
A tool for scanning the repository for human-readable documents and extracting their text content.

This script is a crucial component of the agent's initial information-gathering
and orientation phase. It allows the agent to ingest knowledge from unstructured
or semi-structured documents that are not part of the formal codebase, but which
may contain critical context, requirements, or specifications.

The scanner searches a given directory for files with common document extensions:
- `.pdf`: Uses the `pypdf` library to extract text from PDF files.
- `.md`: Reads Markdown files.
- `.txt`: Reads plain text files.

The output is a dictionary where the keys are the file paths of the discovered
documents and the values are their extracted text content. This data can then
be used by the agent to inform its planning and execution process. This tool
is essential for bridging the gap between human-written documentation and the
agent's operational awareness.
"""
import os
import pypdf
from pypdf import PdfReader
from tooling.filesystem_lister import list_all_files_and_dirs

def scan_documents(directory="."):
    """
    Scans a directory for PDF, Markdown, and text files and extracts their content.
    """
    scanned_data = {}
    # Use the authoritative filesystem_lister to get a reliable file list
    all_files = list_all_files_and_dirs(root_dir=directory, use_gitignore=True)

    for filepath in all_files:
        if filepath.endswith("/"):  # Skip directories
            continue

        if filepath.endswith(".pdf"):
            try:
                reader = PdfReader(filepath)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                scanned_data[filepath] = text
            except (IOError, pypdf.errors.PdfReadError) as e:
                scanned_data[filepath] = f"Error reading PDF {filepath}: {e}"
        elif filepath.endswith((".md", ".txt")):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    scanned_data[filepath] = f.read()
            except IOError as e:
                scanned_data[filepath] = f"Error reading file {filepath}: {e}"
    return scanned_data