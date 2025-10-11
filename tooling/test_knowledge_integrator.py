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
        g.add((URIRef("ex:some_rule"), URIRef("http://example.org/ontology/associated_tool"), Literal("tooling/research.py")))
        g.serialize(self.input_graph_path, format="turtle")

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_load_local_graph_success(self):
        """Test that the local graph loads successfully."""
        g, msg = knowledge_integrator.load_local_graph(self.input_graph_path)
        self.assertIsNotNone(g)
        self.assertIn("Successfully loaded", msg)
        self.assertEqual(len(g), 1)

    def test_load_local_graph_not_found(self):
        """Test that loading a non-existent graph returns None."""
        g, msg = knowledge_integrator.load_local_graph("non_existent_file.ttl")
        self.assertIsNone(g)
        self.assertIn("Error: Local graph file not found", msg)

    def test_extract_concepts(self):
        """Test that concepts are extracted and cleaned correctly."""
        g, _ = knowledge_integrator.load_local_graph(self.input_graph_path)
        concepts, msg = knowledge_integrator.extract_concepts(g)
        self.assertEqual(concepts, ["Python (programming language)"])
        self.assertIn("Extracted 1 unique concepts", msg)

    @patch('tooling.knowledge_integrator.requests.get')
    def test_query_dbpedia_success(self, mock_get):
        """Test a successful query to DBPedia, mocking the HTTP request."""
        mock_rdf_response = Graph()
        mock_rdf_response.add((URIRef("dbr:Git"), URIRef("rdfs:comment"), Literal("Git is a version control system.")))

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_rdf_response.serialize(format="xml")
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result_graph, msg = knowledge_integrator.query_dbpedia("Git")
        self.assertIsNotNone(result_graph)
        self.assertEqual(len(result_graph), 1)
        self.assertIn("Found 1 triples for 'Git'", msg)

    @patch('tooling.knowledge_integrator.requests.get')
    def test_query_dbpedia_http_error(self, mock_get):
        """Test that a DBPedia query handles HTTP errors gracefully."""
        mock_get.side_effect = knowledge_integrator.requests.exceptions.RequestException("HTTP Error")
        result_graph, msg = knowledge_integrator.query_dbpedia("Git")
        self.assertIsNone(result_graph)
        self.assertIn("Error querying DBPedia", msg)

    @patch('tooling.knowledge_integrator.query_dbpedia')
    def test_run_knowledge_integration(self, mock_query_dbpedia):
        """Test the main run_knowledge_integration function."""
        mock_external_graph = Graph()
        mock_external_graph.add((URIRef("dbr:Python"), URIRef("rdfs:comment"), Literal("A programming language.")))
        mock_query_dbpedia.return_value = (mock_external_graph, "Mocked DBPedia query")

        summary = knowledge_integrator.run_knowledge_integration(self.input_graph_path, self.output_graph_path)

        self.assertTrue(os.path.exists(self.output_graph_path))
        final_graph = Graph()
        final_graph.parse(self.output_graph_path, format="turtle")

        self.assertIn("Successfully saved enriched knowledge graph", summary)
        self.assertEqual(len(final_graph), 2)

if __name__ == '__main__':
    unittest.main()