"""
A tool for integrating knowledge from various sources across the repository into a single, unified knowledge base.
"""

import os
import json
import argparse
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, FOAF
import dbpedia_client


def enrich_with_dbpedia(graph):
    """Enriches the graph with DBPedia abstracts for known entities."""
    # Find all entities that have a label
    for s, p, o in graph.triples((None, RDFS.label, None)):
        if isinstance(o, Literal):
            label = str(o)
            try:
                abstract = dbpedia_client.get_abstract(label)
                if abstract:
                    graph.add(
                        (
                            s,
                            URIRef("http://dbpedia.org/ontology/abstract"),
                            Literal(abstract),
                        )
                    )
            except Exception as e:
                print(f"Could not fetch abstract for {label}: {e}")
    return graph


def main():
    parser = argparse.ArgumentParser(
        description="Integrates and enriches a knowledge graph."
    )
    parser.add_argument(
        "--input", required=True, help="The path to the input JSON knowledge graph."
    )
    parser.add_argument(
        "--output",
        default="knowledge_core/knowledge_graph.jsonld",
        help="The path to the output JSON-LD file.",
    )
    args = parser.parse_args()

    with open(args.input, "r") as f:
        knowledge_graph_data = json.load(f)

    graph = Graph()

    # Integrate dependencies
    for node in knowledge_graph_data["dependencies"]["nodes"]:
        node_uri = URIRef(f"http://example.org/dependency/{node['id']}")
        graph.add((node_uri, RDF.type, URIRef("http://example.org/ontology#Dependency")))
        graph.add((node_uri, RDFS.label, Literal(node["id"])))
        if node["path"]:
            graph.add(
                (
                    node_uri,
                    URIRef("http://example.org/ontology#path"),
                    Literal(node["path"]),
                )
            )

    # Integrate symbols
    for symbol in knowledge_graph_data["symbols"]["symbols"]:
        symbol_uri = URIRef(
            f"http://example.org/symbol/{symbol['path']}/{symbol['name']}"
        )
        graph.add((symbol_uri, RDF.type, URIRef("http://example.org/ontology#Symbol")))
        graph.add((symbol_uri, RDFS.label, Literal(symbol["name"])))
        graph.add(
            (
                symbol_uri,
                URIRef("http://example.org/ontology#path"),
                Literal(symbol["path"]),
            )
        )

    # Enrich with DBPedia data
    graph = enrich_with_dbpedia(graph)

    graph.serialize(destination=args.output, format="json-ld")
    print(f"Successfully enriched knowledge graph and saved to {args.output}")


if __name__ == "__main__":
    main()
