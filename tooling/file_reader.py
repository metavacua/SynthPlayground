"""
This module provides functionality for...
"""

def read_file(filepath: str) -> str:
    """Reads the content of the specified file."""
    with open(filepath, "r") as f:
        return f.read()
