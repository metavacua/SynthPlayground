import os
import yaml
import argparse

# --- Static Content ---

# A new template focused on specification (Propositions and Prerequisites)
README_TEMPLATE = """
# Module Specification: `{module_name}`

This document outlines the formal specification for the `{module_name}` module, as defined by the proof-theoretic build system.

## 1. Propositions (Goals)

This module makes the following formal claims, which are proven by its successful build:

{propositions}

## 2. Prerequisites (Dependencies)

To prove its propositions, this module requires the following artifacts to be provided as inputs. These are the verified conclusions of its child modules.

{prerequisites}
"""

# --- Dynamic Content Generation ---

def generate_specification_readme(agents_md_path: str) -> str:
    """
    Parses a YAML-based AGENTS.md file to generate a specification-focused README.md.
    """
    if not os.path.exists(agents_md_path):
        return f"_Error: Sequent file `{agents_md_path}` not found._"

    try:
        with open(agents_md_path, "r", encoding="utf-8") as f:
            sequent_data = yaml.safe_load(f).get("sequent", {})
    except (IOError, yaml.YAMLError) as e:
        return f"_Error reading or parsing `{agents_md_path}`: {e}_"

    # --- Propositions Section ---
    succedent = sequent_data.get("succedent", [])
    propositions_parts = []
    if not succedent:
        propositions_parts.append("- This module makes no formal propositions.")
    else:
        for item in succedent:
            propositions_parts.append(f"- **{item.get('id', 'N/A')}**: {item.get('proposition', 'No proposition stated.')} (Produces artifact `{item.get('witness', 'N/A')}` of type `{item.get('type', 'N/A')}`)")

    propositions_md = "\n".join(propositions_parts)

    # --- Prerequisites Section ---
    antecedent = sequent_data.get("antecedent", [])
    prerequisites_parts = []
    if not antecedent:
        prerequisites_parts.append("- This module has no prerequisites; it is an axiom.")
    else:
        for item in antecedent:
            prerequisites_parts.append(f"- **{item.get('id', 'N/A')}**: Requires artifact `{item.get('witness', 'N/A')}` from module `{item.get('source', 'N/A')}`.")

    prerequisites_md = "\n".join(prerequisites_parts)

    module_name = os.path.basename(os.path.dirname(agents_md_path))
    if not module_name: # Handle root directory case
        module_name = "Repository Root"

    return README_TEMPLATE.format(
        module_name=module_name,
        propositions=propositions_md,
        prerequisites=prerequisites_md
    ).strip()


# --- Main Execution Logic ---

def main():
    """
    Main function to generate the specification README.md content and write it to a file.
    """
    parser = argparse.ArgumentParser(description="Generates a specification README.md from a YAML-based AGENTS.md sequent file.")
    parser.add_argument(
        "--source-file",
        required=True,
        help="Path to the source AGENTS.md sequent file."
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path for the output README.md file."
    )
    args = parser.parse_args()

    module_path = os.path.dirname(args.output_file)
    print(f"--- Generating Specification README.md for module: {module_path} ---")

    print(f"--> Parsing sequent from {args.source_file}...")
    final_readme_content = generate_specification_readme(args.source_file)

    print(f"--> Writing specification to {args.output_file}...")
    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(final_readme_content)
        print("--> Specification README.md generated successfully.")
    except IOError as e:
        print(f"Error: Could not write to {args.output_file}. Reason: {e}")


if __name__ == "__main__":
    main()