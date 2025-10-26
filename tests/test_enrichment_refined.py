import unittest
import os
import subprocess
import rdflib
from rdflib.namespace import RDFS
import shutil
import json

class TestEnrichmentRefined(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp_enrichment_test"
        self.knowledge_core_dir = os.path.join(self.test_dir, "knowledge_core")
        os.makedirs(self.knowledge_core_dir, exist_ok=True)

        self.protocols_file = os.path.join(self.knowledge_core_dir, "protocols.ttl")
        self.enriched_file = os.path.join(self.knowledge_core_dir, "enriched_protocols.ttl")
        self.filesystem_data_file = os.path.join(self.knowledge_core_dir, "filesystem_data.ttl")
        self.resource_map_file = os.path.join(self.test_dir, "resource_map.json")
        self.gold_standard_file = "tests/data/gold_standard_links_v2.json"
        self.sample_protocol_file = "tests/data/sample_protocol.ttl"

        # Clean up previous runs
        if os.path.exists(self.enriched_file):
            os.remove(self.enriched_file)
        if os.path.exists(self.resource_map_file):
            os.remove(self.resource_map_file)

        # Create a dummy filesystem_data.ttl
        with open(self.filesystem_data_file, "w") as f:
            f.write("# Dummy file for testing")

        # Copy the sample protocol to the test directory
        shutil.copy(self.sample_protocol_file, self.protocols_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_refined_enrichment_produces_gold_standard_links(self):
        # 1. Run the enrichment script from the test directory
        subprocess.run([
            "python3",
            "../../enrich_protocols.py",
            "--start", "0",
            "--end", "20"
        ], cwd=self.test_dir, check=True, capture_output=True, text=True)

        # 2. Load the gold standard links
        with open(self.gold_standard_file, "r") as f:
            gold_standard = json.load(f)

        # 3. Read the enriched file and check against the gold standard
        g = rdflib.Graph()
        g.parse(self.enriched_file, format="turtle")

        protocol_uri = rdflib.URIRef("https://www.aida.org/protocol#language-theory-protocol")

        # Get the links that were added by the enrichment process
        generated_links = sorted([str(o) for o in g.objects(protocol_uri, RDFS.seeAlso)])

        # Compare the generated links with the gold standard
        expected_links = sorted(gold_standard.get("https://www.aida.org/protocol#language-theory-protocol", []))

        print("Generated Links:", json.dumps(generated_links, indent=2))
        print("Expected Links:", json.dumps(expected_links, indent=2))

        self.assertCountEqual(generated_links, expected_links, "The generated links do not match the gold standard.")

if __name__ == "__main__":
    unittest.main()
