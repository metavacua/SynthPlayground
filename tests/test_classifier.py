import unittest
import json
import os
import tempfile
import shutil
from language_theory.toolchain.grammar import Grammar
from language_theory.toolchain.classifier import Classifier

class TestClassifier(unittest.TestCase):

    def setUp(self):
        """Create mock AST files for testing."""
        self.test_dir = tempfile.mkdtemp()

        # Mock AST for a Regular Grammar (A -> b C ; C -> d)
        self.regular_ast = {
            "type": "A",
            "children": [
                {"type": "b"},
                {"type": "C", "children": [{"type": "d"}]}
            ]
        }
        self.regular_file = os.path.join(self.test_dir, "regular.json")
        with open(self.regular_file, "w") as f:
            json.dump(self.regular_ast, f)

        # Mock AST for a Context-Free Grammar (A -> B B ; B -> c)
        self.context_free_ast = {
            "type": "A",
            "children": [
                {"type": "B", "children": [{"type": "c"}]},
                {"type": "B", "children": [{"type": "c"}]}
            ]
        }
        self.context_free_file = os.path.join(self.test_dir, "context_free.json")
        with open(self.context_free_file, "w") as f:
            json.dump(self.context_free_ast, f)

        # For context-sensitive, we need to create a grammar manually since it's hard to represent as a tree
        self.context_sensitive_grammar = Grammar(os.path.join(self.test_dir, "csg.txt"))
        self.context_sensitive_grammar.productions = [
             (('A',), ('B',)),          # A -> B (CFG-like)
             (('B',), ('c',)),          # B -> c (CFG-like)
             (('A', 'B'), ('B', 'A')),  # AB -> BA (Context-sensitive)
        ]
        self.context_sensitive_grammar.start_symbol = 'A'


    def tearDown(self):
        """Clean up mock AST files."""
        shutil.rmtree(self.test_dir)

    def test_classify_regular(self):
        grammar = Grammar(self.regular_file)
        classifier = Classifier(grammar)
        self.assertEqual(classifier.classify(), "REGULAR (TYPE-3)")

    def test_classify_context_free(self):
        grammar = Grammar(self.context_free_file)
        classifier = Classifier(grammar)
        self.assertEqual(classifier.classify(), "CONTEXT-FREE (TYPE-2)")

    def test_classify_context_sensitive(self):
        # We use the manually created grammar here
        classifier = Classifier(self.context_sensitive_grammar)
        self.assertEqual(classifier.classify(), "CONTEXT-SENSITIVE (TYPE-1)")

if __name__ == "__main__":
    unittest.main()
