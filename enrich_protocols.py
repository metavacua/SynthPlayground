import rdflib
from rdflib.namespace import RDF, RDFS, OWL
from dbpedia_client import search_resources
import argparse
import json

# Define namespaces
PROTOCOL = rdflib.Namespace("https://www.aida.org/protocol#")
DBR = rdflib.Namespace("http://dbpedia.org/resource/")

def run_enrichment(start, end):
    # Load the existing protocols file
    g = rdflib.Graph()
    g.parse("knowledge_core/protocols.ttl", format="turtle")

    # Bind namespaces for cleaner output
    g.bind("protocol", PROTOCOL)
    g.bind("dbr", DBR)
    g.bind("owl", OWL)

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
            keywords = [word for word in str(description).split() if len(word) > 4 and word.isalpha()]
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
            resources = search_resources(keyword)
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
                g.add((s, OWL.sameAs, rdflib.term.URIRef(resource_uri)))

        if description:
            keywords = [word for word in str(description).split() if len(word) > 4 and word.isalpha()]
            for keyword in keywords:
                if keyword in resource_map:
                    for resource_uri in resource_map[keyword]:
                        g.add((s, OWL.sameAs, rdflib.term.URIRef(resource_uri)))

    print("\nEnrichment complete.")

    # Serialize the enriched graph to a new file
    g.serialize(destination="knowledge_core/enriched_protocols.ttl", format="turtle")
    print("Enriched protocols saved to knowledge_core/enriched_protocols.ttl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enrich RDF protocols with DBPedia resources.")
    parser.add_argument("--start", type=int, required=True, help="Start index for keyword processing.")
    parser.add_argument("--end", type=int, required=True, help="End index for keyword processing.")
    args = parser.parse_args()
    run_enrichment(args.start, args.end)
