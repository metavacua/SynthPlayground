import unittest
import os
import shutil
from unittest.mock import patch
from tooling.protocol_compiler import main_hierarchical_compiler, find_protocol_dirs, generate_root_agents_md

class TestHierarchicalCompiler(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_hierarchical_compiler_dir"
        self.protocols_dir = os.path.join(self.test_dir, "protocols")
        self.core_dir = os.path.join(self.protocols_dir, "core")
        self.compliance_dir = os.path.join(self.protocols_dir, "compliance")
        os.makedirs(self.core_dir)
        os.makedirs(self.compliance_dir)

        # Create dummy protocol files
        with open(os.path.join(self.protocols_dir, "root.protocol.md"), "w") as f:
            f.write("# Root Protocol")
        with open(os.path.join(self.core_dir, "core.protocol.json"), "w") as f:
            f.write('{"protocol_id": "core-001", "description": "Core protocol", "rules": []}')
        with open(os.path.join(self.compliance_dir, "compliance.protocol.md"), "w") as f:
            f.write("# Compliance Protocol")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_find_protocol_dirs(self):
        """Tests that all protocol directories are found."""
        dirs = find_protocol_dirs(self.protocols_dir)
        self.assertIn(self.protocols_dir, dirs)
        self.assertIn(self.core_dir, dirs)
        self.assertIn(self.compliance_dir, dirs)

    def test_generate_root_agents_md(self):
        """Tests the generation of the root AGENTS.md file."""
        root_agents_md = os.path.join(self.test_dir, "AGENTS.md")
        with patch('tooling.protocol_compiler.ROOT_DIR', self.test_dir):
            with patch('tooling.protocol_compiler.ROOT_PROTOCOLS_DIR', self.protocols_dir):
                 with patch('tooling.protocol_compiler.ROOT_AGENTS_MD', root_agents_md):
                    generate_root_agents_md([self.core_dir, self.compliance_dir])

        self.assertTrue(os.path.exists(root_agents_md))
        with open(root_agents_md, "r") as f:
            content = f.read()
            self.assertIn("# Root Protocol", content)
            self.assertIn("[Core](protocols/core/AGENTS.md)", content)
            self.assertIn("[Compliance](protocols/compliance/AGENTS.md)", content)

    @patch('tooling.protocol_compiler.compile_single_module')
    def test_main_hierarchical_compiler(self, mock_compile_single_module):
        """Tests the main orchestration logic."""
        mock_compile_single_module.return_value = (True, "")
        with patch('sys.argv', ['tooling/protocol_compiler.py', '--knowledge-graph-file', 'test.ttl']):
            with patch('tooling.protocol_compiler.ROOT_PROTOCOLS_DIR', self.protocols_dir):
                with patch('tooling.protocol_compiler.generate_root_agents_md') as mock_generate_root:
                    main_hierarchical_compiler()

        self.assertEqual(mock_compile_single_module.call_count, 3)
        mock_generate_root.assert_called_once()


if __name__ == '__main__':
    unittest.main()