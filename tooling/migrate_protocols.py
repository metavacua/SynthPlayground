import os
import re
import json

def migrate_protocols(source_dir):
    """
    Parses an old AGENTS.md file and migrates its content to .protocol.json
    and .protocol.md files.
    """
    agents_md_path = os.path.join(source_dir, "AGENTS.md")
    if not os.path.exists(agents_md_path):
        print(f"No AGENTS.md found in {source_dir}. Skipping.")
        return

    with open(agents_md_path, "r") as f:
        content = f.read()

    # Split the file into individual protocol blocks
    # A protocol block starts with a header like "## Protocol: FDC-001"
    # and ends with "---"
    protocol_blocks = re.split(r'\n---\n', content)

    for block in protocol_blocks:
        if not block.strip():
            continue

        # Extract protocol ID
        id_match = re.search(r'## Protocol: `([A-Z0-9-]+)`', block)
        if not id_match:
            continue
        protocol_id = id_match.group(1).lower()

        # Extract description
        desc_match = re.search(r'\*\*Description\*\*: (.*?)\n', block)
        description = desc_match.group(1) if desc_match else ""

        # The rest of the block is the markdown content
        # We remove the header and description to get the pure markdown
        md_content = re.sub(r'## Protocol: `([A-Z0-9-]+)`\n', '', block)
        md_content = re.sub(r'\*\*Description\*\*: (.*?)\n', '', md_content)
        md_content = md_content.strip()

        # Extract JSON from the block
        json_match = re.search(r'```json\n({.*?})\n```', block, re.DOTALL)
        if json_match:
            json_data = json.loads(json_match.group(1))
            # Remove the json block from the markdown content
            md_content = md_content.replace(json_match.group(0), "").strip()
        else:
            # If no JSON block, create a default one
            json_data = {
                "protocol_id": protocol_id,
                "description": description,
                "rules": [], # This will need to be manually populated if not in json
                "associated_tools": []
            }


        # Write the .protocol.json file
        json_filename = os.path.join(source_dir, f"{protocol_id}.protocol.json")
        with open(json_filename, "w") as f:
            json.dump(json_data, f, indent=2)

        # Write the .protocol.md file
        if md_content:
            md_filename = os.path.join(source_dir, f"{protocol_id}.protocol.md")
            with open(md_filename, "w") as f:
                f.write(md_content)

if __name__ == "__main__":
    protocol_dirs = ["protocols/compliance", "protocols/core", "protocols/critic", "protocols/security"]
    for d in protocol_dirs:
        print(f"Migrating protocols in {d}...")
        migrate_protocols(d)
    print("Migration complete.")