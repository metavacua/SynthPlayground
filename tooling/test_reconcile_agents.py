import unittest
import os
import shutil
from collections import OrderedDict

# Import the functions to be tested
from reconcile_agents import (
    load_archived_agents,
    parse_agent_md,
    reconcile_versions,
    generate_reconciled_md,
    write_report
)

class TestReconcileAgents(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for test artifacts."""
        self.test_dir = "temp_test_reconciliation"
        self.input_dir = os.path.join(self.test_dir, "agents_archive")
        os.makedirs(self.input_dir, exist_ok=True)

    def tearDown(self):
        """Remove the temporary directory after tests."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_archived_agents(self):
        """Test loading of archived agent files."""
        # Create dummy files
        with open(os.path.join(self.input_dir, "main_AGENTS.md"), "w") as f:
            f.write("Content from main")
        with open(os.path.join(self.input_dir, "feat_test_agent.md"), "w") as f:
            f.write("Content from feat_test")

        loaded_data = load_archived_agents(self.input_dir)

        self.assertEqual(len(loaded_data), 2)
        self.assertIn("main", loaded_data)
        self.assertIn("feat_test", loaded_data)
        self.assertEqual(loaded_data["main"], "Content from main")
        self.assertEqual(loaded_data["feat_test"], "Content from feat_test")

    def test_parse_agent_md(self):
        """Test parsing of AGENTS.md content."""
        content = (
            "Preamble content.\n\n"
            "## Section 1\n\n"
            "Content of section 1.\n\n"
            "## Section 2\n\n"
            "Content of section 2."
        )
        parsed = parse_agent_md(content)

        expected = OrderedDict([
            ("Preamble", "Preamble content."),
            ("## Section 1", "Content of section 1."),
            ("## Section 2", "Content of section 2.")
        ])

        self.assertEqual(parsed, expected)

    def test_reconcile_versions_no_conflict(self):
        """Test reconciliation with no conflicts, only additions."""
        parsed_agents = {
            "main": OrderedDict([
                ("## Section 1", "Content 1")
            ]),
            "feat_add": OrderedDict([
                ("## Section 1", "Content 1"),
                ("## Section 2", "New Section Content")
            ])
        }
        reconciled, report = reconcile_versions(parsed_agents, "main")

        # Check that the new section was added
        self.assertIn("## Section 2", reconciled)
        self.assertEqual(reconciled["## Section 2"], "New Section Content")
        self.assertIn("New Section Added", report)

    def test_reconcile_versions_with_conflict(self):
        """Test reconciliation with conflicting content."""
        parsed_agents = {
            "main": OrderedDict([
                ("## Section 1", "Original Content")
            ]),
            "feat_conflict": OrderedDict([
                ("## Section 1", "Conflicting Content")
            ])
        }
        reconciled, report = reconcile_versions(parsed_agents, "main")

        # Check that conflict markers are present
        self.assertIn("<<<<<<<", reconciled["## Section 1"])
        self.assertIn("=======", reconciled["## Section 1"])
        self.assertIn(">>>>>>>", reconciled["## Section 1"])
        self.assertIn("Original Content", reconciled["## Section 1"])
        self.assertIn("Conflicting Content", reconciled["## Section 1"])
        self.assertIn("Conflict Detected", report)

    def test_reconcile_base_branch_not_found(self):
        """Test that an error is raised if the base branch is not found."""
        parsed_agents = {"feat_a": OrderedDict(), "feat_b": OrderedDict()}
        with self.assertRaises(ValueError):
            reconcile_versions(parsed_agents, "main")

    def test_file_generation(self):
        """Test the generation of output files."""
        reconciled_data = OrderedDict([("## Test", "Test Content")])
        report_content = "This is a test report."

        output_file = os.path.join(self.test_dir, "output.md")
        report_file = os.path.join(self.test_dir, "report.md")

        generate_reconciled_md(reconciled_data, output_file)
        write_report(report_content, report_file)

        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.exists(report_file))

        with open(output_file, "r") as f:
            self.assertIn("Test Content", f.read())
        with open(report_file, "r") as f:
            self.assertEqual(f.read(), report_content)

if __name__ == "__main__":
    unittest.main()