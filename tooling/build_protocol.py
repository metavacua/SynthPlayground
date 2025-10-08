import os
import shutil

SAFE_MODE_PROTOCOL_PATH = "AGENTS.safe.md"


def build_protocol(source_dir="protocol_sources", output_file="AGENTS.md"):
    """
    Reads all markdown files from the source directory, concatenates them
    in alphabetical order, and writes the result to the output file.

    If any part of this process fails, it copies the contents of
    AGENTS.safe.md to the output file as a fallback.
    """
    try:
        protocol_parts = []

        if not os.path.isdir(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' not found.")

        files = sorted([f for f in os.listdir(source_dir) if f.endswith(".md")])

        if not files:
            raise FileNotFoundError(f"No markdown files found in '{source_dir}'.")

        for filename in files:
            with open(os.path.join(source_dir, filename), "r") as f:
                protocol_parts.append(f.read())

        full_protocol = "\n\n".join(protocol_parts)

        with open(output_file, "w") as f:
            f.write(full_protocol)

        print(f"Successfully built {output_file} from {len(files)} source files.")

    except Exception as e:
        print(f"--- PROTOCOL BUILD FAILED: {e} ---")
        print(
            "Entering SAFE MODE. "
            f"Copying '{SAFE_MODE_PROTOCOL_PATH}' to '{output_file}'."
        )
        try:
            shutil.copyfile(SAFE_MODE_PROTOCOL_PATH, output_file)
            print("Safe mode protocol successfully activated.")
        except Exception as copy_e:
            print("--- CATASTROPHIC FAILURE: COULD NOT ACTIVATE SAFE MODE ---")
            print(f"Failed to copy safe mode protocol: {copy_e}")
            # Exit with a non-zero code to halt any CI/CD pipelines
            exit(1)


if __name__ == "__main__":
    build_protocol()