"""
This module defines the WitnessRegistry, a core component of the Categorical Reasoning Engine.
Its purpose is to discover, load, and provide access to the formal "witnesses" that
define the objects in the Category of Formal Languages (CatFormLang).
"""

import os
import json
from typing import Dict, Any

class WitnessRegistry:
    """
    Scans a directory for witness metadata files and loads them into a machine-readable registry.
    """

    def __init__(self, root_dir: str = '.'):
        self.root_dir = root_dir
        self.witnesses: Dict[str, Any] = {}

    def scan(self, verbose=False) -> None:
        """
        Scans the repository for witness.json files and loads them.
        """
        for root, _, files in os.walk(self.root_dir):
            if 'witness.json' in files:
                filepath = os.path.join(root, 'witness.json')
                try:
                    with open(filepath, 'r') as f:
                        metadata = json.load(f)

                    key = os.path.basename(root)
                    self.witnesses[key] = metadata
                    if verbose:
                        print(f"Loaded witness: {key}")

                except json.JSONDecodeError:
                    if verbose:
                        print(f"Warning: Could not parse witness file at {filepath}")

        if verbose:
            print(f"Witness registry scan complete. Found {len(self.witnesses)} witnesses.")

    def get_witness(self, name: str) -> Dict[str, Any]:
        """
        Retrieves a specific witness by its name.
        """
        return self.witnesses.get(name)

    def list_witnesses(self) -> list:
        """
        Returns a list of all loaded witness names.
        """
        return list(self.witnesses.keys())

if __name__ == '__main__':
    registry = WitnessRegistry()
    registry.scan(verbose=True)
    print("\n--- Loaded Witnesses ---")
    for name in registry.list_witnesses():
        print(f"- {name}")
    print("------------------------")
