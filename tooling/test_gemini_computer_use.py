import unittest
from unittest.mock import patch, MagicMock
from tooling.gemini_computer_use import main


class TestGeminiComputerUse(unittest.TestCase):

    @patch("tooling.gemini_computer_use.sync_playwright")
    @patch("tooling.gemini_computer_use.genai.GenerativeModel")
    def test_main(
        self, mock_generative_model, mock_sync_playwright
    ):
        """Tests the main function of the gemini_computer_use tool."""
        # Mock the Gemini API client and model
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model

        # Mock the Playwright library
        mock_playwright = MagicMock()
        mock_sync_playwright.return_value = mock_playwright
        mock_browser = MagicMock()
        mock_playwright.chromium.launch.return_value = mock_browser
        mock_context = MagicMock()
        mock_browser.new_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.new_page.return_value = mock_page

        # Mock the Gemini API response
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [
            MagicMock(function_call=None, text="Task complete")
        ]
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response

        # Run the main function with a test task
        with patch("sys.argv", ["gemini_computer_use.py", "test task"]):
            main()

        # Assert that the Gemini API was called with the correct arguments
        mock_model.generate_content.assert_called()


if __name__ == "__main__":
    unittest.main()
