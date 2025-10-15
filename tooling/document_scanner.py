"""
This script provides a utility for extracting text content from various document types.

It is designed to scan a directory tree and identify files with common document
extensions like `.pdf`, `.md`, and `.txt`. For each file found, it uses the
appropriate method to read its content:
- For PDFs, it uses the `pypdf` library to extract text from each page.
- For Markdown and plain text files, it reads the raw text content.

The script returns a dictionary where the keys are the file paths of the
scanned documents and the values are their extracted text content. This tool is
a key part of the agent's initial orientation, allowing it to gather context
from human-readable documentation within the repository.
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