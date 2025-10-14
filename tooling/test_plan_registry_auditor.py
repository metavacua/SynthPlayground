import unittest
import json
import os
from tooling.plan_registry_auditor import audit_plan_registry

class TestPlanRegistryAuditor(unittest.TestCase):

    def setUp(self):
        # Create a dummy plan registry and dummy plan files for testing
        self.test_registry_path = "test_plan_registry.json"
        self.valid_plan_path = "test_valid_plan.txt"

        # Create a valid plan file
        with open(self.valid_plan_path, "w") as f:
            f.write("This is a valid plan.")

        # Create a registry with one valid and one invalid entry
        self.registry_data = {
            "valid_plan": self.valid_plan_path,
            "invalid_plan": "non_existent_plan.txt"
        }
        with open(self.test_registry_path, "w") as f:
            json.dump(self.registry_data, f)


    def tearDown(self):
        # Clean up the dummy files
        if os.path.exists(self.test_registry_path):
            os.remove(self.test_registry_path)
        if os.path.exists(self.valid_plan_path):
            os.remove(self.valid_plan_path)

    def test_audit_plan_registry(self):
        """
        Tests that the auditor correctly identifies valid and invalid plan links.
        """
        # Pass the path to our test registry directly to the function
        dead_links = audit_plan_registry(registry_path=self.test_registry_path)

        # Check that exactly one dead link was found
        self.assertEqual(len(dead_links), 1)

        # Check that the details of the dead link are correct
        name, path = dead_links[0]
        self.assertEqual(name, "invalid_plan")
        self.assertEqual(path, "non_existent_plan.txt")

if __name__ == "__main__":
    unittest.main()