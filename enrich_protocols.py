import rdflib
from rdflib.namespace import RDFS
from dbpedia_client import get_relevant_links
import argparse
import json
import sys
import os

# Add root directory for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Define namespaces
PROTOCOL = rdflib.Namespace("https://www.aida.org/protocol#")
DBR = rdflib.Namespace("http://dbpedia.org/resource/")

def extract_keywords(text):
    """
    Extracts meaningful keywords from a text, focusing on nouns and noun phrases.
    This is a simple heuristic and could be improved with NLP libraries.
    """
    # A curated list of keywords that are relevant to the repository's domain
    domain_keywords = [
        "Chomsky Hierarchy",
        "Intuitionistic Linear Logic",
        "Sequent Calculus",
        "Subclassical Logic"
    ]

    keywords = []
    for keyword in domain_keywords:
        if keyword.lower() in text.lower():
            keywords.append(keyword.lower())

    return keywords

def run_enrichment(start, end, knowledge_core_dir):
    # Load the existing protocols file
    g = rdflib.Graph()
    g.parse(os.path.join(knowledge_core_dir, "protocols.ttl"), format="turtle")
    g.parse(os.path.join(knowledge_core_dir, "filesystem_data.ttl"), format="turtle")

    # Bind namespaces for cleaner output
    g.bind("protocol", PROTOCOL)
    g.bind("dbr", DBR)
    g.bind("rdfs", RDFS)

    # Get all subjects once to have a total count
    subjects = list(g.subjects(None, None))
    total_subjects = len(subjects)
    all_keywords = set()

    # First pass: collect all keywords
    for s in subjects:
        label = g.value(s, RDFS.label)
        description = g.value(s, PROTOCOL.description)
        if label:
            all_keywords.add(str(label))
        if description:
            keywords = extract_keywords(str(description))
            all_keywords.update(keywords)

    # Query DBPedia for a chunk of unique keywords
    sorted_keywords = sorted(list(all_keywords))
    keyword_chunk = sorted_keywords[start:end]

    print(f"Found {len(all_keywords)} unique keywords. Querying DBPedia for chunk {start}-{end}...")
    resource_map = {}

    # Load existing resource map if it exists
    try:
        with open('resource_map.json', 'r') as f:
            resource_map = json.load(f)
    except FileNotFoundError:
        pass

    for i, keyword in enumerate(keyword_chunk):
        print(f"Querying keyword {i+start+1}/{len(all_keywords)}: {keyword}", end='\r')
        if keyword not in resource_map:
            resources = get_relevant_links(keyword, None)
            if resources:
                resource_map[keyword] = [str(DBR[r]) for r in resources]
    print("\nDBPedia queries for chunk complete.")

    # Save the updated resource map
    with open('resource_map.json', 'w') as f:
        json.dump(resource_map, f)

    # Second pass: add triples to the graph
    for i, s in enumerate(subjects):
        print(f"Enriching subject {i+1}/{total_subjects}: {s}", end='\r')
        label = g.value(s, RDFS.label)
        description = g.value(s, PROTOCOL.description)

        if label and str(label) in resource_map:
            for resource_uri in resource_map[str(label)]:
                g.add((s, RDFS.seeAlso, rdflib.term.URIRef(resource_uri)))

        if description:
            keywords = extract_keywords(str(description))
            for keyword in keywords:
                if keyword in resource_map:
                    for resource_uri in resource_map[keyword]:
                        g.add((s, RDFS.seeAlso, rdflib.term.URIRef(resource_uri)))

    print("\nEnrichment complete.")

    # Serialize the enriched graph to a new file
    g.serialize(destination=os.path.join(knowledge_core_dir, "enriched_protocols.ttl"), format="turtle")
    print(f"Enriched protocols saved to {os.path.join(knowledge_core_dir, 'enriched_protocols.ttl')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enrich RDF protocols with DBPedia resources.")
    parser.add_argument("--start", type=int, required=True, help="Start index for keyword processing.")
    parser.add_argument("--end", type=int, required=True, help="End index for keyword processing.")
    parser.add_argument("--knowledge-core-dir", type=str, default="knowledge_core", help="The directory containing the knowledge core files.")
    args = parser.parse_args()
    run_enrichment(args.start, args.end, args.knowledge_core_dir)
