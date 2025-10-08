import unittest
import os
import shutil
import json
from toolchain.decider import decide


class TestDeciderEngine(unittest.TestCase):

    TEST_DIR = "test_decider_workspace"
    COMPONENTS_DIR = os.path.join(TEST_DIR, "components")
    OUTPUT_DIR = os.path.join(TEST_DIR, "resolved")
    POLICY_FILE = os.path.join(TEST_DIR, "policy.json")

    def setUp(self):
        """Set up a temporary directory and prototype components."""
        os.makedirs(self.COMPONENTS_DIR, exist_ok=True)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        # Create Component A (Completeness)
        comp_a_path = os.path.join(self.COMPONENTS_DIR, "component-a")
        os.makedirs(comp_a_path, exist_ok=True)
        with open(os.path.join(comp_a_path, "logic.py"), "w") as f:
            f.write("# Component A")
        with open(os.path.join(comp_a_path, "manifest.json"), "w") as f:
            json.dump(
                {
                    "stance": "Completeness",
                    "provides": "logic.py",
                    "verification_command": "exit 0",
                },
                f,
            )

        # Create Component B (Safety)
        comp_b_path = os.path.join(self.COMPONENTS_DIR, "component-b")
        os.makedirs(comp_b_path, exist_ok=True)
        with open(os.path.join(comp_b_path, "logic.py"), "w") as f:
            f.write("# Component B")
        with open(os.path.join(comp_b_path, "manifest.json"), "w") as f:
            json.dump(
                {
                    "stance": "Safety",
                    "provides": "logic.py",
                    "verification_command": "exit 0",
                },
                f,
            )

        # Create Resolution Policy
        with open(self.POLICY_FILE, "w") as f:
            json.dump({"priority_of_stances": ["Safety", "Completeness"]}, f)

    def tearDown(self):
        """Remove the temporary directory."""
        shutil.rmtree(self.TEST_DIR)

    def test_decider_prefers_safety(self):
        """Test that the decider chooses Safety over Completeness based on policy."""
        decide(self.COMPONENTS_DIR, self.POLICY_FILE, self.OUTPUT_DIR)
        resolved_file = os.path.join(self.OUTPUT_DIR, "logic.py")
        self.assertTrue(os.path.exists(resolved_file))
        with open(resolved_file, "r") as f:
            content = f.read()
            self.assertEqual(content, "# Component B")

    def test_decider_chooses_completeness_if_safety_fails(self):
        """Test that the decider falls back to the next priority if the first fails verification."""
        # Make Component B's verification fail
        comp_b_manifest_path = os.path.join(
            self.COMPONENTS_DIR, "component-b", "manifest.json"
        )
        with open(comp_b_manifest_path, "w") as f:
            json.dump(
                {
                    "stance": "Safety",
                    "provides": "logic.py",
                    "verification_command": "exit 1",
                },
                f,
            )

        decide(self.COMPONENTS_DIR, self.POLICY_FILE, self.OUTPUT_DIR)
        resolved_file = os.path.join(self.OUTPUT_DIR, "logic.py")
        self.assertTrue(os.path.exists(resolved_file))
        with open(resolved_file, "r") as f:
            content = f.read()
            self.assertEqual(content, "# Component A")

    def test_decider_fails_if_no_verified_component_matches_policy(self):
        """Test that resolution fails if no verified component matches the policy."""
        # Create a policy that doesn't match any component
        unmatchable_policy_path = os.path.join(self.TEST_DIR, "unmatchable_policy.json")
        with open(unmatchable_policy_path, "w") as f:
            json.dump({"priority_of_stances": ["Performance", "Security"]}, f)

        decide(self.COMPONENTS_DIR, unmatchable_policy_path, self.OUTPUT_DIR)
        resolved_file = os.path.join(self.OUTPUT_DIR, "logic.py")
        # The decider should fail, so no file is created
        self.assertFalse(os.path.exists(resolved_file))


if __name__ == "__main__":
    unittest.main()
