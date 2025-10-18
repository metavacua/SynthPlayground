import os
import glob
import yaml
import argparse
import json

def compile_aal(source_dir, target_file, interface_file="jules.interface.json"):
    """
    Reads all .aal files from the source directory, parses them, and compiles them
    into a target markdown file, integrating agent-specific usage instructions.
    """
    output_filename = os.path.basename(target_file)
    print(f"--- Starting AAL Protocol Compilation for {output_filename} ---")
    print(f"Source directory: {source_dir}")
    print(f"Target file: {target_file}")

    all_aal_files = sorted(glob.glob(os.path.join(source_dir, "*.aal")))

    if not all_aal_files:
        print(f"Warning: No .aal files found in {source_dir}.")
        with open(target_file, "w") as f:
            f.write("# No AAL protocols found.")
        return

    print(f"Found {len(all_aal_files)} AAL protocol files.")

    # Load the agent interface file
    agent_interface = {}
    if os.path.exists(interface_file):
        try:
            with open(interface_file, "r") as f:
                agent_interface = json.load(f)
            print(f"Loaded agent interface from {interface_file}")
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {interface_file}. Proceeding without it.")
    else:
        print(f"Warning: Agent interface file not found at {interface_file}. Proceeding without it.")


    final_content = []

    for file_path in all_aal_files:
        print(f"  - Processing: {os.path.basename(file_path)}")
        with open(file_path, "r") as f:
            content = f.read()

        # Check if the file starts with YAML frontmatter
        if content.startswith('---'):
            # Find the end of the frontmatter
            end_frontmatter = content.find('---', 3)
            if end_frontmatter != -1:
                yaml_frontmatter = content[3:end_frontmatter]
                markdown_content = content[end_frontmatter+3:].strip()
                try:
                    protocol_data = yaml.safe_load(yaml_frontmatter)
                    if protocol_data: # Ensure there is data to process
                        final_content.append(f"# Protocol: {protocol_data.get('protocol_id', 'N/A')}")
                        if 'description' in protocol_data:
                            final_content.append(f"_{protocol_data['description'].strip()}_")
                        final_content.append("\n")

                        for rule in protocol_data.get('rules', []):
                            final_content.append(f"## Rule: `{rule.get('rule_id', 'N/A')}`")
                            if 'description' in rule:
                                final_content.append(f"**Description**: {rule['description'].strip()}")
                            if 'enforcement' in rule:
                                final_content.append(f"**Enforcement**: {rule['enforcement'].strip()}")
                            final_content.append("\n")

                        if 'associated_tools' in protocol_data:
                            final_content.append(f"**Associated Tools**: `{'`, `'.join(protocol_data.get('associated_tools', []))}`")

                            # Add agent-specific usage instructions
                            for tool_path in protocol_data['associated_tools']:
                                if tool_path in agent_interface:
                                    interface = agent_interface[tool_path]
                                    final_content.append("\n### Jules Usage\n")
                                    final_content.append(f"To use this tool, call the `{interface['agent_tool']}` tool with the following command:")
                                    final_content.append(f"```bash\n{interface['command_template'].format(tool_path=tool_path, args='<args>')}\n```")


                        final_content.append("\n---\n")

                    if markdown_content:
                        final_content.append("## Additional Information\n")
                        final_content.append(markdown_content)
                        final_content.append("\n---\n")

                except yaml.YAMLError as e:
                    print(f"    - Warning: Could not parse YAML from {os.path.basename(file_path)}. Treating as plain markdown. Error: {e}")
                    # If parsing fails, just treat the whole file as markdown
                    final_content.append(content)
            else:
                # It starts with '---' but doesn't have a closing '---'. Treat as markdown.
                final_content.append(content)
        else:
            # No frontmatter, just append the whole content
            final_content.append(content)
            final_content.append("\n---\n")


    # Write the final markdown content
    with open(target_file, "w") as f:
        f.write("\n".join(final_content))

    print(f"\n--- {output_filename} Compilation Successful ---")
    print(f"Successfully generated new {output_filename} file.")


def main_cli():
    """Main function to run the compiler from the command line."""
    parser = argparse.ArgumentParser(
        description="Compiles AAL protocol files into a single AGENTS.md document."
    )
    parser.add_argument(
        "--source-dir",
        default="protocols.aal",
        help="Directory containing the AAL protocol source files.",
    )
    parser.add_argument(
        "--output-file",
        default="AGENTS.md",
        help="Path for the output AGENTS.md file.",
    )

    args = parser.parse_args()

    compile_aal(
        source_dir=args.source_dir,
        target_file=args.output_file,
    )

if __name__ == "__main__":
    main_cli()