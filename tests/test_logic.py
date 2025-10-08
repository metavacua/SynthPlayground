import unittest
import importlib.util


def import_from_path(module_name, file_path):
    """Dynamically imports a module from a given file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load spec for module {module_name} from {file_path}"
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# We can now import these directly as they are part of the installed package.
# However, for this specific test's purpose (testing two files with the same name),
# dynamic import remains the cleanest approach, but without the sys.path hack.
logic_a = import_from_path("logic_a", "prototype/version-A/logic.py")
logic_b = import_from_path("logic_b", "prototype/version-B/logic.py")


class TestParaconsistentLogic(unittest.TestCase):
    def test_version_a_completeness_success(self):
        """
        Tests that Version A (Completeness) works with valid data.
        """
        user_data = {"name": "Alice"}
        self.assertEqual(logic_a.get_user_name(user_data), "Alice")

    def test_version_a_completeness_failure(self):
        """
        Tests that Version A (Completeness) fails with invalid data, as expected.
        This is the trade-off for its simplicity.
        """
        user_data = {"email": "alice@example.com"}
        with self.assertRaises(KeyError):
            logic_a.get_user_name(user_data)

    def test_version_b_safety_success(self):
        """
        Tests that Version B (Safety) works with valid data.
        """
        user_data = {"name": "Bob"}
        self.assertEqual(logic_b.get_user_name(user_data), "Bob")

    def test_version_b_safety_failure_graceful(self):
        """
        Tests that Version B (Safety) fails gracefully with invalid data, as expected.
        This is the benefit of its robustness.
        """
        user_data = {"email": "bob@example.com"}
        self.assertEqual(logic_b.get_user_name(user_data), "Anonymous")

    def test_version_b_safety_empty_name(self):
        """
        Tests that Version B (Safety) handles an empty name gracefully.
        """
        user_data = {"name": ""}
        self.assertEqual(logic_b.get_user_name(user_data), "Anonymous")


if __name__ == "__main__":
    unittest.main()
