
import argparse
import os
from yaml_ld import to_rdf
from rdflib import ConjunctiveGraph
import yaml

def main():
    """Integrates knowledge from various YAML-LD sources into a single graph."""
    parser = argparse.ArgumentParser(
        description="Integrate knowledge from various YAML-LD sources."
    )
    parser.add_argument(
        "--source-file",
        action="append",
        dest="source_files",
        help="Source YAML-LD files to integrate.",
    )
    parser.add_argument("--output-file", required=True, help="Output JSON-LD file path.")
    args = parser.parse_args()

    # Use a ConjunctiveGraph to store multiple named graphs
    integrated_graph = ConjunctiveGraph()

    # Load and parse each source file into the integrated graph
    for source_file in args.source_files:
        if not os.path.exists(source_file):
            print(f"Warning: Source file not found: {source_file}")
            continue
        try:
            with open(source_file, 'r') as f:
                # The to_rdf function takes the file content as an argument
                graph = to_rdf(
                    yaml.safe_load(f),
                    context_file='protocols/protocol.context.jsonld'
                )
                integrated_graph += graph
        except Exception as e:
            print(f"Error parsing {source_file}: {e}")
            continue

    # Serialize the integrated graph to the output file in JSON-LD format
    json_ld_output = integrated_graph.serialize(format="json-ld", indent=2)

    with open(args.output_file, "w") as f:
        f.write(json_ld_output)

    print(f"Successfully integrated knowledge into {args.output_file}")

if __name__ == "__main__":
    main()
