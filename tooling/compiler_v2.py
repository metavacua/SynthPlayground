"""
A declarative, manifest-driven build system for compiling hierarchical AGENTS.md files.

This script represents the second generation of the protocol compilation system.
It replaces the fragile, file-system-based discovery of the original
`hierarchical_compiler.py` with a robust, declarative model driven by a
central manifest file (`protocols/hierarchy.yaml`).

The compiler operates in a single, logical pass:
1.  **Load Manifest:** It reads `protocols/hierarchy.yaml` to understand the
    explicitly defined module hierarchy and dependencies.
2.  **Build Modules:** It iterates through all modules defined in the manifest,
    compiling their protocol sources (`*.protocol.json` and `*.protocol.md`)
    into an in-memory representation.
3.  **Assemble Hierarchy:** Using the manifest's dependency graph, it
    recursively assembles the final AGENTS.md content for each module by
    injecting the compiled content of its children. This is done entirely in
    memory, avoiding the need for temporary files.
4.  **Write Artifacts:** It writes the final, assembled AGENTS.md files to their
    respective module directories.
5.  **Compile Knowledge Graph:** It performs a full scan of all `*.protocol.json`
    files and compiles them into a single, centralized RDF knowledge graph,
    preserving the semantic web capabilities of the previous system.
"""
import os
import sys
import json
import yaml  # PyYAML dependency
import re
import subprocess
from collections import defaultdict

# Ensure the project root is in the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from tooling import protocol_compiler

# --- Constants ---
HIERARCHY_MANIFEST_PATH = os.path.join(ROOT_DIR, "protocols", "hierarchy.yaml")
PROTOCOLS_DIR_NAME = "protocols"
AGENTS_MD_FILENAME = "AGENTS.md"
KNOWLEDGE_GRAPH_FILENAME = os.path.join(ROOT_DIR, "knowledge_core", "protocols.ttl")
PROTOCOL_SCHEMA_PATH = os.path.join(ROOT_DIR, "protocols", "protocol.schema.json")


class CompilerV2:
    """
    The main class for the new, manifest-driven protocol compiler.
    """

    def __init__(self, manifest_path):
        """
        Initializes the compiler with the path to the hierarchy manifest.
        """
        self.manifest_path = manifest_path
        self.hierarchy = self._load_manifest()
        self.compiled_modules = {} # To store in-memory compiled content

    def _load_manifest(self):
        """Loads and validates the hierarchy.yaml manifest."""
        print(f"Loading hierarchy manifest from: {self.manifest_path}")
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"Hierarchy manifest not found at {self.manifest_path}")
        with open(self.manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
        # Basic validation
        if 'root' not in manifest:
            raise ValueError("Manifest must contain a 'root' module definition.")
        print("Manifest loaded successfully.")
        return manifest

    def compile_all(self):
        """
        Orchestrates the entire compilation process.
        """
        print("\n--- Starting Compiler V2 ---")
        self._build_all_modules()
        self._assemble_and_write_artifacts()
        self._compile_knowledge_graph()
        print("\n--- Compiler V2 Finished ---")

    def _build_all_modules(self):
        """
        Compiles the source files for each module into an in-memory structure.
        It uses the existing `protocol_compiler` to generate the raw content
        for each module, which is then stored in `self.compiled_modules`.
        """
        print("\n--- Pass 1: Building all modules in-memory ---")
        for name, module_def in self.hierarchy.items():
            module_path = os.path.join(ROOT_DIR, module_def['path'])
            protocol_src_dir = os.path.join(module_path, PROTOCOLS_DIR_NAME)

            if not os.path.isdir(protocol_src_dir):
                print(f"  - Skipping module '{name}': No 'protocols' directory found.")
                continue

            print(f"  - Compiling module: '{name}' from {protocol_src_dir}")
            try:
                # Use the existing compiler to get the raw module content
                content = protocol_compiler.compile_protocols_to_string(
                    protocol_src_dir, PROTOCOL_SCHEMA_PATH
                )
                self.compiled_modules[name] = content
                print(f"    - Successfully compiled '{name}' in-memory.")
            except Exception as e:
                print(f"    - Error compiling module '{name}': {e}", file=sys.stderr)

    def _assemble_and_write_artifacts(self):
        """
        Assembles the final AGENTS.md files from the in-memory representations
        and writes them to disk using a recursive, top-down approach.
        """
        print("\n--- Pass 2: Assembling and writing artifacts ---")
        # A cache to store the fully assembled content of each module
        assembly_cache = {}

        # The recursive function to assemble content
        def get_assembled_content(module_name):
            if module_name in assembly_cache:
                return assembly_cache[module_name]

            # Start with the module's own compiled content
            if module_name not in self.compiled_modules:
                return "" # Should not happen if manifest is correct

            final_content = self.compiled_modules.get(module_name, "")

            # Recursively get content from children and append it
            module_def = self.hierarchy.get(module_name, {})
            children = module_def.get('children', [])
            for child_name in children:
                print(f"  - Assembling child '{child_name}' into parent '{module_name}'")
                child_content = get_assembled_content(child_name)

                # Add a clear header for the child module's section
                header = f"\n\n# --- Child Module: `{child_name}` ---\n"
                final_content += header + child_content

            assembly_cache[module_name] = final_content
            return final_content

        # Iterate through all modules and write their final, assembled AGENTS.md
        for name, module_def in self.hierarchy.items():
            module_path = os.path.join(ROOT_DIR, module_def['path'])
            target_filepath = os.path.join(module_path, AGENTS_MD_FILENAME)

            print(f"  - Generating final AGENTS.md for module: '{name}'")
            final_agents_md = get_assembled_content(name)

            try:
                with open(target_filepath, 'w') as f:
                    f.write(final_agents_md)
                print(f"    - Successfully wrote artifact to {target_filepath}")
            except Exception as e:
                print(f"    - Error writing artifact for '{name}': {e}", file=sys.stderr)

    def _compile_knowledge_graph(self):
        """
        Scans the entire repository for `*.protocol.json` files and compiles
        them into a single, centralized RDF knowledge graph in Turtle format.
        This logic is ported directly from the original hierarchical compiler.
        """
        print("\n--- Pass 3: Compiling centralized knowledge graph ---")
        try:
            from rdflib import Graph
            import jsonschema
        except ImportError:
            print("  - Error: rdflib or jsonschema not found. Please ensure dependencies are installed.", file=sys.stderr)
            return

        schema = json.load(open(PROTOCOL_SCHEMA_PATH))
        g = Graph()
        context_path = os.path.join(ROOT_DIR, "protocols", "protocol.context.jsonld")

        all_json_files = []
        for root, _, files in os.walk(ROOT_DIR):
            for file in files:
                if file.endswith(".protocol.json"):
                    all_json_files.append(os.path.join(root, file))

        print(f"  - Found {len(all_json_files)} protocol.json files for KG compilation.")

        for file_path in all_json_files:
            try:
                with open(file_path, "r") as f:
                    protocol_data = json.load(f)
                jsonschema.validate(instance=protocol_data, schema=schema)

                protocol_data_for_ld = protocol_data.copy()
                if os.path.exists(context_path):
                    # The context path needs to be relative for JSON-LD processing
                    relative_context_path = os.path.relpath(context_path, os.path.dirname(file_path))
                    protocol_data_for_ld["@context"] = relative_context_path
                    base_uri = "file://" + os.path.abspath(os.path.dirname(file_path)) + "/"
                    g.parse(
                        data=json.dumps(protocol_data_for_ld),
                        format="json-ld",
                        publicID=base_uri,
                    )
            except Exception as e:
                print(f"  - Warning: Failed to process {os.path.basename(file_path)} for KG: {e}", file=sys.stderr)

        # Serialize the final graph
        try:
            g.serialize(destination=KNOWLEDGE_GRAPH_FILENAME, format="turtle")
            print(f"  - Successfully generated knowledge graph at {KNOWLEDGE_GRAPH_FILENAME}")
        except Exception as e:
            print(f"  - Error: Failed to serialize centralized RDF graph: {e}", file=sys.stderr)


def main():
    """
    Main entry point for the script.
    """
    try:
        compiler = CompilerV2(HIERARCHY_MANIFEST_PATH)
        compiler.compile_all()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()