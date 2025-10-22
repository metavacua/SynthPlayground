import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def get_abstract(resource):
    """
    Fetches the abstract for a given DBPedia resource.
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT ?abstract
        WHERE {{
            dbr:{resource} dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result["abstract"]["value"]
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 dbpedia_client.py <resource_name>")
        sys.exit(1)

    resource_name = sys.argv[1]
    abstract = get_abstract(resource_name)

    if abstract:
        print(abstract)
    else:
        print(f"No abstract found for '{resource_name}'")
