import os
import re
import argparse
import sys

def analyze_protocol(filepath):
    """
    Analyzes an AGENTS.md file for quality and structural integrity.

    Checks for:
    1.  Presence of key structural headers.
    2.  Existence of file paths referenced within the text.
    3.  Basic complexity metrics (number of sections).
    """
    if not os.path.exists(filepath):
        print(f"Error: Input file not found at '{filepath}'", file=sys.stderr)
        return

    with open(filepath, 'r') as f:
        content = f.read()

    results = {
        "structural_validation": {"passed": True, "missing": []},
        "file_references": {"total": 0, "valid": 0, "invalid": []},
        "complexity": {"h2_sections": 0, "h3_sections": 0},
    }

    # 1. Structural Validation
    required_headers = [
        "## 1. The Core Problem",
        "## 2. The Solution",
        "### STANDING ORDERS",
    ]
    for header in required_headers:
        if header not in content:
            results["structural_validation"]["passed"] = False
            results["structural_validation"]["missing"].append(header)

    # 2. File Reference Verification
    # This regex finds paths that look like 'tooling/script.py' or 'protocols/file.md'
    # It specifically looks for paths containing a slash.
    referenced_files = re.findall(r'[`\'"]([a-zA-Z0-9_-]+/[a-zA-Z0-9_./-]+)', content)
    unique_files = sorted(list(set(referenced_files)))

    results["file_references"]["total"] = len(unique_files)
    for file_ref in unique_files:
        if os.path.exists(file_ref):
            results["file_references"]["valid"] += 1
        else:
            results["file_references"]["invalid"].append(file_ref)

    # 3. Complexity Metrics
    results["complexity"]["h2_sections"] = len(re.findall(r'(?m)^## ', content))
    results["complexity"]["h3_sections"] = len(re.findall(r'(?m)^### ', content))

    # --- Print Report ---
    print("--- Protocol Analysis Report ---")
    print(f"File: {filepath}\n")

    print("1. Structural Validation:")
    if results["structural_validation"]["passed"]:
        print("  - Status: PASSED")
    else:
        print("  - Status: FAILED")
        for missing in results["structural_validation"]["missing"]:
            print(f"    - Missing required header: {missing}")

    print("\n2. File Reference Verification:")
    print(f"  - Total unique file references found: {results['file_references']['total']}")
    print(f"  - Valid references (file exists): {results['file_references']['valid']}")
    if results["file_references"]["invalid"]:
        print("  - Invalid references (file NOT found):")
        for invalid in results["file_references"]["invalid"]:
            print(f"    - {invalid}")

    print("\n3. Complexity Metrics:")
    print(f"  - Number of H2 sections: {results['complexity']['h2_sections']}")
    print(f"  - Number of H3 sections: {results['complexity']['h3_sections']}")
    print("\n--- End of Report ---")

def main():
    parser = argparse.ArgumentParser(description="Analyze an AGENTS.md file for quality and structural integrity.")
    parser.add_argument(
        "input_file",
        help="The path to the AGENTS.md file to analyze."
    )
    args = parser.parse_args()

    analyze_protocol(args.input_file)

if __name__ == "__main__":
    main()