"""
Enriches the local knowledge graph with data from external sources like DBPedia.

This script loads the RDF graph generated from the project's protocols,
identifies key concepts (like tools and rules), queries the DBPedia SPARQL
endpoint to find related information, and merges the external data into a new,
enriched knowledge graph.
"""

import os
import requests
from rdflib import Graph

# DBPedia SPARQL endpoint
DBPEDIA_SPARQL_ENDPOINT = "http://dbpedia.org/sparql"

def load_local_graph(graph_file):
    """Loads the local RDF graph from a file."""
    if not os.path.exists(graph_file):
        return None, f"Error: Local graph file not found at {graph_file}"
    g = Graph()
    g.parse(graph_file, format="turtle")
    return g, f"Successfully loaded local graph with {len(g)} triples."

def extract_concepts(graph):
    """
    Extracts key concepts (e.g., tools) from the local graph to query externally.
    This version dynamically extracts tool names from the graph.
    """
    # This query finds the string values of any objects connected by the
    # 'associated_tool' property.
    query = """
    SELECT DISTINCT ?toolName
    WHERE {
        ?s <http://example.org/ontology/associated_tool> ?toolName .
    }
    """
    results = graph.query(query)
    concepts = [row.toolName.toPython() for row in results]
    # Clean up concepts - they might be paths or have other noise
    cleaned_concepts = []
    for concept in concepts:
        # Example cleanup: take the last part of a path-like tool name
        if "/" in concept:
            cleaned_concepts.append(concept.split("/")[-1])
        else:
            cleaned_concepts.append(concept)

    # A simple heuristic to map file extensions to broader concepts
    final_concepts = []
    for concept in cleaned_concepts:
        if concept.endswith(".py"):
            final_concepts.append("Python (programming language)")
        elif concept.endswith(".json"):
            final_concepts.append("JSON")
        elif concept == "git":
             final_concepts.append("Git")
        else:
             final_concepts.append(concept)

    # Return unique concepts
    unique_concepts = sorted(list(set(final_concepts)))
    return unique_concepts, f"Extracted {len(unique_concepts)} unique concepts to query."

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
    headers = {"Accept": "application/rdf+xml"}
    params = {"query": query, "format": "application/rdf+xml"}
    try:
        response = requests.get(DBPEDIA_SPARQL_ENDPOINT, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        sub_graph = Graph()
        sub_graph.parse(data=response.text, format="xml")
        return sub_graph, f"Found {len(sub_graph)} triples for '{concept}'."
    except requests.exceptions.RequestException as e:
        return None, f"Error querying DBPedia for '{concept}': {e}"

def run_knowledge_integration(input_graph_path, output_graph_path):
    """
    The main library function to run the knowledge integration process.
    It loads a graph, extracts concepts, queries DBPedia, and saves the
    enriched graph.
    """
    messages = []

    # 1. Load local graph
    local_graph, msg = load_local_graph(input_graph_path)
    messages.append(msg)
    if not local_graph:
        return "\n".join(messages)

    initial_triple_count = len(local_graph)

    # 2. Extract concepts
    concepts_to_query, msg = extract_concepts(local_graph)
    messages.append(msg)
    if not concepts_to_query:
        messages.append("No concepts found to enrich. Exiting.")
        return "\n".join(messages)

    # 3. Query DBPedia and merge results
    total_added_triples = 0
    for concept in concepts_to_query:
        external_graph, msg = query_dbpedia(concept)
        messages.append(f"  - {msg}")
        if external_graph:
            total_added_triples += len(external_graph)
            local_graph += external_graph

    # 4. Save the enriched graph
    local_graph.serialize(destination=output_graph_path, format="turtle")
    final_triple_count = len(local_graph)
    messages.append(
        f"\nSuccessfully saved enriched knowledge graph to {output_graph_path}.\n"
        f"Initial triples: {initial_triple_count}, Added: {total_added_triples}, "
        f"Final triples: {final_triple_count}."
    )

    return "\n".join(messages)