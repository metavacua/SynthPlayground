import os
import json
import yaml
from rdflib import Graph, Literal, RDF, RDFS, URIRef, BNode
from rdflib.namespace import Namespace, PROV, FOAF

# --- Ontology Definition ---
# Define our custom namespace
BUILD = Namespace("http://example.com/build-ontology#")

# Core Classes
ProofStep = BUILD.ProofStep
BuildArtifact = BUILD.BuildArtifact
Sequent = BUILD.Sequent
AxiomaticStep = BUILD.AxiomaticStep # for steps with no antecedents
InferentialStep = BUILD.InferentialStep # for steps with antecedents

# Core Properties
hasSequent = BUILD.hasSequent
hasPremise = BUILD.hasPremise # Connects InferentialStep to child ProofSteps
hasConclusion = BUILD.hasConclusion # Connects ProofStep to the BuildArtifact it produces
requiresResource = BUILD.requiresResource # Connects ProofStep to BuildArtifacts it consumes

def define_ontology(graph):
    """Adds the ontology definitions to the graph."""
    # Class definitions
    graph.add((ProofStep, RDF.type, RDFS.Class))
    graph.add((ProofStep, RDFS.subClassOf, PROV.Activity))
    graph.add((AxiomaticStep, RDFS.subClassOf, ProofStep))
    graph.add((InferentialStep, RDFS.subClassOf, ProofStep))

    graph.add((BuildArtifact, RDF.type, RDFS.Class))
    graph.add((BuildArtifact, RDFS.subClassOf, PROV.Entity))

    graph.add((Sequent, RDF.type, RDFS.Class))

    # Property definitions
    graph.add((hasPremise, RDF.type, RDF.Property))
    graph.add((hasConclusion, RDF.type, RDF.Property))
    graph.add((requiresResource, RDF.type, RDF.Property))
    graph.add((hasSequent, RDF.type, RDF.Property))

def find_all_sequents(root_dir):
    """Finds all AGENTS.md sequent files in the repository."""
    sequent_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        if 'AGENTS.md' in filenames:
            sequent_files.append(os.path.join(dirpath, 'AGENTS.md'))
    return sequent_files

def process_sequent_file(graph, file_path, root_dir):
    """Processes a single AGENTS.md file and adds its triples to the graph."""
    module_path = os.path.dirname(file_path)
    module_rel_path = os.path.relpath(module_path, root_dir)
    module_uri = BUILD[module_rel_path.replace(os.sep, '_') or 'root']

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    sequent_data = data.get('sequent', {})
    antecedent = sequent_data.get('antecedent', [])
    succedent = sequent_data.get('succedent', [])

    # Create the ProofStep for this module
    step_type = InferentialStep if antecedent else AxiomaticStep
    graph.add((module_uri, RDF.type, step_type))
    graph.add((module_uri, RDFS.label, Literal(f"Proof Step for {module_rel_path or 'root'}")))

    # Process succedent (conclusions)
    for item in succedent:
        artifact_id = item.get('id', 'unknown_artifact')
        artifact_uri = BUILD[artifact_id]
        graph.add((artifact_uri, RDF.type, BuildArtifact))
        graph.add((artifact_uri, RDFS.label, Literal(item.get('proposition'))))
        graph.add((artifact_uri, BUILD.hasType, Literal(item.get('type'))))
        graph.add((artifact_uri, PROV.wasGeneratedBy, module_uri))
        graph.add((module_uri, hasConclusion, artifact_uri))

    # Process antecedent (premises/consumed resources)
    for item in antecedent:
        source_module_path = os.path.normpath(os.path.join(module_path, item.get('source')))
        source_module_rel_path = os.path.relpath(source_module_path, root_dir)
        source_module_uri = BUILD[source_module_rel_path.replace(os.sep, '_')]

        artifact_id = item.get('id', 'unknown_artifact')
        artifact_uri = BUILD[artifact_id]

        graph.add((module_uri, requiresResource, artifact_uri))
        graph.add((module_uri, PROV.used, artifact_uri))
        graph.add((module_uri, hasPremise, source_module_uri)) # Link to the premise step
        graph.add((artifact_uri, PROV.wasDerivedFrom, source_module_uri)) # Indicate derivation

def generate_knowledge_graph(root_dir):
    """Generates the full knowledge graph and serializes it to JSON-LD."""
    g = Graph()
    g.bind("build", BUILD)
    g.bind("prov", PROV)
    g.bind("foaf", FOAF)

    define_ontology(g)

    sequent_files = find_all_sequents(root_dir)
    for file_path in sequent_files:
        print(f"Processing sequent: {file_path}")
        process_sequent_file(g, file_path, root_dir)

    print("Serializing knowledge graph to JSON-LD...")
    # The context maps prefixes to full URLs for JSON-LD
    context = {
        "@vocab": str(BUILD),
        "prov": str(PROV),
        "foaf": str(FOAF),
        "label": str(RDFS.label),
        "subClassOf": str(RDFS.subClassOf),
    }
    jsonld_data = g.serialize(format='json-ld', context=context, indent=4)

    return jsonld_data

def main():
    """Main function to generate and print the knowledge graph."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    jsonld_output = generate_knowledge_graph(root_dir)

    # In a real scenario, this would overwrite the root AGENTS.md
    # For now, we print it to stdout.
    print("\n--- Generated Knowledge Graph (JSON-LD) ---")
    print(jsonld_output)

    # Example of how to save it
    # with open(os.path.join(root_dir, "AGENTS.md"), "w") as f:
    #     f.write(jsonld_output)

if __name__ == "__main__":
    main()