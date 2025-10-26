import sys
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.parse import quote
from urllib.error import URLError

def get_abstract(resource, lang='en'):
    """
    Fetches the abstract for a given DBPedia resource in the specified language.
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setTimeout(30)  # Set a 30-second timeout

    safe_resource = quote(resource)

    sparql.setQuery(f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT ?abstract
        WHERE {{
            dbr:{safe_resource} dbo:abstract ?abstract .
            FILTER (lang(?abstract) = '{lang}')
        }}
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            return result["abstract"]["value"]
    except URLError:
        print(f"Error: Timeout while trying to connect to DBPedia endpoint.", file=sys.stderr)
        return None
    return None

def search_resources(keyword, resource_type=None):
    """
    Searches for DBPedia resources with labels matching the keyword, with an optional type filter.
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setTimeout(30)

    type_filter = ""
    if resource_type:
        type_filter = f"?resource a dbo:{resource_type} ."

    safe_keyword = "".join(e for e in keyword if e.isalnum() or e.isspace())
    sparql.setQuery(f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?resource
        WHERE {{
            ?resource rdfs:label ?label .
            ?label bif:contains "'{safe_keyword}'" .
            {type_filter}
            FILTER(langMatches(lang(?label), "EN")) .
            FILTER (!regex(str(?resource), "^http://dbpedia.org/resource/Category:"))
        }}
        LIMIT 10
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        resources = []
        for result in results["results"]["bindings"]:
            resource_uri = result["resource"]["value"]
            resource_name = resource_uri.split("/")[-1]
            resources.append(resource_name)
        return resources
    except URLError:
        print(f"Error: Timeout while trying to connect to DBPedia endpoint.", file=sys.stderr)
        return []

def get_resource_type(resource):
    """
    Fetches the rdf:type for a given DBPedia resource.
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setTimeout(30)

    safe_resource = quote(resource)

    sparql.setQuery(f"""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?type
        WHERE {{
            dbr:{safe_resource} rdf:type ?type .
        }}
        LIMIT 1
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            return result["type"]["value"]
    except URLError:
        print(f"Error: Timeout while trying to connect to DBPedia endpoint.", file=sys.stderr)
        return None
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A command-line client for the DBPedia API.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'get' command
    parser_get = subparsers.add_parser("get", help="Get the abstract for a specific DBPedia resource.")
    parser_get.add_argument("resource_name", help="The name of the DBPedia resource (e.g., 'Albert_Einstein').")
    parser_get.add_argument("--lang", default="en", help="The language of the abstract (e.g., 'es', 'fr').")

    # 'search' command
    parser_search = subparsers.add_parser("search", help="Search for DBPedia resources.")
    parser_search.add_argument("keyword", help="The keyword to search for.")
    parser_search.add_argument("--type", help="Filter the search by a specific resource type (e.g., 'Person', 'Work').")

    # 'get_type' command
    parser_get_type = subparsers.add_parser("get_type", help="Get the rdf:type for a specific DBPedia resource.")
    parser_get_type.add_argument("resource_name", help="The name of the DBPedia resource (e.g., 'Software_engineering').")

    args = parser.parse_args()

    if args.command == "get":
        abstract = get_abstract(args.resource_name, args.lang)
        if abstract:
            print(abstract)
        else:
            print(f"No abstract found for '{args.resource_name}' in language '{args.lang}'.", file=sys.stderr)
            sys.exit(1)
    elif args.command == "search":
        resources = search_resources(args.keyword, args.type)
        if resources:
            for resource in resources:
                print(resource)
        else:
            print(f"No resources found for keyword '{args.keyword}'.", file=sys.stderr)
            sys.exit(1)
    elif args.command == "get_type":
        resource_type = get_resource_type(args.resource_name)
        if resource_type:
            print(resource_type)
        else:
            print(f"No type found for '{args.resource_name}'.", file=sys.stderr)
            sys.exit(1)
