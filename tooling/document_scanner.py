"""
A tool for scanning the repository for document files (.pdf, .md, .txt)
and extracting their text content.

This scanner is a crucial part of the agent's bootstrap process, allowing it
to gather initial context from human-written documents found within the
project structure.
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