import unittest
from tooling.research import execute_research_protocol


# The native tools are not defined in the module, they are injected globals.
# We use `create=True` to tell the patcher to create the attribute on the
# module during the test, which simulates the agent's execution environment.
class TestResearchExecutor(unittest.TestCase):
    """
    Tests for the research executor tool, mocking the native tools that are
    globally injected by the execution environment.
    """

    def setUp(self):
        self.mock_tools = {
            "read_file": unittest.mock.MagicMock(return_value="file content"),
            "list_files": unittest.mock.MagicMock(return_value=["file1.txt", "file2.txt"]),
            "google_search": unittest.mock.MagicMock(return_value="search results"),
            "view_text_website": unittest.mock.MagicMock(return_value="website content"),
        }

    def test_local_filesystem_file_scope(self):
        """Verify it calls read_file for local file scope."""
        constraints = {
            "target": "local_filesystem",
            "scope": "file",
            "path": "test.txt",
        }

        result = execute_research_protocol(constraints, self.mock_tools)

        self.mock_tools["read_file"].assert_called_once_with(filepath="test.txt")
        self.assertEqual(result, "file content")
        # Ensure other mocks were not called
        self.mock_tools["list_files"].assert_not_called()
        self.mock_tools["google_search"].assert_not_called()
        self.mock_tools["view_text_website"].assert_not_called()

    def test_local_filesystem_directory_scope(self):
        """Verify it calls list_files for local directory scope."""
        constraints = {
            "target": "local_filesystem",
            "scope": "directory",
            "path": "test_dir/",
        }

        result = execute_research_protocol(constraints, self.mock_tools)

        self.mock_tools["list_files"].assert_called_once_with(path="test_dir/")
        self.assertEqual(result, "file1.txt\nfile2.txt")

    def test_external_web_narrow_scope(self):
        """Verify it calls google_search for external narrow scope."""
        constraints = {
            "target": "external_web",
            "scope": "narrow",
            "query": "test query",
        }

        result = execute_research_protocol(constraints, self.mock_tools)

        self.mock_tools["google_search"].assert_called_once_with(query="test query")
        self.assertEqual(result, "search results")

    def test_external_web_broad_scope(self):
        """Verify it calls view_text_website for external broad scope."""
        constraints = {
            "target": "external_web",
            "scope": "broad",
            "url": "http://example.com",
        }

        result = execute_research_protocol(constraints, self.mock_tools)

        self.mock_tools["view_text_website"].assert_called_once_with(url="http://example.com")
        self.assertEqual(result, "website content")

    def test_external_repository_scope(self):
        """Verify it calls view_text_website for external repository scope."""
        self.mock_tools["view_text_website"].return_value = "repo file content"
        constraints = {
            "target": "external_repository",
            "url": "http://example.com/file.py",
        }

        result = execute_research_protocol(constraints, self.mock_tools)

        self.mock_tools["view_text_website"].assert_called_once_with(url="http://example.com/file.py")
        self.assertEqual(result, "repo file content")

    def test_invalid_target(self):
        """Verify it returns an error for an invalid target."""
        constraints = {"target": "invalid_target"}
        result = execute_research_protocol(constraints, self.mock_tools)
        self.assertEqual(
            result,
            "Error: The provided constraints do not map to a recognized research protocol.",
        )

    def test_missing_parameters(self):
        """Verify it returns an error if required parameters are missing."""
        constraints = {"target": "local_filesystem", "scope": "file"}  # Missing 'path'
        result = execute_research_protocol(constraints, self.mock_tools)
        self.assertEqual(result, "Error: 'path' not specified for local file research.")


if __name__ == "__main__":
    unittest.main()
