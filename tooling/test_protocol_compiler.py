import unittest
import os
import json
import shutil
from protocol_compiler import compile_single_module, load_schema, process_protocol_file
import jsonschema
from rdflib import Graph

class TestProtocolCompiler(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_protocol_compiler_dir"
        self.source_dir = os.path.join(self.test_dir, "protocols")
        os.makedirs(self.source_dir, exist_ok=True)

        self.schema_path = os.path.join(self.source_dir, "protocol.schema.json")
        self.schema = {
            "type": "object",
            "properties": {
                "protocol_id": {"type": "string"},
                "description": {"type": "string"},
                "rules": {"type": "array"},
                "associated_tools": {"type": "array"},
                "is_applicable_path": {"type": "string"}
            },
            "required": ["protocol_id", "description", "rules"]
        }
        with open(self.schema_path, "w") as f:
            json.dump(self.schema, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_process_json_protocol(self):
        """Tests that a valid JSON protocol is processed correctly."""
        json_path = os.path.join(self.source_dir, "p1.protocol.json")
        protocol_data = {"protocol_id": "TEST-001", "description": "First test protocol.", "rules": [], "associated_tools": []}
        with open(json_path, "w") as f:
            json.dump(protocol_data, f)

        processed_data = process_protocol_file(json_path, self.schema)
        self.assertEqual(processed_data["protocol_id"], "TEST-001")

    def test_process_python_protocol(self):
        """Tests that a valid Python protocol is processed correctly."""
        py_path = os.path.join(self.source_dir, "p2.protocol.py")
        with open(py_path, "w") as f:
            f.write('PROTOCOL_ID = "PY-001"\n')
            f.write('DESCRIPTION = "Python protocol."\n')
            f.write('RULES = []\n')
            f.write('ASSOCIATED_TOOLS = []\n')
            f.write('def is_applicable(context): return True\n')

        processed_data = process_protocol_file(py_path, self.schema)
        self.assertEqual(processed_data["protocol_id"], "PY-001")
        self.assertIn("is_applicable_path", processed_data)

    def test_compile_single_module(self):
        """Tests that a module with mixed protocols is compiled correctly."""
        # Create a JSON protocol
        json_path = os.path.join(self.source_dir, "p1.protocol.json")
        with open(json_path, "w") as f:
            json.dump({"protocol_id": "TEST-001", "description": "JSON protocol.", "rules": [], "associated_tools": []}, f)

        # Create a Python protocol
        py_path = os.path.join(self.source_dir, "p2.protocol.py")
        with open(py_path, "w") as f:
            f.write('PROTOCOL_ID = "PY-001"\n')
            f.write('DESCRIPTION = "Python protocol."\n')
            f.write('RULES = [{"rule_id": "py-rule-1", "description": "desc", "enforcement": "enf"}]\n')
            f.write('ASSOCIATED_TOOLS = []\n')

        target_file = os.path.join(self.source_dir, "AGENTS.md")
        g = Graph()

        compile_single_module(
            source_dir=self.source_dir,
            target_file=target_file,
            schema=self.schema,
            knowledge_graph=g
        )

        # Check AGENTS.md content
        self.assertTrue(os.path.exists(target_file))
        with open(target_file, "r") as f:
            content = f.read()
        self.assertIn("TEST-001", content)
        self.assertIn("PY-001", content)

        # Check graph content
        self.assertIn((None, None, None), g) # check if graph is not empty
        self.assertGreater(len(g), 0)


if __name__ == "__main__":
    unittest.main()