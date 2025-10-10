import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS

# Assuming knowledge_integrator is in the same directory or accessible
from tooling import knowledge_integrator

class TestKnowledgeIntegrator(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and files for testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.input_graph_path = os.path.join(self.test_dir.name, "protocols.ttl")
        self.output_graph_path = os.path.join(self.test_dir.name, "enriched.ttl")

        # Create a dummy input graph
        g = Graph()
        g.add((URIRef("ex:Git"), RDF.type, URIRef("ex:Tool")))
        g.serialize(self.input_graph_path, format="turtle")

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_load_local_graph_success(self):
        """Test that the local graph loads successfully."""
        g = knowledge_integrator.load_local_graph(self.input_graph_path)
        self.assertIsNotNone(g)
        self.assertEqual(len(g), 1)

    def test_load_local_graph_not_found(self):
        """Test that loading a non-existent graph returns None."""
        g = knowledge_integrator.load_local_graph("non_existent_file.ttl")
        self.assertIsNone(g)

    @patch('tooling.knowledge_integrator.requests.get')
    def test_query_dbpedia_success(self, mock_get):
        """Test a successful query to DBPedia, mocking the HTTP request."""
        # Create a mock RDF response from DBPedia
        mock_rdf_response = Graph()
        mock_rdf_response.add((URIRef("dbr:Git"), RDFS.comment, Literal("Git is a version control system.")))

        # Configure the mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_rdf_response.serialize(format="xml")
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Run the query
        result_graph = knowledge_integrator.query_dbpedia("Git")

        # Assertions
        self.assertIsNotNone(result_graph)
        self.assertEqual(len(result_graph), 1)
        self.assertIn(
            (URIRef("dbr:Git"), RDFS.comment, Literal("Git is a version control system.")),
            result_graph
        )

    @patch('tooling.knowledge_integrator.requests.get')
    def test_query_dbpedia_http_error(self, mock_get):
        """Test that a DBPedia query handles HTTP errors gracefully."""
        mock_get.side_effect = knowledge_integrator.requests.exceptions.RequestException("HTTP Error")

        result_graph = knowledge_integrator.query_dbpedia("Git")
        self.assertIsNone(result_graph)

    @patch('tooling.knowledge_integrator.query_dbpedia')
    def test_main_integration(self, mock_query_dbpedia):
        """Test the main function's integration of loading, querying, and saving."""
        # Mock the DBPedia query to return a predictable subgraph
        mock_external_graph = Graph()
        mock_external_graph.add((URIRef("dbr:Python"), RDFS.comment, Literal("A programming language.")))
        mock_query_dbpedia.return_value = mock_external_graph

        # Run the main function with test arguments
        with patch('sys.argv', ['knowledge_integrator.py', '--input-graph', self.input_graph_path, '--output-graph', self.output_graph_path]):
            knowledge_integrator.main()

        # Verify the output file was created and has the correct content
        self.assertTrue(os.path.exists(self.output_graph_path))

        final_graph = Graph()
        final_graph.parse(self.output_graph_path, format="turtle")

        # The final graph should contain triples from both the local and mocked external graphs
        self.assertEqual(len(final_graph), 2) # 1 local + 1 unique mocked triple
        self.assertIn((URIRef("ex:Git"), RDF.type, URIRef("ex:Tool")), final_graph)
        self.assertIn((URIRef("dbr:Python"), RDFS.comment, Literal("A programming language.")), final_graph)

if __name__ == '__main__':
    unittest.main()