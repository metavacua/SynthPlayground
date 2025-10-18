import json
import os
import glob
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, RDFS

def find_all_protocol_files(root_path: str) -> list[str]:
    """Finds all '.protocol.json' files recursively from the root path."""
    return glob.glob(os.path.join(root_path, '**', '*.protocol.json'), recursive=True)

def generate_knowledge_graph(root_path: str, output_file: str):
    """
    Generates a Turtle RDF knowledge graph from all protocol files.
    """
    print("Starting knowledge graph generation...")

    # Define a namespace for our protocol ontology
    PROTO = Namespace("http://agent-protocol.com/ontology#")

    # Create a new RDF graph
    g = Graph()
    g.bind("proto", PROTO)
    g.bind("dcterms", DCTERMS)
    g.bind("rdfs", RDFS)

    # Define classes and properties in our ontology for clarity
    g.add((PROTO.Protocol, RDF.type, RDFS.Class))
    g.add((PROTO.Protocol, RDFS.label, Literal("Protocol")))
    g.add((PROTO.Rule, RDF.type, RDFS.Class))
    g.add((PROTO.Rule, RDFS.label, Literal("Rule")))
    g.add((PROTO.hasRule, RDF.type, RDF.Property))
    g.add((PROTO.governsTool, RDF.type, RDF.Property))

    protocol_files = find_all_protocol_files(root_path)

    if not protocol_files:
        print("No protocol files found. Knowledge graph will be empty.")
        g.serialize(destination=output_file, format='turtle')
        return

    for proto_file in protocol_files:
        try:
            with open(proto_file, 'r') as f:
                data = json.load(f)

            protocol_id = data.get("protocol_id")
            if not protocol_id:
                continue

            print(f"  - Processing {protocol_id} from {proto_file}")

            # Create a URI for the protocol
            protocol_uri = URIRef(f"http://agent-protocol.com/protocols/{protocol_id}")

            # Add basic protocol information
            g.add((protocol_uri, RDF.type, PROTO.Protocol))
            g.add((protocol_uri, RDFS.label, Literal(protocol_id)))
            g.add((protocol_uri, DCTERMS.description, Literal(data.get("description", ""))))

            # Add rules
            for i, rule in enumerate(data.get("rules", [])):
                rule_id = rule.get("rule_id")
                # Create a URI for the rule, ensuring it's unique
                rule_uri = URIRef(f"http://agent-protocol.com/rules/{protocol_id}/{rule_id}")

                g.add((rule_uri, RDF.type, PROTO.Rule))
                g.add((protocol_uri, PROTO.hasRule, rule_uri))
                g.add((rule_uri, RDFS.label, Literal(rule_id)))
                g.add((rule_uri, DCTERMS.description, Literal(rule.get("description", ""))))
                if "enforcement" in rule:
                    g.add((rule_uri, PROTO.enforcement, Literal(rule.get("enforcement"))))

            # Add associated tools
            for tool in data.get("associated_tools", []):
                # We create a simple literal for the tool path for now
                g.add((protocol_uri, PROTO.governsTool, Literal(tool)))

        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error processing file {proto_file}: {e}")
            continue

    # Serialize the graph to a Turtle file
    g.serialize(destination=output_file, format='turtle')
    print(f"Successfully generated knowledge graph at: {output_file}")

if __name__ == '__main__':
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    output_ttl_file = os.path.join(repo_root, 'protocols.ttl')
    generate_knowledge_graph(repo_root, output_ttl_file)