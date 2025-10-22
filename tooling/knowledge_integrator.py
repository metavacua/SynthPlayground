"""
A tool for integrating knowledge from various sources across the repository into a single, unified knowledge base.
"""

import os
import json
import argparse
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, FOAF

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def integrate_lessons(graph, lessons_file):
    """Integrates lessons from a JSONL file into the knowledge graph."""
    if not os.path.exists(lessons_file):
        print(f"Warning: Lessons file not found at {lessons_file}")
        return

    with open(lessons_file, "r") as f:
        for line in f:
            lesson = json.loads(line)
            lesson_uri = URIRef(f"http://example.org/lesson/{lesson['lesson_id']}")
            graph.add((lesson_uri, RDF.type, URIRef("http://example.org/ontology#Lesson")))
            graph.add((lesson_uri, RDFS.label, Literal(lesson['lesson'])))
            graph.add((lesson_uri, URIRef("http://example.org/ontology#action"), Literal(json.dumps(lesson['action']))))

def integrate_protocols(graph, protocols_dir):
    """Integrates protocol definitions into the knowledge graph."""
    for root, _, files in os.walk(protocols_dir):
        for file in files:
            if file.endswith(".protocol.json"):
                with open(os.path.join(root, file), "r") as f:
                    protocol = json.load(f)
                    protocol_uri = URIRef(f"http://example.org/protocol/{protocol['protocol_id']}")
                    graph.add((protocol_uri, RDF.type, URIRef("http://example.org/ontology#Protocol")))
                    graph.add((protocol_uri, RDFS.label, Literal(protocol['description'])))
                    for rule in protocol.get("rules", []):
                        rule_uri = URIRef(f"http://example.org/rule/{rule['rule_id']}")
                        graph.add((rule_uri, RDF.type, URIRef("http://example.org/ontology#Rule")))
                        graph.add((rule_uri, RDFS.label, Literal(rule['description'])))
                        graph.add((protocol_uri, URIRef("http://example.org/ontology#hasRule"), rule_uri))

def integrate_research(graph, research_dir):
    """Integrates research findings into the knowledge graph."""
    for root, _, files in os.walk(research_dir):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    # This is a simple example; a more sophisticated system would use NLP to extract key findings.
                    research_uri = URIRef(f"http://example.org/research/{file}")
                    graph.add((research_uri, RDF.type, URIRef("http://example.org/ontology#Research")))
                    graph.add((research_uri, RDFS.label, Literal(f"Research findings from {file}")))
                    graph.add((research_uri, URIRef("http://example.org/ontology#content"), Literal(content)))

def main():
    parser = argparse.ArgumentParser(description="Integrates knowledge from various sources into a single knowledge base.")
    parser.add_argument("--output-file", required=True, help="The path to the output knowledge base file.")
    args = parser.parse_args()

    graph = Graph()

    # Load the existing graph if it exists
    if os.path.exists(args.output_file):
        try:
            graph.parse(args.output_file, format="json-ld")
            print(f"Loaded existing knowledge base from {args.output_file}")
        except Exception as e:
            print(f"Warning: Could not parse existing knowledge base. A new one will be created. Error: {e}")

    integrate_lessons(graph, os.path.join(ROOT_DIR, "knowledge_core/lessons.jsonl"))
    integrate_protocols(graph, os.path.join(ROOT_DIR, "protocols"))
    integrate_research(graph, os.path.join(ROOT_DIR, "research"))

    graph.serialize(destination=args.output_file, format="json-ld")
    print(f"Successfully integrated knowledge into {args.output_file}")

if __name__ == "__main__":
    main()
