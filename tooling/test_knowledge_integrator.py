import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from rdflib import Graph, Literal, URIRef

from tooling import knowledge_integrator


class TestKnowledgeIntegrator(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and files for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.input_graph_path = os.path.join(self.test_dir.name, "protocols.ttl")
        self.output_graph_path = os.path.join(self.test_dir.name, "enriched.ttl")

        # Create a dummy input graph with a tool to be extracted
        g = Graph()
        g.add(
            (
                URIRef("ex:some_rule"),
                URIRef("http://example.org/ontology/associated_tool"),
                Literal("tooling/research.py"),
            )
        )
        g.serialize(self.input_graph_path, format="turtle")

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

if __name__ == "__main__":
    unittest.main()
