import unittest
from unittest.mock import patch, mock_open
from tooling.research_planner import plan_deep_research

class TestResearchPlanner(unittest.TestCase):
    """
    Tests for the research planner tool.
    """

    @patch("builtins.open", new_callable=mock_open, read_data='```json\n{"protocol_id": "mock-protocol"}\n```')
    def test_plan_deep_research_local_repo(self, mock_file):
        """
        Verify that plan_deep_research generates a valid plan for the 'local' repository.
        """
        topic = "The Impact of AI on Software Development"
        plan = plan_deep_research(topic, repository='local')

        # 1. Verify basic properties
        self.assertIsInstance(plan, str)

        # 2. Verify context block with correct markdown formatting
        self.assertIn(f"- **Topic:** {topic}", plan)
        self.assertIn("- **Repository Context:** local", plan)
        self.assertIn("- **Governing Protocol:** `AGENTS.md`", plan)

        # 3. Verify structure
        self.assertIn("## 1. Research Context", plan)
        self.assertIn("## 2. Research Phases", plan)
        self.assertIn("### Phase A: Initial Planning & Question Formulation", plan)
        self.assertIn("## 3. Protocol Reference Snippet", plan)

        # 4. Verify content
        self.assertIn('"protocol_id": "mock-protocol"', plan)
        self.assertIn("execute_research_protocol", plan)

        # 5. Verify mock usage
        mock_file.assert_called_once_with("AGENTS.md", "r")

    @patch("tooling.research_planner.execute_research_protocol")
    def test_plan_deep_research_external_repo(self, mock_execute_research):
        """
        Verify that plan_deep_research generates a valid plan for the 'external' repository.
        """
        mock_execute_research.return_value = "Mocked external file content"

        topic = "External Toolchain Analysis"
        plan = plan_deep_research(topic, repository='external')

        # 1. Verify context block with correct markdown formatting
        self.assertIn(f"- **Topic:** {topic}", plan)
        self.assertIn("- **Repository Context:** external", plan)
        self.assertIn("- **Governing Protocol:** `src/open_deep_research/deep_researcher.py`", plan)

        # 2. Verify content
        self.assertIn("Mocked external file content", plan)

        # 3. Verify the mock was called correctly
        expected_path = "src/open_deep_research/deep_researcher.py"
        mock_execute_research.assert_called_once_with({
            "target": "external_repository",
            "path": expected_path
        })

if __name__ == '__main__':
    unittest.main()