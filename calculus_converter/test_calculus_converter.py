import unittest
import os
import tempfile
import shutil
import json
from calculus_converter.parser import parse_latex_to_document
from calculus_converter.sequent_generator import generate_sequent_yaml
from tooling.knowledge_compiler import load_and_parse_sequents, sequents_to_rdf

class TestCalculusConverterPipeline(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sequents_dir = os.path.join(self.test_dir, "sequents")
        os.makedirs(self.sequents_dir)

        self.mock_latex_content = r"""
\documentclass{article}
\usepackage{ebproof}
\title{Test Calculus}
\author{J. Agent}
\begin{document}
\section{Simple Rule}
\begin{prooftree}
\hypo{A \vdash B}
\infer1[Imp]{A \rightarrow B \vdash C}
\end{prooftree}
\end{document}
"""
        self.latex_path = os.path.join(self.test_dir, "test_calculus.tex")
        with open(self.latex_path, "w") as f:
            f.write(self.mock_latex_content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_01_parser(self):
        """Test that the parser correctly extracts structured data."""
        doc = parse_latex_to_document(self.mock_latex_content)
        self.assertEqual(doc.title, "Test Calculus")
        self.assertEqual(len(doc.elements), 2) # section and prooftree

        tree_element = doc.elements[1]
        self.assertEqual(tree_element[0], "prooftree")
        proof_tree = tree_element[1]

        self.assertEqual(proof_tree.rule_name, "Imp")
        self.assertEqual(len(proof_tree.hypotheses), 1)

        conclusion = proof_tree.conclusion
        self.assertEqual(len(conclusion.antecedent), 1)
        self.assertEqual(conclusion.antecedent[0].raw, "A \\rightarrow B")
        self.assertEqual(conclusion.succedent[0].raw, "C")

        hypothesis = proof_tree.hypotheses[0]
        self.assertEqual(hypothesis.antecedent[0].raw, "A")
        self.assertEqual(hypothesis.succedent[0].raw, "B")

    def test_02_sequent_generator(self):
        """Test that the YAML sequent file is generated correctly."""
        generate_sequent_yaml(self.latex_path, self.sequents_dir)

        output_path = os.path.join(self.sequents_dir, "test_calculus.agents.md")
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, 'r') as f:
            content = f.read()
            self.assertIn("calculus: Test Calculus", content)
            self.assertIn("rule: Imp", content)
            self.assertIn('"raw": "A \\\\rightarrow B \\\\vdash C"', content)

    def test_03_knowledge_compiler_integration(self):
        """Test that the knowledge compiler can load and convert sequents to RDF."""
        # First, generate the sequent file
        generate_sequent_yaml(self.latex_path, self.sequents_dir)

        # Second, load and parse it
        rules = load_and_parse_sequents(self.sequents_dir)
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['calculus'], 'Test Calculus')
        self.assertEqual(rules[0]['id'], 'imp_1')

        # Third, convert to RDF
        rdf_graph = sequents_to_rdf(rules)
        self.assertGreater(len(rdf_graph), 0)

        # Check for some key triples
        query = """
            PREFIX build: <http://example.com/build#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            SELECT ?rule ?prop WHERE {
                ?rule a build:ProofRule ;
                      rdfs:label ?prop .
            }
        """
        results = rdf_graph.query(query)
        self.assertEqual(len(results), 1)
        for row in results:
            self.assertIn("Rule 'Imp'", str(row.prop))

if __name__ == '__main__':
    unittest.main()