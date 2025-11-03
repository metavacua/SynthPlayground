"""
This module defines the RefactoringRegistry, a component of the Categorical Reasoning Engine.
It discovers, loads, and provides access to the formal "morphisms" (refactoring tools)
that define the transformations between objects in CatFormLang.
"""

import os
import json
from typing import Dict, Any, List

class RefactoringRegistry:
    """
    Scans a directory for refactoring metadata files (refactor.json) and builds a graph of morphisms.
    """

    def __init__(self, root_dir: str = 'tooling'):
        self.root_dir = root_dir
        self.morphisms: Dict[str, Any] = {}

    def scan(self, verbose=False) -> None:
        """
        Scans the repository for refactor.json files and loads them.
        """
        for root, _, files in os.walk(self.root_dir):
            if 'refactor.json' in files:
                filepath = os.path.join(root, 'refactor.json')
                try:
                    with open(filepath, 'r') as f:
                        metadata = json.load(f)

                    name = metadata.get('name')
                    if not name:
                        if verbose:
                            print(f"Warning: Missing 'name' in refactoring metadata at {filepath}")
                        continue

                    self.morphisms[name] = metadata
                    if verbose:
                        print(f"Loaded morphism: {name}")

                except json.JSONDecodeError:
                    if verbose:
                        print(f"Warning: Could not parse refactoring metadata at {filepath}")

        if verbose:
            print(f"Refactoring registry scan complete. Found {len(self.morphisms)} morphisms.")

    def find_morphism(self, source_class: str, target_class: str) -> Dict[str, Any]:
        """
        Finds a morphism that transforms a source class to a target class.
        """
        for morphism in self.morphisms.values():
            if morphism.get('source') == source_class and morphism.get('target') == target_class:
                return morphism
        return None

if __name__ == '__main__':
    registry = RefactoringRegistry()
    registry.scan(verbose=True)
    print("\n--- Loaded Morphisms ---")
    for name, data in registry.morphisms.items():
        print(f"- {name}: {data.get('source')} -> {data.get('target')}")
    print("------------------------")
