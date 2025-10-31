"""
This module provides functionality for...
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="Read the content of a file.")
    parser.add_argument("--filename", required=True, help="The name of the file to read.")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()
