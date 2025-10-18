import os
import unittest
import tempfile
import shutil
import json
from unittest.mock import patch

# Add root to path to allow imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.protocol_compiler import main_orchestrator
from utils.file_system_utils import find_protocol_dirs

class TestProtocolCompilerOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.protocols_dir = os.path.join(self.test_dir, 'protocols')
        self.core_module_dir = os.path.join(self.protocols_dir, 'core')
        os.makedirs(self.core_module_dir)

        # Create a dummy schema file
        self.schema_path = os.path.join(self.protocols_dir, 'protocol.schema.json')
        with open(self.schema_path, 'w') as f:
            json.dump({
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "Test Schema",
                "type": "object",
                "properties": {"protocol_id": {"type": "string"}},
                "required": ["protocol_id"]
            }, f)

        # Create a dummy local build script in the core module
        self.core_build_script_path = os.path.join(self.core_module_dir, 'build.py')
        with open(self.core_build_script_path, 'w') as f:
            f.write("""
import os
print("--- Core module build script running ---")
with open('AGENTS.md', 'w') as f:
    f.write('# Core Module AGENTS.md')
""")
        # Create a dummy protocol file for the build script to "compile"
        with open(os.path.join(self.core_module_dir, 'core.protocol.md'), 'w') as f:
            f.write("A core protocol.")


    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_orchestrator_discovers_and_runs_local_build(self):
        """
        Verify the orchestrator finds the local build.py, runs it,
        and generates the root AGENTS.md.
        """
        # We need to patch the configuration constants in protocol_compiler
        # to point to our temporary directory structure.
        root_agents_md_path = os.path.join(self.test_dir, 'AGENTS.md')
        with patch('tooling.protocol_compiler.ROOT_PROTOCOLS_DIR', self.protocols_dir), \
             patch('tooling.protocol_compiler.ROOT_DIR', self.test_dir), \
             patch('tooling.protocol_compiler.ROOT_AGENTS_MD', root_agents_md_path):

            # Run the main orchestrator function
            # We also patch sys.argv to avoid argparse issues
            with patch('sys.argv', ['tooling/protocol_compiler.py']):
                 main_orchestrator()

            # --- Assertions ---
            # 1. Check that the local build script created the module's AGENTS.md
            core_agents_md = os.path.join(self.core_module_dir, 'AGENTS.md')
            self.assertTrue(os.path.exists(core_agents_md))
            with open(core_agents_md, 'r') as f:
                content = f.read()
                self.assertEqual(content, '# Core Module AGENTS.md')

            # 2. Check that the orchestrator created the root AGENTS.md
            root_agents_md = os.path.join(self.test_dir, 'AGENTS.md')
            self.assertTrue(os.path.exists(root_agents_md))

            # 3. Check that the root AGENTS.md links to the core module's AGENTS.md
            with open(root_agents_md, 'r') as f:
                content = f.read()
                self.assertIn('- [Core](protocols/core/AGENTS.md)', content)


if __name__ == '__main__':
    unittest.main()