#!/usr/bin/env python3
"""
Polymorphic AGENTS.md Generator

This script generates AGENTS.md files throughout the repository with
different content based on directory function, following the minimalistic
method where root has barebones context and subdirectories extend it.

All generated files are W3C semantic web compliant using JSON-LD structure.
"""

import os
import sys
import yaml
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PolymorphicAgentsMdGenerator:
    """Generates polymorphic AGENTS.md files based on directory context."""

    def __init__(self, project_root, mapping_config_path):
        self.project_root = project_root
        self.mapping_config_path = mapping_config_path
        self.mapping_config = self._load_mapping_config()
        self.all_protocols = {}  # Loaded from protocols.yaml-ld

    def _load_mapping_config(self):
        """Load the agents_md_mapping.yaml configuration."""
        try:
            with open(self.mapping_config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error(f"Failed to load mapping config: {e}")
            return {}

    def load_protocols(self):
        """Load all protocols from protocols.yaml-ld."""
        protocols_file = os.path.join(self.project_root, "protocols.yaml-ld")
        if not os.path.exists(protocols_file):
            logging.error(
                "protocols.yaml-ld not found. Run 'python3 tooling/builder.py --target protocols' first."
            )
            return False

        try:
            with open(protocols_file, "r") as f:
                data = yaml.safe_load(f)
                for item in data.get("@graph", []):
                    protocol_id = item.get("protocol_id", "").upper()
                    if protocol_id:
                        self.all_protocols[protocol_id] = item
        except Exception as e:
            logging.error(f"Failed to load protocols: {e}")
            return False

        return True

    def discover_directories(self):
        """Discover all directories that should have AGENTS.md files."""
        directories = []

        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and common exclusions
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["__pycache__", "node_modules", "venv", "env", ".git"]
            ]

            rel_path = os.path.relpath(root, self.project_root)
            if rel_path == ".":
                rel_path = "/"
            else:
                rel_path = "/" + rel_path

            directories.append(rel_path)

        # Determine which directories should get AGENTS.md
        result = []
        for directory in sorted(directories):
            if self._should_generate_agents_md(directory):
                result.append(directory)

        return result

    def _should_generate_agents_md(self, directory):
        """Determine if AGENTS.md should be generated for this directory."""
        # Explicitly listed directories always get AGENTS.md
        if directory in self.mapping_config:
            return True

        # Root always gets AGENTS.md
        if directory == "/":
            return True

        # Check if directory has meaningful content
        dir_path = directory[1:] if directory != "/" else ""
        full_path = os.path.join(self.project_root, dir_path)

        if not os.path.exists(full_path):
            return False

        # Count relevant files
        relevant_files = []
        if os.path.isdir(full_path):
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                if os.path.isfile(item_path):
                    if item.endswith(
                        (".py", ".md", ".yaml", ".json", ".js", ".ts", ".html", ".css")
                    ):
                        if not item.startswith("."):
                            relevant_files.append(item)

        # Generate AGENTS.md if directory has 3+ relevant files or is explicitly configured
        return len(relevant_files) >= 3

    def get_protocols_for_directory(self, directory):
        """Get protocols that apply to this directory."""
        if directory in self.mapping_config:
            return self.mapping_config[directory].get("protocols", [])
        elif "__default__" in self.mapping_config:
            return self.mapping_config["__default__"].get("protocols", [])
        else:
            return ["BEST-PRACTICES-001", "NON-COMPLIANCE-PROTOCOL-001"]

    def get_description_for_directory(self, directory):
        """Get description for this directory."""
        if directory in self.mapping_config:
            return self.mapping_config[directory].get(
                "description", f"Agent protocols for {directory}"
            )
        elif "__default__" in self.mapping_config:
            return self.mapping_config["__default__"].get(
                "description", f"Default protocols for {directory}"
            )
        else:
            return f"Agent protocols and operational directives for {directory}"

    def should_inherit_from_parent(self, directory):
        """Determine if this directory should inherit parent protocols."""
        if directory in self.mapping_config:
            return self.mapping_config[directory].get("inherits", True)
        return True

    def get_parent_directory(self, directory):
        """Get parent directory path."""
        if directory == "/":
            return None
        parent = os.path.dirname(directory)
        if parent == "":
            return "/"
        return parent

    def collect_protocols(self, directory):
        """Collect all protocols that apply to this directory (including inherited)."""
        protocols = set()

        # Get protocols for this directory
        dir_protocols = self.get_protocols_for_directory(directory)
        # Normalize to uppercase for case-insensitive lookup
        protocols.update([p.upper() for p in dir_protocols])

        # Inherit from parent if configured
        if self.should_inherit_from_parent(directory):
            parent = self.get_parent_directory(directory)
            if parent and self._should_generate_agents_md(parent):
                parent_protocols = self.get_protocols_for_directory(parent)
                # Normalize to uppercase for case-insensitive lookup
                protocols.update([p.upper() for p in parent_protocols])

        return sorted(list(protocols))

    def generate_agents_md(self, directory):
        """Generate AGENTS.md content for a specific directory."""
        description = self.get_description_for_directory(directory)
        protocols = self.collect_protocols(directory)

        # Filter protocols to only those that exist in the compiled protocols
        valid_protocols = []
        for protocol_id in protocols:
            if protocol_id in self.all_protocols:
                valid_protocols.append(protocol_id)
            else:
                logging.warning(
                    f"Protocol {protocol_id} not found for directory {directory}"
                )

        # Generate W3C semantic web compliant content
        content = self._generate_w3c_compliant_content(
            directory, description, valid_protocols
        )
        return content

    def _generate_w3c_compliant_content(self, directory, description, protocol_ids):
        """Generate W3C semantic web compliant content using JSON-LD."""
        # Get protocol details from compiled protocols
        protocols_data = []
        for protocol_id in protocol_ids:
            if protocol_id in self.all_protocols:
                protocol_data = self.all_protocols[protocol_id]
                protocols_data.append(protocol_data)

        # Create JSON-LD structured data
        jsonld_context = {
            "@context": "protocols/protocol.context.jsonld",
            "@type": "AgentContext",
            "directory": directory,
            "description": description,
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "protocols": protocols_data,
        }

        # Create markdown content with embedded JSON-LD
        content = f"""# AGENTS.md

**Directory:** `{directory}`
**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Description

{description}

## Protocols

This AGENTS.md file contains {len(protocol_ids)} operational protocols for this directory.

```yaml
{yaml.dump(jsonld_context, default_flow_style=False)}
```

## Protocol Summary

"""

        # Add protocol summaries
        for protocol_id in protocol_ids:
            if protocol_id in self.all_protocols:
                protocol = self.all_protocols[protocol_id]
                content += f"### {protocol_id}\n\n"
                description = protocol.get("description", "No description available.")
                content += f"{description}\n\n"

                # Add rules summary
                rules = protocol.get("rules", [])
                if rules:
                    content += "**Rules:**\n\n"
                    for i, rule in enumerate(rules[:3]):  # Show first 3 rules
                        rule_id = rule.get("rule_id", f"rule-{i+1}")
                        rule_desc = rule.get("description", "")
                        if rule_desc:
                            content += f"- `{rule_id}`: {rule_desc[:100]}...\n"
                    if len(rules) > 3:
                        content += f"- ... and {len(rules) - 3} more rules\n"
                    content += "\n"

        content += """## Notes

*This AGENTS.md file is a build artifact. Do not edit directly.*
*Make changes to source files in `protocols/` directory and regenerate.*

## Build Instructions

To regenerate this file, run:
```bash
python3 tooling/builder.py --target agents-md
```
"""

        return content

    def write_agents_md(self, directory, content):
        """Write AGENTS.md content to file."""
        try:
            dir_path = directory[1:] if directory != "/" else ""
            full_path = os.path.join(self.project_root, dir_path, "AGENTS.md")
            full_path = os.path.abspath(full_path)

            # Ensure parent directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w") as f:
                f.write(content)

            logging.info(f"Generated AGENTS.md for directory: {directory}")
            return True
        except Exception as e:
            logging.error(f"Failed to write AGENTS.md for {directory}: {e}")
            return False

    def generate_all(self):
        """Generate AGENTS.md for all applicable directories."""
        if not self.load_protocols():
            return False

        directories = self.discover_directories()
        logging.info(f"Discovered {len(directories)} directories that need AGENTS.md")

        success_count = 0
        for directory in directories:
            try:
                content = self.generate_agents_md(directory)
                if self.write_agents_md(directory, content):
                    success_count += 1
            except Exception as e:
                logging.error(f"Failed to generate AGENTS.md for {directory}: {e}")

        logging.info(f"Successfully generated {success_count} AGENTS.md files")
        return success_count > 0


def main():
    """Main entry point."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    mapping_config_path = os.path.join(project_root, "agents_md_mapping.yaml")

    generator = PolymorphicAgentsMdGenerator(project_root, mapping_config_path)

    if generator.generate_all():
        return 0
    else:
        logging.error("Failed to generate AGENTS.md files")
        return 1


if __name__ == "__main__":
    sys.exit(main())
