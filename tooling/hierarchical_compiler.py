"""
A hierarchical build system for compiling nested protocol modules.

This script orchestrates the compilation of `AGENTS.md` and `README.md` files
across a repository with a nested or hierarchical module structure. It is a key
component of the system's ability to manage complexity by allowing protocols to
be defined in a modular, distributed way while still being presented as a unified,
coherent whole at each level of the hierarchy.

The compiler operates in two main passes:

**Pass 1: Documentation Compilation (Bottom-Up)**
1.  **Discovery:** It finds all `protocols` directories in the repository, which
    signify the root of a documentation module.
2.  **Bottom-Up Traversal:** It processes these directories from the most deeply
    nested ones upwards. This ensures that child modules are always built before
    their parents.
3.  **Child Summary Injection:** For each compiled child module, it generates a
    summary of its protocols and injects this summary into the parent's
    `protocols` directory as a temporary file.
4.  **Parent Compilation:** When the parent module is compiled, the standard
    `protocol_compiler.py` automatically includes the injected child summaries,
    creating a single `AGENTS.md` file that contains both the parent's native
    protocols and the full protocols of all its direct children.
5.  **README Generation:** After each `AGENTS.md` is compiled, the corresponding
    `README.md` is generated.

**Pass 2: Centralized Knowledge Graph Compilation**
1.  After all documentation is built, it performs a full repository scan to find
    every `*.protocol.json` file.
2.  It parses all of these files and compiles them into a single, centralized
    RDF knowledge graph (`protocols.ttl`). This provides a unified,
    machine-readable view of every protocol defined anywhere in the system.

This hierarchical approach allows for both localized, context-specific protocol
definitions and a holistic, system-wide understanding of the agent's governing rules.
"""
import os
import sys
import json
import re

# Ensure the project root is in the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import subprocess
from tooling import protocol_compiler
from utils.file_system_utils import find_files, get_ignore_patterns
import fnmatch

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROTOCOLS_DIR_NAME = "protocols"
AGENTS_MD_FILENAME = "AGENTS.md"
README_FILENAME = "README.md"
SUMMARY_FILE_PREFIX = "_z_child_summary_"
SPECIAL_DIRS = [
    "protocols/security"
]  # Directories to be ignored by the hierarchical scan


def find_protocol_dirs(root_dir):
    """
    Finds all directories named 'protocols' within the root directory,
    ignoring any special-cased directories.
    """
    protocol_dirs = []
    dir_patterns, _ = get_ignore_patterns(root_dir)
    special_paths = {os.path.join(root_dir, d) for d in SPECIAL_DIRS}

    for dirpath, dirnames, _ in os.walk(root_dir):
        # Exclude ignored directories from traversal
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, p) for p in dir_patterns)]
        if PROTOCOLS_DIR_NAME in dirnames:
            proto_dir_path = os.path.join(dirpath, PROTOCOLS_DIR_NAME)
            if proto_dir_path in special_paths:
                print(f"Ignoring special directory: {proto_dir_path}")
                continue
            protocol_dirs.append(proto_dir_path)

    # Process from the deepest directories upwards to ensure children are built before parents
    return sorted(protocol_dirs, key=lambda x: -x.count(os.sep))


def run_system_doc_generator():
    """Invokes the doc_builder.py script to generate system docs."""
    doc_builder_script = os.path.join(ROOT_DIR, "tooling", "doc_builder.py")
    output_file = os.path.join(ROOT_DIR, "knowledge_core", "SYSTEM_DOCUMENTATION.md")

    command = [
        "python3",
        doc_builder_script,
        "--format", "system",
        "--output-file", output_file,
        "--source-dir", "tooling/",
        "--source-dir", "utils/"
    ]

    print("--- Generating System-Wide Documentation ---")
    print(f"Command: {' '.join(command)}")
    try:
        # Run with check=True to raise an exception on failure
        result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=ROOT_DIR)
        print(result.stdout)
        print(f"Successfully generated {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error generating system documentation:")
        print(e.stderr)
        # In a real build, we might want to exit here. For now, we return None.
        return None




def run_compiler(source_dir, doc_sources):
    """Invokes the protocol_compiler.py script as a library."""
    parent_dir = os.path.dirname(source_dir)
    target_agents_md = os.path.join(parent_dir, AGENTS_MD_FILENAME)
    schema_file = os.path.join(source_dir, "protocol.schema.json")
    if not os.path.exists(schema_file):
        # Fallback to the root schema if not found in the current protocol dir
        schema_file = os.path.join(ROOT_DIR, "protocols", "protocol.schema.json")

    print(f"Running AGENTS.md compiler for: {source_dir}")
    try:
        protocol_compiler.compile_protocols(
            source_dir,
            target_agents_md,
            schema_file,
            doc_sources=doc_sources
        )
        print(f"Successfully compiled {target_agents_md}")
        return target_agents_md
    except Exception as e:
        print(f"Error compiling AGENTS.md in {source_dir}:")
        print(e)
        # Re-raise to halt the build on error
        raise


def run_readme_generator(source_agents_md):
    """Invokes the doc_builder.py script to generate a README."""
    if not source_agents_md or not os.path.exists(source_agents_md):
        print(f"Warning: Source AGENTS.md not found. Cannot generate README.md.")
        return None

    parent_dir = os.path.dirname(source_agents_md)
    target_readme = os.path.join(parent_dir, README_FILENAME)
    doc_builder_script = os.path.join(ROOT_DIR, "tooling", "doc_builder.py")

    command = [
        "python3",
        doc_builder_script,
        "--format", "readme",
        "--source-file", source_agents_md,
        "--output-file", target_readme
    ]

    print(f"Running README generator for: {source_agents_md}")
    print(f"Command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, cwd=ROOT_DIR)
        print(f"Successfully generated {target_readme}")
        return target_readme
    except subprocess.CalledProcessError as e:
        print(f"Error generating README.md for {source_agents_md}:")
        print(e.stderr)
        return None


def generate_summary(child_agents_md_path):
    """
    Extracts the full, rendered protocol blocks from a child AGENTS.md file.
    This function finds all protocol definitions (human-readable markdown and
    the associated machine-readable JSON block) and concatenates them into a
    single string to be injected into the parent AGENTS.md.
    """
    if not child_agents_md_path or not os.path.exists(child_agents_md_path):
        return ""

    with open(child_agents_md_path, "r") as f:
        content = f.read()

    # Find all protocol blocks, which start with a header and end with a separator.
    # This regex captures the entire block from a header (e.g., #, ##) up to the
    # standard protocol separator '---'. This ensures that the full, unabridged
    # protocol text is captured for inclusion in the parent AGENTS.md.
    protocol_blocks = re.findall(r"(# Protocol:.*?---\n)", content, re.DOTALL)

    if not protocol_blocks:
        return ""

    child_dir_name = os.path.basename(os.path.dirname(child_agents_md_path))

    # Prepend a header to clearly mark the beginning of the child module's protocols.
    summary_md = f"# --- Child Module: `{child_dir_name}` ---\n\n"
    summary_md += "\n".join(protocol_blocks)

    return summary_md


def cleanup_summaries(directory):
    """Removes temporary summary files from a protocols directory."""
    if not os.path.isdir(directory):
        return
    for filename in os.listdir(directory):
        if filename.startswith(SUMMARY_FILE_PREFIX):
            os.remove(os.path.join(directory, filename))
            print(f"Cleaned up summary file: {filename}")


def get_parent_module(module_path, all_module_paths):
    """Finds the direct parent module of a given module."""
    parent_path = os.path.dirname(module_path)
    while len(parent_path) >= len(ROOT_DIR) and parent_path != "/":
        if parent_path in all_module_paths:
            return parent_path
        parent_path = os.path.dirname(parent_path)
    return None


def compile_centralized_knowledge_graph():
    """
    Finds all protocol.json files in the entire repository, loads them, and
    compiles them into a single, unified knowledge graph.
    """
    print("\n--- Starting Centralized Knowledge Graph Compilation ---")
    from rdflib import Graph
    import jsonschema

    schema_file = os.path.join(ROOT_DIR, "protocols", "protocol.schema.json")
    schema = json.load(open(schema_file))

    all_json_files = [os.path.join(ROOT_DIR, f) for f in find_files("*.protocol.json")]

    print(f"Found {len(all_json_files)} protocol.json files for KG compilation.")

    g = Graph()
    context_path = os.path.join(ROOT_DIR, "protocols", "protocol.context.jsonld")

    for file_path in all_json_files:
        try:
            with open(file_path, "r") as f:
                protocol_data = json.load(f)
            jsonschema.validate(instance=protocol_data, schema=schema)

            protocol_data_for_ld = protocol_data.copy()
            if os.path.exists(context_path):
                relative_context_path = os.path.relpath(
                    context_path, os.path.dirname(file_path)
                )
                protocol_data_for_ld["@context"] = relative_context_path
                base_uri = "file://" + os.path.abspath(os.path.dirname(file_path)) + "/"
                g.parse(
                    data=json.dumps(protocol_data_for_ld),
                    format="json-ld",
                    publicID=base_uri,
                )
        except Exception as e:
            print(
                f"  - Error: Failed to process {os.path.basename(file_path)} for KG: {e}"
            )

    # Serialize the final graph
    kg_file = os.path.join(ROOT_DIR, "knowledge_core", "protocols.ttl")
    try:
        g.serialize(destination=kg_file, format="turtle")
        print(f"Successfully generated centralized knowledge graph at {kg_file}")
    except Exception as e:
        print(f"Error serializing centralized RDF graph: {e}")

    print("--- Centralized Knowledge Graph Compilation Finished ---")


def main():
    """
    Main function to orchestrate the hierarchical compilation.
    """
    print("--- Starting Hierarchical Build ---")

    # --- Pre-computation: Generate all documentation that might be injected ---
    # This breaks the dependency on the Makefile's ordering, making the build
    # system more robust and self-contained.
    system_doc_path = run_system_doc_generator()
    # The root README is generated after the root AGENTS.md, so we just
    # define the path here for the compiler to use if a placeholder exists.
    root_readme_path = os.path.join(ROOT_DIR, README_FILENAME)
    kg_path = os.path.join(ROOT_DIR, "knowledge_core", "protocols.ttl")

    doc_sources = {
        "system": system_doc_path,
        "readme": root_readme_path,
        "kg": kg_path
    }

    all_protocol_dirs = find_protocol_dirs(ROOT_DIR)
    module_paths = [os.path.dirname(p) for p in all_protocol_dirs]

    compiled_artifacts = {}

    # --- Pass 1: Compile Documentation (AGENTS.md, README.md) ---
    for proto_dir in all_protocol_dirs:
        current_module_path = os.path.dirname(proto_dir)
        print(f"\n--- Processing Module: {current_module_path} ---")

        cleanup_summaries(proto_dir)

        # Inject summaries from children that have already been compiled
        for child_module_path, artifacts in compiled_artifacts.items():
            parent_module = get_parent_module(child_module_path, module_paths)
            if parent_module == current_module_path:
                print(f"Found compiled child: {child_module_path}. Generating summary.")
                summary_content = generate_summary(artifacts["agents_md"])
                if summary_content:
                    summary_filename = f"{SUMMARY_FILE_PREFIX}{os.path.basename(child_module_path)}.protocol.md"
                    summary_filepath = os.path.join(proto_dir, summary_filename)
                    with open(summary_filepath, "w") as f:
                        f.write(summary_content)
                    print(
                        f"Injected summary for '{child_module_path}' into {summary_filepath}"
                    )

        # Compile the current module's AGENTS.md, passing in the paths to all
        # potential documentation sources. The protocol_compiler will be responsible
        # for deciding which ones to use based on placeholders.
        target_agents_md = run_compiler(proto_dir, doc_sources)

        # Generate the corresponding README.md for the newly compiled AGENTS.md
        target_readme = run_readme_generator(target_agents_md)

        if target_agents_md:
            compiled_artifacts[current_module_path] = {
                "agents_md": target_agents_md,
                "readme": target_readme,
            }

    print("\n--- Hierarchical Build Summary ---")
    for module, artifacts in sorted(compiled_artifacts.items()):
        print(f"Module: {module}")
        agents_md_path = artifacts.get("agents_md")
        readme_path = artifacts.get("readme")
        if agents_md_path:
            print(f"  - Compiled: {os.path.relpath(agents_md_path, ROOT_DIR)}")
        if readme_path:
            print(f"  - Generated: {os.path.relpath(readme_path, ROOT_DIR)}")

    # --- Pass 2: Compile Centralized Knowledge Graph ---
    # This runs last, after all protocols have been compiled and validated.
    compile_centralized_knowledge_graph()

    print("\n--- Hierarchical Build Finished ---")


if __name__ == "__main__":
    main()
