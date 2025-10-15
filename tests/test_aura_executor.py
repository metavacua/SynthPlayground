import unittest
import sys
import subprocess
from pathlib import Path

class TestAuraExecutor(unittest.TestCase):

    def test_integration_demo_end_to_end_subprocess(self):
        # Get the path to the python executable
        python_executable = sys.executable
        # Get the path to the aura_executor.py script
        executor_path = Path(__file__).resolve().parent.parent / "src" / "tooling" / "aura_executor.py"
        # Get the path to the integration_demo.aura script
        script_path = Path(__file__).resolve().parent.parent / "integration_demo.aura"

        # Run the aura_executor.py script as a subprocess
        process = subprocess.Popen(
            [python_executable, str(executor_path), str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        output = stdout + stderr

        # Check the output
        print(f"Aura executor output:\n---\n{output}\n---")
        self.assertIn("Provable", output)
        self.assertIn("[Message User]: Integration demo complete!", output)

if __name__ == '__main__':
    unittest.main()