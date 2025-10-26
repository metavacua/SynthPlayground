"""
A tool for managing the agent's contextual awareness by orchestrating various scanning and analysis tools.
"""

import argparse
import json
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description="Orchestrates context-gathering tools to build a knowledge graph."
    )
    parser.add_argument(
        "--output-dir",
        default="knowledge_core/context_outputs",
        help="The directory to store the outputs of the context-gathering tools.",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    dependency_graph_path = os.path.join(args.output_dir, "dependency_graph.json")
    symbol_map_path = os.path.join(args.output_dir, "symbol_map.json")
    knowledge_graph_path = os.path.join(args.output_dir, "knowledge_graph.json")
    enriched_knowledge_graph_path = os.path.join(
        "knowledge_core", "knowledge_graph.jsonld"
    )

    print("Running dependency graph generator...")
    subprocess.run(
        [
            "python",
            "tooling/dependency_graph_generator.py",
            "--output",
            dependency_graph_path,
        ]
    )

    print("Running symbol map generator...")
    subprocess.run(
        [
            "python",
            "tooling/symbol_map_generator.py",
            "--output",
            symbol_map_path,
        ]
    )

    print("Integrating outputs into a unified knowledge graph...")
    with open(dependency_graph_path, "r") as f:
        dependency_graph = json.load(f)
    with open(symbol_map_path, "r") as f:
        symbol_map = json.load(f)

    knowledge_graph = {
        "dependencies": dependency_graph,
        "symbols": symbol_map,
    }

    with open(knowledge_graph_path, "w") as f:
        json.dump(knowledge_graph, f, indent=2)

    print(f"Knowledge graph created at: {knowledge_graph_path}")

    print("Enriching knowledge graph with DBPedia data...")
    subprocess.run(
        [
            "python",
            "tooling/knowledge_integrator.py",
            "--input",
            knowledge_graph_path,
            "--output",
            enriched_knowledge_graph_path,
        ]
    )

    print(f"Enriched knowledge graph created at: {enriched_knowledge_graph_path}")


if __name__ == "__main__":
    main()
