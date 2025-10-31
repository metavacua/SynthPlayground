"""
This module provides functionality for...
"""

import argparse
import os
import re

def main():
    """
    Validates a review document to ensure it complies with the Guardian Protocol.
    """
    parser = argparse.ArgumentParser(description="Guardian Protocol Validator")
    parser.add_argument("filepath", help="Path to the review document.")
    args = parser.parse_args()

    filepath = args.filepath

    if not os.path.exists(filepath):
        print(f"Error: Review document not found at {filepath}")
        exit(1)

    if not filepath.endswith(".md"):
        print("Error: Review document must be a markdown file.")
        exit(1)

    if "reviews/" not in filepath:
        print("Error: Review document must be in the reviews/ directory.")
        exit(1)

    with open(filepath, "r") as f:
        content = f.read()

    required_sections = ["Summary", "Impact Analysis", "Verification Plan"]
    for section in required_sections:
        if not re.search(fr"^\s*#+\s*{section}", content, re.MULTILINE | re.IGNORECASE):
            print(f"Error: Missing required section '{section}' in review document.")
            exit(1)

    print("Review document is valid.")

if __name__ == "__main__":
    main()
