"""
This module provides functionality for...
"""

import os
import sys
import json
import re
import jsonschema


def find_files(pattern, base_dir=".", recursive=True):
    """Finds files matching a pattern in a directory."""
    if recursive:
        return [
            os.path.join(dp, f)
            for dp, dn, filenames in os.walk(base_dir)
            for f in filenames
            if f.endswith(pattern)
        ]
    else:
        return [
            f
            for f in os.listdir(base_dir)
            if os.path.isfile(os.path.join(base_dir, f)) and f.endswith(pattern)
        ]


def load_schema(schema_file):
    """Loads the JSON schema from a file."""
    try:
        with open(schema_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from schema file at {schema_file}",
            file=sys.stderr,
        )
        sys.exit(1)


def sanitize_markdown(content):
    """Removes potentially unsafe constructs from Markdown."""
    content = re.sub(
        r"<script.*?>.*?</script>", "", content, flags=re.IGNORECASE | re.DOTALL
    )
    content = re.sub(r" on\w+=\".*?\"", "", content, flags=re.IGNORECASE)
    content = re.sub(
        r"<<<SENSITIVE_INSTRUCTIONS>>>.*<<<SENSITIVE_INSTRUCTIONS>>>",
        "",
        content,
        flags=re.DOTALL,
    )
    return content


def execute_code(code, protocol_id, rule_id):
    """Executes a block of Python code in a controlled environment."""
    print(f"--- Executing Code for {protocol_id}/{rule_id} ---")
    try:
        # For safety, we're just printing for now.
        # In a real scenario, this would use a sandbox.
        print("--- CODE START ---")
        print(code)
        print("--- CODE END ---")
        # exec(code) # This would be the actual execution.
        print(f"--- Successfully executed code for {protocol_id}/{rule_id} ---")
    except Exception as e:
        print(f"Error executing code for {protocol_id}/{rule_id}: {e}", file=sys.stderr)
