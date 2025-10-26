"""
Protocol Compiler

This script compiles protocol source files into a single YAML-LD artifact.
It is designed to be called by the main build script.
"""

import argparse
import json
import yaml
import os

def main():
    parser = argparse.ArgumentParser(description="Compile protocol sources.")
    parser.add_argument("--source-file", action="append", dest="source_files", help="Source files to compile.")
    parser.add_argument("--output-file", required=True, help="Output file path.")
    args = parser.parse_args()

    # For now, we'll just create a placeholder output file.
    # In the future, this will contain the compiled YAML-LD data.
    output_data = {
        "compiled": True,
        "sources": args.source_files,
        "output": args.output_file,
    }

    with open(args.output_file, "w") as f:
        yaml.dump(output_data, f, default_flow_style=False)

    print(f"Successfully compiled protocols to {args.output_file}")

if __name__ == "__main__":
    main()
