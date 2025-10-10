import unittest
from unittest.mock import patch
from tooling.research import execute_research_protocol

# The native tools are not defined in the module, they are injected globals.
# We use `create=True` to tell the patcher to create the attribute on the
# module during the test, which simulates the agent's execution environment.
@patch('tooling.research.view_text_website', create=True)
@patch('tooling.research.google_search', create=True)
@patch('tooling.research.list_files', create=True)
@patch('tooling.research.read_file', create=True)
class TestResearchExecutor(unittest.TestCase):
    """
    Tests for the research executor tool, mocking the native tools that are
    globally injected by the execution environment.
    """

    def test_local_filesystem_file_scope(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it calls read_file for local file scope."""
        mock_read_file.return_value = "file content"
        constraints = {"target": "local_filesystem", "scope": "file", "path": "test.txt"}

        result = execute_research_protocol(constraints)

        mock_read_file.assert_called_once_with(filepath="test.txt")
        self.assertEqual(result, "file content")
        # Ensure other mocks were not called
        mock_list_files.assert_not_called()
        mock_google_search.assert_not_called()
        mock_view_text_website.assert_not_called()

    def test_local_filesystem_directory_scope(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it calls list_files for local directory scope."""
        mock_list_files.return_value = ["file1.txt", "file2.txt"]
        constraints = {"target": "local_filesystem", "scope": "directory", "path": "test_dir/"}

        result = execute_research_protocol(constraints)

        mock_list_files.assert_called_once_with(path="test_dir/")
        self.assertEqual(result, "file1.txt\nfile2.txt")

    def test_external_web_narrow_scope(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it calls google_search for external narrow scope."""
        mock_google_search.return_value = "search results"
        constraints = {"target": "external_web", "scope": "narrow", "query": "test query"}

        result = execute_research_protocol(constraints)

        mock_google_search.assert_called_once_with(query="test query")
        self.assertEqual(result, "search results")

    def test_external_web_broad_scope(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it calls view_text_website for external broad scope."""
        mock_view_text_website.return_value = "website content"
        constraints = {"target": "external_web", "scope": "broad", "url": "http://example.com"}

        result = execute_research_protocol(constraints)

        mock_view_text_website.assert_called_once_with(url="http://example.com")
        self.assertEqual(result, "website content")

    def test_external_repository_scope(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it calls view_text_website for external repository scope."""
        mock_view_text_website.return_value = "repo file content"
        constraints = {"target": "external_repository", "url": "http://example.com/file.py"}

        result = execute_research_protocol(constraints)

        mock_view_text_website.assert_called_once_with(url="http://example.com/file.py")
        self.assertEqual(result, "repo file content")

    def test_invalid_target(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it returns an error for an invalid target."""
        constraints = {"target": "invalid_target"}
        result = execute_research_protocol(constraints)
        self.assertEqual(result, "Error: The provided constraints do not map to a recognized research protocol.")

    def test_missing_parameters(self, mock_read_file, mock_list_files, mock_google_search, mock_view_text_website):
        """Verify it returns an error if required parameters are missing."""
        constraints = {"target": "local_filesystem", "scope": "file"} # Missing 'path'
        result = execute_research_protocol(constraints)
        self.assertEqual(result, "Error: 'path' not specified for local file research.")

if __name__ == '__main__':
    unittest.main()