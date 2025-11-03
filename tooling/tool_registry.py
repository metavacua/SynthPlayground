"""
This module defines the ToolRegistry, a component of the Categorical Reasoning Engine.
It discovers, loads, and provides access to general-purpose tools that are not
formal morphisms, such as external API callers or services.
"""

import os
import json
from typing import Dict, Any

class ToolRegistry:
    """
    Scans a directory for tool metadata files (*.tool.json) and loads them.
    """

    def __init__(self, root_dir: str = 'tooling'):
        self.root_dir = root_dir
        self.tools: Dict[str, Any] = {}

    def scan(self, verbose=False) -> None:
        """
        Scans the repository for *.tool.json files and loads them.
        """
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('tool.json'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            metadata = json.load(f)

                        name = metadata.get('name')
                        if not name:
                            if verbose:
                                print(f"Warning: Missing 'name' in tool metadata at {filepath}")
                            continue

                        self.tools[name] = metadata
                        if verbose:
                            print(f"Loaded tool: {name}")

                    except json.JSONDecodeError:
                        if verbose:
                            print(f"Warning: Could not parse tool metadata at {filepath}")

        if verbose:
            print(f"Tool registry scan complete. Found {len(self.tools)} tools.")

    def get_tool(self, name: str) -> Dict[str, Any]:
        """
        Retrieves a specific tool by its name.
        """
        return self.tools.get(name)

    def find_tool_by_capability(self, capability: str) -> Dict[str, Any]:
        """
        Finds a tool that provides a specific capability.
        """
        for tool in self.tools.values():
            if tool.get('capability') == capability:
                return tool
        return None

if __name__ == '__main__':
    registry = ToolRegistry()
    registry.scan(verbose=True)
    print("\n--- Loaded Tools ---")
    for name, data in registry.tools.items():
        print(f"- {name}: Capability: {data.get('capability')}")
    print("--------------------")
