import unittest
import os
import shutil
from tooling.self_improvement_cli import create_proposal, PROPOSALS_DIR, PROPOSAL_TEMPLATE

class TestNewSelfImprovementCLI(unittest.TestCase):

    def setUp(self):
        """Set up a clean proposals directory for each test."""
        self.proposals_path = PROPOSALS_DIR
        if os.path.exists(self.proposals_path):
            shutil.rmtree(self.proposals_path)
        os.makedirs(self.proposals_path)

    def tearDown(self):
        """Clean up the proposals directory after each test."""
        if os.path.exists(self.proposals_path):
            shutil.rmtree(self.proposals_path)

    def test_create_proposal_creates_directory_and_file(self):
        """
        Tests that `create_proposal` successfully creates a directory and a
        proposal.md file inside it.
        """
        # Run the function to create the proposal
        proposal_file_path = create_proposal()

        # Check that the returned path is not None and the file exists
        self.assertIsNotNone(proposal_file_path)
        self.assertTrue(os.path.exists(proposal_file_path))

        # Check that the directory was created
        proposal_dir = os.path.dirname(proposal_file_path)
        self.assertTrue(os.path.isdir(proposal_dir))
        self.assertTrue(proposal_dir.startswith(self.proposals_path))

        # Check that the file has the correct name
        self.assertEqual(os.path.basename(proposal_file_path), "proposal.md")

    def test_create_proposal_file_contains_template(self):
        """
        Tests that the generated proposal.md file contains the correct
        template content.
        """
        # Run the function to create the proposal
        proposal_file_path = create_proposal()

        # Read the content of the created file
        with open(proposal_file_path, "r") as f:
            content = f.read()

        # Check if the content matches the template
        self.assertEqual(content, PROPOSAL_TEMPLATE)

    def test_create_proposal_is_idempotent(self):
        """
        Tests that calling create_proposal multiple times results in multiple,
        unique proposal directories.
        """
        # Create two proposals
        proposal_path_1 = create_proposal()
        proposal_path_2 = create_proposal()

        # Check that they are different
        self.assertNotEqual(proposal_path_1, proposal_path_2)

        # Check that both files exist
        self.assertTrue(os.path.exists(proposal_path_1))
        self.assertTrue(os.path.exists(proposal_path_2))

if __name__ == "__main__":
    unittest.main()