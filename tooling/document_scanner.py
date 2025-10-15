"""
Recursively scans a directory to find and extract text from documents.

This script provides a crucial capability for the agent's orientation phase.
It walks through a given directory structure and identifies files with common
document extensions: `.pdf`, `.md`, and `.txt`.

For each file found, it attempts to extract the full text content:
- For `.pdf` files, it uses the `pypdf` library to parse the document and
  extract text from each page.
- For `.md` and `.txt` files, it reads the raw text content.

The script returns a dictionary where the keys are the file paths of the
scanned documents and the values are their extracted text content. This allows
the agent to gather a broad base of knowledge from the human-readable
documentation available in a repository.
"""
import os
import pypdf
from pypdf import PdfReader

def scan_documents(directory="."):
    """
    Scans a directory for PDF, Markdown, and text files and extracts their content.
    """
    scanned_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(".pdf"):
                try:
                    reader = PdfReader(filepath)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    scanned_data[filepath] = text
                except (IOError, pypdf.errors.PdfReadError) as e:
                    scanned_data[filepath] = f"Error reading PDF {filepath}: {e}"
            elif file.endswith((".md", ".txt")):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        scanned_data[filepath] = f.read()
                except IOError as e:
                    scanned_data[filepath] = f"Error reading file {filepath}: {e}"
    return scanned_data