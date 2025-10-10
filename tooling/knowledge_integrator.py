"""
Enriches the local knowledge graph with data from external sources like DBPedia.

This script loads the RDF graph generated from the project's protocols,
identifies key concepts (like tools and rules), queries the DBPedia SPARQL
endpoint to find related information, and merges the external data into a new,
enriched knowledge graph.
"""

import argparse
import os
import requests
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS

# DBPedia SPARQL endpoint
DBPEDIA_SPARQL_ENDPOINT = "http://dbpedia.org/sparql"

# --- Main Functions ---

def load_local_graph(graph_file):
    """Loads the local RDF graph from a file."""
    if not os.path.exists(graph_file):
        print(f"Error: Local graph file not found at {graph_file}")
        return None
    g = Graph()
    g.parse(graph_file, format="turtle")
    print(f"Successfully loaded local graph with {len(g)} triples.")
    return g

def extract_concepts(graph):
    """Extracts key concepts (e.g., tools) from the local graph to query externally."""
    # This query will need to be adapted to the actual structure of the local graph.
    # For now, let's assume we are looking for subjects with a 'toolName' property.
    # A more robust implementation would inspect the ontology.
    query = """
    SELECT DISTINCT ?concept
    WHERE {
        ?s <http://example.org/ontology/associated_tool> ?concept .
    }
    """
    results = graph.query(query)
    concepts = [row.concept.toPython() for row in results]
    print(f"Extracted {len(concepts)} concepts to query from DBPedia.")
    return concepts

def query_dbpedia(concept):
    """Queries DBPedia for a given concept and returns a graph of results."""
    # We will look for the abstract/comment and the type of the concept.
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>

    CONSTRUCT {{
        ?thing rdfs:comment ?comment .
        ?thing rdf:type ?type .
    }}
    WHERE {{
        ?thing rdfs:label "{concept}"@en .
        OPTIONAL {{ ?thing dbo:abstract ?comment . FILTER (lang(?comment) = 'en') }}
        OPTIONAL {{ ?thing rdf:type ?type . }}
    }}
    LIMIT 10
    """
    headers = {
        "Accept": "application/rdf+xml"
    }
    params = {
        "query": query,
        "format": "application/rdf+xml"
    }
    try:
        response = requests.get(DBPEDIA_SPARQL_ENDPOINT, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        sub_graph = Graph()
        sub_graph.parse(data=response.text, format="xml")
        return sub_graph
    except requests.exceptions.RequestException as e:
        print(f"Error querying DBPedia for '{concept}': {e}")
        return None

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Enrich local knowledge graph with DBPedia.")
    parser.add_argument(
        "--input-graph",
        default="knowledge_core/protocols.ttl",
        help="Path to the local knowledge graph file."
    )
    parser.add_argument(
        "--output-graph",
        default="knowledge_core/enriched_protocols.ttl",
        help="Path to save the enriched knowledge graph."
    )
    args = parser.parse_args()

    # 1. Load local graph
    local_graph = load_local_graph(args.input_graph)
    if not local_graph:
        return

    # 2. Extract concepts
    # For this initial version, we will hardcode a few concepts to test the pipeline.
    # The `extract_concepts` function will be used in the next iteration.
    concepts_to_query = ["Python (programming language)", "JSON", "Git"]
    print(f"Using test concepts: {concepts_to_query}")

    # 3. Query DBPedia and merge results
    for concept in concepts_to_query:
        print(f"  - Querying DBPedia for: {concept}")
        external_graph = query_dbpedia(concept)
        if external_graph:
            print(f"    - Found {len(external_graph)} triples. Merging into local graph.")
            local_graph += external_graph

    # 4. Save the enriched graph
    local_graph.serialize(destination=args.output_graph, format="turtle")
    print(f"\nSuccessfully saved enriched knowledge graph to {args.output_graph}")
    print(f"Final graph contains {len(local_graph)} triples.")

if __name__ == "__main__":
    main()