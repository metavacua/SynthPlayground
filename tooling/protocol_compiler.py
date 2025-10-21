import json
import argparse


def compile_agents_md(human_readable_file, machine_readable_file, output_file):
    """
    Combines a human-readable Markdown file and a machine-readable JSON-LD
    protocol into a single AGENTS.md file.
    """
    try:
        with open(human_readable_file, "r") as f:
            human_content = f.read()
    except FileNotFoundError:
        print(f"Error: Human-readable file not found at {human_readable_file}")
        return

    try:
        with open(machine_readable_file, "r") as f:
            machine_content = json.load(f)
    except FileNotFoundError:
        print(f"Error: Machine-readable file not found at {machine_readable_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {machine_readable_file}")
        return

    # Combine the content
    # The final AGENTS.md will contain the human-readable part, followed by
    # the machine-readable part in a JSON block.
    combined_content = (
        f"{human_content}\n\n"
        "## Machine-Readable Protocol\n\n"
        "The following is a machine-readable protocol that defines the available commands.\n"
        "Agents should parse this protocol to understand the available actions.\n\n"
        "```json\n"
        f"{json.dumps(machine_content, indent=2)}\n"
        "```\n"
    )

    try:
        with open(output_file, "w") as f:
            f.write(combined_content)
        print(
            f"Successfully compiled {output_file} from {human_readable_file} and {machine_readable_file}"
        )
    except IOError as e:
        print(f"Error writing to output file {output_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Compile the AGENTS.md file from human- and machine-readable sources."
    )
    parser.add_argument(
        "--human-readable-file",
        required=True,
        help="The path to the human-readable Markdown source file.",
    )
    parser.add_argument(
        "--machine-readable-file",
        required=True,
        help="The path to the machine-readable JSON-LD protocol file.",
    )
    parser.add_argument(
        "--output-file", required=True, help="The path to the output AGENTS.md file."
    )
    args = parser.parse_args()

    compile_agents_md(
        args.human_readable_file, args.machine_readable_file, args.output_file
    )


if __name__ == "__main__":
    main()
