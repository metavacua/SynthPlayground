# tests/aura/test_aura_integration.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import unittest
import subprocess

class TestAuraIntegration(unittest.TestCase):
    def test_aura_integration(self):
        result = subprocess.run(
            ["python3", "tooling/aura/aura_executor.py", "tests/aura/integration_test.aura"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout.strip(), "Success!")

if __name__ == "__main__":
    unittest.main()
