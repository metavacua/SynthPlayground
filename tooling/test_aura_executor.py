import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

# Add the parent directory to the path to allow imports
sys.path.append(str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))

from tooling.aura_executor import dynamic_agent_call_tool
from tooling.tool_registry import TOOL_REGISTRY

class TestAuraExecutor(unittest.TestCase):

    def test_tool_registry_is_not_empty(self):
        self.assertIsInstance(TOOL_REGISTRY, dict)
        self.assertGreater(len(TOOL_REGISTRY), 0)

    @patch('importlib.import_module')
    def test_dynamic_call_success(self, mock_import_module):
        """Tests that a tool from the registry can be called successfully."""
        mock_tool_module = MagicMock()
        mock_tool_module.main.return_value = "Success"
        mock_import_module.return_value = mock_tool_module

        tool_name = "hdl_prover" # A tool we know is in the registry
        result = dynamic_agent_call_tool(tool_name, "arg1", "arg2")

        # Check that the module was imported with the correct path
        mock_import_module.assert_called_with(TOOL_REGISTRY[tool_name])

        # Check that the main function was called
        mock_tool_module.main.assert_called_once()

        # The dynamic_agent_call_tool wraps results in an interpreter Object
        self.assertEqual(result.value, "Success")

    def test_dynamic_call_tool_not_found(self):
        """Tests that a non-existent tool returns None and prints an error."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = dynamic_agent_call_tool("non_existent_tool")
            self.assertIsNone(result)
            self.assertIn("not found in registry", mock_stderr.getvalue())

    @patch('importlib.import_module')
    def test_dynamic_call_module_not_found(self, mock_import_module):
        """Tests that a tool with a bad module path is handled."""
        mock_import_module.side_effect = ModuleNotFoundError

        with self.assertRaises(ModuleNotFoundError):
            dynamic_agent_call_tool("hdl_prover")

if __name__ == '__main__':
    unittest.main()