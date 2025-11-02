import os
import unittest
from tooling.protocol_compiler import compile_protocols

class TestProtocolCompilerPreservesHeader(unittest.TestCase):

    def test_header_and_intermediate_content_preservation(self):
        # Arrange
        header = """# This is a test header
## With multiple lines

---
"""
        intermediate_content = """
This is some intermediate content that should be preserved.
It can span multiple lines.
"""
        yaml_start = "```yaml"
        dummy_agents_md = "AGENTS.md"
        with open(dummy_agents_md, "w") as f:
            f.write(header)
            f.write(intermediate_content)
            f.write(yaml_start + "\n")
            f.write("\n'some: yaml'")


        # Act
        compile_protocols(dummy_agents_md)

        # Assert
        with open(dummy_agents_md, "r") as f:
            content = f.read()
            self.assertTrue(content.startswith(header))
            self.assertIn(intermediate_content, content)

        # Clean up
        os.remove(dummy_agents_md)

if __name__ == '__main__':
    unittest.main()
