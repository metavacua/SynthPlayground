import os
from compiler import compile_protocols

def find_protocol_directories(root_path: str):
    """
    Finds all directories named 'protocols' within the repository,
    ignoring specified directories like '.git'.
    """
    protocol_dirs = []
    ignore_dirs = ['.git', '.github', 'archive', 'knowledge_core', 'tests']
    for root, dirs, _ in os.walk(root_path):
        # Modify dirs in-place to prune the search
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        if 'protocols' in dirs:
            protocol_dirs.append(os.path.join(root, 'protocols'))
    return protocol_dirs

def run_hierarchical_compilation(root_path: str):
    """
    Runs the protocol compiler on every 'protocols' directory found.
    """
    print("Starting hierarchical protocol compilation...")

    # First, compile the root protocols directory
    root_protocol_dir = os.path.join(root_path, 'protocols')
    if os.path.isdir(root_protocol_dir):
        print("\n--- Compiling Root Protocols ---")
        output_file = os.path.join(root_path, 'AGENTS.md')
        compile_protocols(root_protocol_dir, output_file)
    else:
        print("\n--- No Root Protocols Directory Found ---")


    # Then, find and compile all nested protocol directories
    # We search from the root_path to find directories containing a 'protocols' subdir
    for dirpath, dirnames, _ in os.walk(root_path):
        if 'protocols' in dirnames:
            # We are in a directory that has a 'protocols' subdirectory
            # e.g., dirpath could be './core'
            protocol_src_dir = os.path.join(dirpath, 'protocols')
            output_file = os.path.join(dirpath, 'AGENTS.md')

            # We don't want to re-compile the root directory
            if os.path.samefile(protocol_src_dir, root_protocol_dir):
                continue

            print(f"\n--- Compiling Nested Protocols: {protocol_src_dir} ---")
            compile_protocols(protocol_src_dir, output_file)


from knowledge_graph_generator import generate_knowledge_graph

if __name__ == '__main__':
    # Run the compilation process starting from the repository root.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # First, run the AGENTS.md compilation
    run_hierarchical_compilation(repo_root)
    print("\n--- Hierarchical Compilation Complete ---")

    # Then, generate the knowledge graph
    output_ttl_file = os.path.join(repo_root, 'protocols.ttl')
    generate_knowledge_graph(repo_root, output_ttl_file)
    print("\n--- Knowledge Graph Generation Complete ---")