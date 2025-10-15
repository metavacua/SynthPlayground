import os
import sys

def main():
    """
    Compiles all markdown files from the 'protocols/' directory into a single
    AGENTS.md file in the repository root.
    """
    try:
        # Get the absolute path of the repository root
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        protocols_dir = os.path.join(root_dir, "protocols")
        output_file_path = os.path.join(root_dir, "AGENTS.md")

        if not os.path.isdir(protocols_dir):
            print(f"Error: Source directory '{protocols_dir}' not found.", file=sys.stderr)
            print("Please create it and add protocol source files.", file=sys.stderr)
            sys.exit(1)

        # Get all .md files and sort them alphabetically to ensure correct order
        protocol_files = sorted([f for f in os.listdir(protocols_dir) if f.endswith('.md')])

        if not protocol_files:
            print(f"Warning: No protocol files found in '{protocols_dir}'. AGENTS.md will be empty.", file=sys.stderr)
            # Create an empty AGENTS.md
            open(output_file_path, 'w').close()
            return

        # Read and concatenate the content of each file
        full_protocol_content = ""
        for filename in protocol_files:
            filepath = os.path.join(protocols_dir, filename)
            with open(filepath, 'r') as f:
                # Add a newline to ensure separation between file contents
                full_protocol_content += f.read() + "\n"

        # Write the combined content to the output file
        with open(output_file_path, 'w') as f:
            f.write(full_protocol_content.strip())

        print(f"Successfully compiled {len(protocol_files)} protocol file(s) into '{output_file_path}'.")

    except Exception as e:
        print(f"An error occurred during protocol compilation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()