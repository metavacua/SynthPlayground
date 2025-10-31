# tests/aura/test_aura_api.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import unittest
from tooling.aura.aura_api import ToolRegistry, Tool, agent_call_tool
from aura_lang.interpreter import Object

class TestAuraAPI(unittest.TestCase):
    def test_tool_registry(self):
        registry = ToolRegistry()
        tool = Tool("test_tool", lambda x: x, "A test tool.")
        registry.register(tool)
        self.assertEqual(registry.get("test_tool"), tool)

    def test_agent_call_tool(self):
        registry = ToolRegistry()
        tool = Tool("test_tool", lambda x: x, "A test tool.")
        registry.register(tool)
        result = agent_call_tool(registry, Object("test_tool"), Object("test"))
        self.assertEqual(result.value, "test")

    def test_agent_call_nonexistent_tool(self):
        registry = ToolRegistry()
        result = agent_call_tool(registry, Object("nonexistent_tool"))
        self.assertEqual(result.value, "Error: Tool 'nonexistent_tool' not found.")

    def test_agent_call_tool_with_incorrect_arguments(self):
        registry = ToolRegistry()
        tool = Tool("test_tool", lambda x: x, "A test tool.")
        registry.register(tool)
        result = agent_call_tool(registry, Object("test_tool"))
        self.assertIn("Error executing tool", result.value)

if __name__ == "__main__":
    unittest.main()
