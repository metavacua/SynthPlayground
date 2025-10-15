import unittest
import sys
import subprocess
from pathlib import Path

class TestAuraExecutor(unittest.TestCase):

    def test_integration_demo_end_to_end_subprocess(self):
        # Get the path to the python executable
        python_executable = sys.executable
        # Get the path to the aura_executor.py script
        executor_path = Path(__file__).resolve().parent.parent / "tooling" / "aura_executor.py"
        # Get the path to the integration_demo.aura script
        script_path = Path(__file__).resolve().parent.parent / "integration_demo.aura"

        # Run the aura_executor.py script as a subprocess
        result = subprocess.run(
            [python_executable, str(executor_path), str(script_path)],
            capture_output=True,
            text=True
        )

        # Check the output
        output = result.stdout
        self.assertIn("Provable", output)
        self.assertIn("Sequent is provable!", output)
        self.assertIn("[Message User]: Integration demo complete!", output)

if __name__ == '__main__':
    unittest.main()