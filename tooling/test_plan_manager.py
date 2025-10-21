import unittest
import os
import shutil
from unittest.mock import patch
from tooling.plan_manager import (
    get_registry,
    save_registry,
    register_plan,
    deregister_plan,
    list_plans,
)


class TestPlanManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_plan_manager_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.registry_path = os.path.join(self.test_dir, "plan_registry.json")
        self.plan_file_path = os.path.join(self.test_dir, "my_plan.txt")
        with open(self.plan_file_path, "w") as f:
            f.write("This is a test plan.")

        # Patch the REGISTRY_PATH to use our temporary file
        patcher = patch("tooling.plan_manager.REGISTRY_PATH", self.registry_path)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_and_save_registry(self):
        """Tests that the registry can be read from and saved to a file."""
        self.assertEqual(get_registry(), {})  # Should be empty initially

        test_data = {"plan-a": "path/to/a"}
        save_registry(test_data)

        self.assertEqual(get_registry(), test_data)

    def test_register_plan(self):
        """Tests registering a new plan."""
        with patch("sys.exit") as mock_exit:
            register_plan("my-plan", self.plan_file_path)
            mock_exit.assert_not_called()

        registry = get_registry()
        self.assertIn("my-plan", registry)
        self.assertEqual(registry["my-plan"], self.plan_file_path)

    def test_register_duplicate_plan_fails(self):
        """Tests that registering a duplicate plan name fails."""
        register_plan("my-plan", self.plan_file_path)

        with self.assertRaises(SystemExit):
            register_plan("my-plan", self.plan_file_path)

    def test_register_non_existent_plan_fails(self):
        """Tests that registering a non-existent plan file fails."""
        with self.assertRaises(SystemExit):
            register_plan("bad-plan", "non_existent_file.txt")

    def test_deregister_plan(self):
        """Tests deregistering an existing plan."""
        register_plan("my-plan", self.plan_file_path)
        self.assertIn("my-plan", get_registry())

        with patch("sys.exit") as mock_exit:
            deregister_plan("my-plan")
            mock_exit.assert_not_called()

        self.assertNotIn("my-plan", get_registry())

    def test_deregister_non_existent_plan_fails(self):
        """Tests that deregistering a non-existent plan name fails."""
        with self.assertRaises(SystemExit):
            deregister_plan("non-existent-plan")

    @patch("builtins.print")
    def test_list_plans(self, mock_print):
        """Tests that listing plans prints the correct information."""
        # Create dummy files for the plans
        plan_a_path = os.path.join(self.test_dir, "plan_a.txt")
        plan_b_path = os.path.join(self.test_dir, "plan_b.txt")
        with open(plan_a_path, "w") as f:
            f.write("plan a")
        with open(plan_b_path, "w") as f:
            f.write("plan b")

        register_plan("plan-a", plan_a_path)
        register_plan("plan-b", plan_b_path)

        list_plans()

        mock_print.assert_any_call("--- Registered Plans ---")
        mock_print.assert_any_call(f"plan-a : {plan_a_path}")
        mock_print.assert_any_call(f"plan-b : {plan_b_path}")


if __name__ == "__main__":
    unittest.main()
