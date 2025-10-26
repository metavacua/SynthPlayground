import os
import json

def extract_json_from_md(md_content):
    """
    Extracts the first JSON block from a Markdown string.

    Args:
        md_content: The string content of the Markdown file.

    Returns:
        The extracted JSON string, or None if no JSON block is found.
    """
    in_json_block = False
    json_lines = []
    for line in md_content.splitlines():
        if line.strip() == "```json":
            in_json_block = True
            continue
        if line.strip() == "```" and in_json_block:
            break
        if in_json_block:
            json_lines.append(line)

    if json_lines:
        return "".join(json_lines)
    return None

def main():
    """
    Finds all Markdown files in the 'protocols' directory,
    extracts JSON from them, and saves it to new files.
    """
    for root, _, files in os.walk("protocols"):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r") as f:
                    content = f.read()

                json_content = extract_json_from_md(content)

                if json_content:
                    try:
                        # Validate that it's proper JSON
                        json.loads(json_content)

                        new_filename = os.path.splitext(filepath)[0] + ".json"
                        with open(new_filename, "w") as f:
                            f.write(json_content)
                        print(f"Extracted JSON from {filepath} to {new_filename}")
                    except json.JSONDecodeError:
                        print(f"Could not decode JSON from {filepath}")

if __name__ == "__main__":
    main()
