import os


def build_protocol(source_dir="protocol_sources", output_file="AGENTS.md"):
    """
    Reads all markdown files from the specified source directory,
    concatenates them in alphabetical order, and writes the
    result to the specified output file.
    """
    protocol_parts = []

    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        return

    files = sorted([f for f in os.listdir(source_dir) if f.endswith(".md")])

    if not files:
        print(f"No markdown files found in '{source_dir}'.")
        return

    for filename in files:
        with open(os.path.join(source_dir, filename), "r") as f:
            protocol_parts.append(f.read())

    # Add a newline between parts to ensure proper separation
    full_protocol = "\n\n".join(protocol_parts)

    with open(output_file, "w") as f:
        f.write(full_protocol)

    print(f"Successfully built {output_file} from {len(files)} source files.")


if __name__ == "__main__":
    build_protocol()
