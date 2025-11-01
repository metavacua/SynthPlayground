import argparse
import json
import sys
import os
import importlib.util
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

PROTOCOL = Namespace("https://www.aida.org/protocol#")
DEFAULT_KG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "knowledge_core", "protocols.ttl"
)


def get_applicable_protocols(graph, context):
    """
    Queries the graph to find protocols that are applicable to the given context.
    This function dynamically loads and executes the `is_applicable` function
    from the Python protocol files.
    """
    # First, find all protocols that have a Python-based applicability condition.
    query_str = """
    SELECT ?protocol ?conditionPath WHERE {
        ?protocol rdf:type protocol:Protocol .
        ?protocol protocol:hasApplicabilityCondition ?conditionPath .
    }
    """
    q = prepareQuery(
        query_str,
        initNs={
            "protocol": PROTOCOL,
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        },
    )

    applicable_protocols = []

    for row in graph.query(q):
        protocol_uri = row.protocol
        condition_path = str(row.conditionPath)

        try:
            # Dynamically load the module and run the applicability check
            spec = importlib.util.spec_from_file_location(
                "protocol_module", condition_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if module.is_applicable(context):
                applicable_protocols.append(str(protocol_uri))
        except Exception as e:
            print(
                f"Error evaluating applicability for {protocol_uri} from {condition_path}: {e}",
                file=sys.stderr,
            )

    # Also, include all protocols that *don't* have a specific applicability condition (i.e., they are always applicable)
    query_static_str = """
    SELECT ?protocol WHERE {
        ?protocol rdf:type protocol:Protocol .
        FILTER NOT EXISTS { ?protocol protocol:hasApplicabilityCondition ?cond . }
    }
    """
    q_static = prepareQuery(
        query_static_str,
        initNs={
            "protocol": PROTOCOL,
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        },
    )

    for row in graph.query(q_static):
        applicable_protocols.append(str(row.protocol))

    return applicable_protocols


def get_rules_for_protocols(graph, protocol_uris):
    """
    Retrieves all rules associated with the given list of protocol URIs.
    """
    if not protocol_uris:
        return []

    # We need to format the list of URIs for the SPARQL query
    protocol_uri_refs = [f"<{uri}>" for uri in protocol_uris]

    query_str = f"""
    SELECT ?rule_id ?description ?enforcement WHERE {{
        VALUES ?protocol {{ {' '.join(protocol_uri_refs)} }} .
        ?protocol protocol:hasRule ?rule .
        ?rule rdfs:label ?rule_id .
        ?rule protocol:description ?description .
        ?rule protocol:enforcement ?enforcement .
    }}
    """

    q = prepareQuery(
        query_str,
        initNs={"protocol": PROTOCOL, "rdfs": "http://www.w3.org/2000/01/rdf-schema#"},
    )

    rules = []
    for row in graph.query(q):
        rules.append(
            {
                "rule_id": str(row.rule_id),
                "description": str(row.description),
                "enforcement": str(row.enforcement),
            }
        )
    return rules


def main():
    parser = argparse.ArgumentParser(
        description="Protocol Oracle: Queries the knowledge graph for applicable agent protocols."
    )
    parser.add_argument(
        "--context",
        required=True,
        help="A JSON string representing the agent's current context (e.g., task, target files).",
    )
    parser.add_argument(
        "--kg-file",
        default=DEFAULT_KG_FILE,
        help="Path to the protocol knowledge graph file.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.kg_file):
        print(
            f"Error: Knowledge graph file not found at {args.kg_file}", file=sys.stderr
        )
        sys.exit(1)

    try:
        context = json.loads(args.context)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format for context.", file=sys.stderr)
        sys.exit(1)

    g = Graph()
    g.parse(args.kg_file, format="turtle")

    applicable_protocols = get_applicable_protocols(g, context)
    rules = get_rules_for_protocols(g, applicable_protocols)

    # Output the rules as a JSON object for easy parsing by the agent
    print(json.dumps(rules, indent=2))


if __name__ == "__main__":
    main()
