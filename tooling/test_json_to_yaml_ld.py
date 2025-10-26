import unittest
import os
import json
import yaml
import shutil
from json_to_yaml_ld import convert_json_to_yaml_ld

class TestJsonToYamlLd(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'temp_test_dir_for_conversion'
        self.context_file = 'temp_test_context.jsonld'
        os.makedirs(self.test_dir, exist_ok=True)

        self.json_data = {"key": "value", "nested": {"key2": "value2"}}
        self.json_file_path = os.path.join(self.test_dir, 'test.json')
        with open(self.json_file_path, 'w') as f:
            json.dump(self.json_data, f)

        self.context_data = {
            "@context": {
                "proto": "https://w3id.org/jules/protocol/",
                "key": "proto:key"
            }
        }
        with open(self.context_file, 'w') as f:
            json.dump(self.context_data, f)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.context_file):
            os.remove(self.context_file)

    def test_convert_json_to_yaml_ld(self):
        convert_json_to_yaml_ld(self.test_dir, self.context_file)

        yaml_filepath = os.path.join(self.test_dir, 'test.yaml')
        self.assertTrue(os.path.exists(yaml_filepath), "YAML file was not created.")

        with open(yaml_filepath, 'r') as f:
            converted_data = yaml.safe_load(f)

        expected_data = self.json_data.copy()
        expected_data['@context'] = self.context_data['@context']

        self.assertEqual(converted_data, expected_data, "Converted YAML data does not match expected data.")

if __name__ == '__main__':
    unittest.main()
