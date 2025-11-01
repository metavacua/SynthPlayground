"""
A tool to migrate protocols from the old, manual AGENTS.md format to the new,
structured, and compiler-friendly format.

This script is designed to be a one-time migration utility that helps to
transition the valuable, detailed protocols from the original AGENTS.md file
into a format that can be processed by the new, dynamic build system.

The tool works by:
1.  Reading the `AGENTS.md.bak` file, which is a backup of the original.
2.  Parsing the file to identify the distinct protocol sections (Phase 1-6 and
    the "STANDING ORDER").
3.  Creating a new `protocols/manual_protocol/` directory to house the
    migrated protocols.
4.  Writing each extracted protocol into its own formatted Markdown file within
    the new directory.

This ensures that the protocols are preserved and integrated into the new
system without requiring manual copying and pasting.
"""

import os
import re


def main():
    """
    Main function to run the protocol migration.
    """
    print("--- Starting Protocol Migration ---")

    # --- Configuration ---
    backup_file = "AGENTS.md.bak"
    output_dir = "protocols/manual_protocol"

    if not os.path.exists(backup_file):
        print(f"Error: Backup file '{backup_file}' not found. Aborting.")
        return

    # --- Read the Backup File ---
    with open(backup_file, "r") as f:
        content = f.read()

    # --- Create Output Directory ---
    os.makedirs(output_dir, exist_ok=True)
    print(f"Ensured output directory exists: '{output_dir}'")

    # --- Extract and Write Protocols ---
    # The protocols are defined by "Phase X" headers and the "STANDING ORDER"
    # We will split the content by these headers and process each section.
    sections = re.split(
        r"(Phase \d:.*?|STANDING ORDER - RAG MANDATE \(REVISED\))", content
    )

    # The first element is the content before the first match, which we can ignore.
    # The matched delimiters will be at odd indices, and the content at even indices.
    protocol_sections = {}
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        body = sections[i + 1].strip()
        protocol_sections[header] = body

    for header, body in protocol_sections.items():
        # Sanitize the header to create a valid filename
        filename = (
            header.lower()
            .replace(" ", "_")
            .replace(":", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            + ".md"
        )
        filepath = os.path.join(output_dir, filename)

        # Write the content to the new file
        with open(filepath, "w") as f:
            f.write(
                f"""# {header.replace(':', '')}

{body}"""
            )

        print(f"Successfully migrated protocol '{header}' to '{filepath}'")

    print("--- Protocol Migration Finished ---")


if __name__ == "__main__":
    main()
