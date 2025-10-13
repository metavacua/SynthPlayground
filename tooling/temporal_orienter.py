import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

def get_dbpedia_summary(topic):
    """
    Queries DBpedia for a summary of the given topic.

    Args:
        topic (str): The topic to search for (e.g., "Artificial_intelligence").

    Returns:
        str: The summary of the topic, or an error message if not found.
    """
    # Workaround for SSL certificate issues with the DBpedia endpoint
    ssl._create_default_https_context = ssl._create_unverified_context

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    # Use the full URI in angle brackets to handle special characters in the topic.
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?abstract
        WHERE {{
            <http://dbpedia.org/resource/{topic}> dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["abstract"]["value"]
        else:
            return f"No summary found for topic: {topic}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query DBpedia for a topic summary.")
    parser.add_argument("topic", type=str, help="The topic to search for (e.g., 'Artificial_intelligence').")
    args = parser.parse_args()

    summary = get_dbpedia_summary(args.topic)
    print(summary)