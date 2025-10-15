import os
import re
import argparse
import sys
import shutil

def sanitize_filename(name):
    """
    Sanitizes a string to be used as a valid filename.
    Removes special characters and replaces spaces with underscores.
    """
    name = name.lower()
    # Remove the leading number and period if they exist (e.g., "1. " or "1a. ")
    name = re.sub(r'^\d+[a-z]?\.\s*', '', name)
    name = re.sub(r'[^a-z0-9\s_-]', '', name)
    name = re.sub(r'[\s-]+', '_', name)
    return name

def decompile_protocol(input_filepath, output_dir):
    """
    Decompiles a monolithic AGENTS.md file into smaller, numbered protocol files.

    The file is split based on H2 (##) and H3 (###) markdown headers.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found at '{input_filepath}'", file=sys.stderr)
        sys.exit(1)

    # Ensure the output directory is clean before decompiling
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with open(input_filepath, 'r') as f:
        content = f.read()

    # Split the content by H2 and H3 headers, keeping the headers.
    # The regex looks for '## ' or '### ' at the beginning of a line.
    sections = re.split(r'(?m)^(## |### )', content)

    # The first element is the content before the first header (the introduction).
    intro_content = sections.pop(0).strip()
    if intro_content:
        with open(os.path.join(output_dir, "00_introduction.md"), 'w') as f:
            f.write(intro_content)
        print("Created 00_introduction.md")

    # The rest of the list is pairs of (header_marker, section_content)
    file_counter = 1
    # We iterate through the rest of the sections, taking them in pairs
    for i in range(0, len(sections), 2):
        header_marker = sections[i]
        section_body = sections[i+1]

        # The first line of the body is the header title.
        header_title = section_body.split('\n', 1)[0].strip()

        # Combine the marker and title to form the full header for the file content.
        full_header = f"{header_marker}{header_title}"

        # The rest of the body is the content.
        section_content = ""
        if '\n' in section_body:
            section_content = section_body.split('\n', 1)[1].strip()

        # Create a sanitized filename
        sanitized_title = sanitize_filename(header_title)
        filename = f"{file_counter:02d}_{sanitized_title}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as f:
            f.write(f"{full_header}\n\n{section_content}".strip())

        print(f"Created {filename}")
        file_counter += 1

    print(f"\nDecompilation complete. {file_counter-1} file(s) created in '{output_dir}'.")

def main():
    parser = argparse.ArgumentParser(description="Decompile a monolithic AGENTS.md file into a structured directory of protocol source files.")
    parser.add_argument(
        "input_file",
        default="AGENTS.md",
        nargs='?',
        help="The path to the monolithic AGENTS.md file to decompile. Defaults to 'AGENTS.md'."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="protocols",
        help="The directory to save the decomposed protocol files. Defaults to 'protocols'."
    )
    args = parser.parse_args()

    decompile_protocol(args.input_file, args.output_dir)

if __name__ == "__main__":
    main()