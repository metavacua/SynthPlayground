import os
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import OWL
from urllib.parse import quote

# Define namespaces
FS = Namespace("https://w3id.org/jules/filesystem/")
A = RDF.type


def generate_filesystem_rdf(root_dir, output_file):
    """
    Scans the directory structure and generates an RDF graph.
    """
    g = Graph()
    g.bind("fs", FS)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)

    # Add ontology import
    g.add((URIRef(FS), OWL.imports, URIRef(FS + "filesystem_ontology.ttl")))

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore .git directory
        if ".git" in dirnames:
            dirnames.remove(".git")

        dir_uri = URIRef(FS + quote(dirpath.replace("./", "")))
        g.add((dir_uri, A, FS.Directory))
        g.add((dir_uri, FS.filePath, Literal(dirpath)))

        parent_dir_path = os.path.dirname(dirpath)
        if parent_dir_path and parent_dir_path != dirpath:
            parent_dir_uri = URIRef(FS + quote(parent_dir_path.replace("./", "")))
            g.add((dir_uri, FS.hasParentDirectory, parent_dir_uri))

        for dirname in dirnames:
            subdir_path = os.path.join(dirpath, dirname)
            subdir_uri = URIRef(FS + quote(subdir_path.replace("./", "")))
            g.add((subdir_uri, A, FS.Directory))
            g.add((subdir_uri, FS.filePath, Literal(subdir_path)))
            g.add((dir_uri, FS.hasSubDirectory, subdir_uri))
            g.add((subdir_uri, FS.hasParentDirectory, dir_uri))

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_uri = URIRef(FS + quote(file_path.replace("./", "")))
            g.add((file_uri, A, FS.File))
            g.add((file_uri, FS.filePath, Literal(file_path)))
            g.add((dir_uri, FS.hasFile, file_uri))
            g.add((file_uri, FS.hasParentDirectory, dir_uri))

    g.serialize(destination=output_file, format="turtle")


if __name__ == "__main__":
    generate_filesystem_rdf(".", "knowledge_core/filesystem_data.ttl")
    print("Filesystem RDF data generated successfully.")
