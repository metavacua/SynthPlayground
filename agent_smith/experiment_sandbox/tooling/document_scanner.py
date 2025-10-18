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
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.file_system_utils import find_files

def scan_documents(directory="."):
    """
    Scans a directory for PDF, Markdown, and text files and extracts their content.
    """
    scanned_data = {}
    pdf_files = find_files("*.pdf", base_dir=directory)
    md_files = find_files("*.md", base_dir=directory)
    txt_files = find_files("*.txt", base_dir=directory)

    for file in pdf_files:
        filepath = os.path.join(directory, file)
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            scanned_data[filepath] = text
        except (IOError, pypdf.errors.PdfReadError) as e:
            scanned_data[filepath] = f"Error reading PDF {filepath}: {e}"

    for file in md_files + txt_files:
        filepath = os.path.join(directory, file)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                scanned_data[filepath] = f.read()
        except IOError as e:
            scanned_data[filepath] = f"Error reading file {filepath}: {e}"
    return scanned_data