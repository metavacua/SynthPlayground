import unittest
from unittest.mock import patch
from tooling.message_user import main as message_user_main


class TestMessageUser(unittest.TestCase):

    @patch("sys.argv", ["tooling/message_user.py", "Hello, world!"])
    @patch("builtins.print")
    def test_main_prints_message(self, mock_print):
        """Tests that the main function prints the message."""
        message_user_main()
        mock_print.assert_called_once_with("[Message User]: Hello, world!")


if __name__ == "__main__":
    unittest.main()
