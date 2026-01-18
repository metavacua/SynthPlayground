#!/usr/bin/env python3
"""
Sandbox Probe Runner

A tool for running Java-based sandbox probes and interpreting results.
This is the bridge between the agent and the experimental framework.

Usage:
    python3 tooling/sandbox_probe_runner.py --probe filesystem
    python3 tooling/sandbox_probe_runner.py --probe network
    python3 tooling/sandbox_probe_runner.py --probe services
"""

import argparse
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Tuple

# Constants
PROBES_DIR = Path("/home/engine/project/sandbox_probes")
EXPERIMENTS_DIR = Path("/home/engine/project/knowledge_core/experiments")
JAVA_HOME = Path("/home/engine/java/jdk-17.0.1")
JAVAC = JAVA_HOME / "bin" / "javac"
JAVA = JAVA_HOME / "bin" / "java"


class ProbeResult:
    """Represents the result of a single test within a probe."""

    def __init__(
        self,
        test_name: str,
        success: bool,
        error: Optional[str] = None,
        observation: Optional[str] = None,
        interpretation: Optional[str] = None,
        constraint: Optional[str] = None,
    ):
        self.test_name = test_name
        self.success = success
        self.error = error
        self.observation = observation
        self.interpretation = interpretation
        self.constraint = constraint

    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "success": self.success,
            "error": self.error,
            "observation": self.observation,
            "interpretation": self.interpretation,
            "constraint": self.constraint,
        }


class ProbeExecution:
    """Represents a complete probe execution with all tests."""

    def __init__(self, probe_name: str, timestamp: str, objective: str):
        self.probe_name = probe_name
        self.timestamp = timestamp
        self.objective = objective
        self.tests: List[ProbeResult] = []
        self.conclusions: List[str] = []
        self.next_probe: Optional[str] = None

    def add_test(self, result: ProbeResult):
        self.tests.append(result)

    def to_dict(self) -> dict:
        return {
            "probe_name": self.probe_name,
            "timestamp": self.timestamp,
            "objective": self.objective,
            "tests": [test.to_dict() for test in self.tests],
            "conclusions": self.conclusions,
            "next_probe": self.next_probe,
        }


class SandboxProbeRunner:
    """Main class for running sandbox probes."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._setup_environment()

    def _setup_environment(self):
        """Ensure Java is available and directories exist."""
        if not JAVAC.exists():
            raise RuntimeError(f"Java compiler not found at {JAVAC}")
        if not JAVA.exists():
            raise RuntimeError(f"Java runtime not found at {JAVA}")

        PROBES_DIR.mkdir(parents=True, exist_ok=True)
        EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    def _run_command(
        self, cmd: List[str], cwd: Optional[Path] = None
    ) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        if self.verbose:
            print(f"Running: {' '.join(cmd)}")

        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

        if self.verbose:
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"STDERR:\n{result.stderr}")

        return result.returncode, result.stdout, result.stderr

    def compile_probe(self, probe_name: str) -> bool:
        """Compile a Java probe."""
        java_file = PROBES_DIR / f"Probe{probe_name.capitalize()}.java"

        if not java_file.exists():
            raise FileNotFoundError(f"Probe file not found: {java_file}")

        print(f"Compiling probe: {java_file}")
        returncode, stdout, stderr = self._run_command(
            [str(JAVAC), str(java_file)], cwd=PROBES_DIR
        )

        if returncode != 0:
            print(f"✗ Compilation failed: {stderr}")
            return False

        print("✓ Compilation successful")
        return True

    def run_probe(self, probe_name: str) -> ProbeExecution:
        """Compile and run a probe, returning parsed results."""
        # Compile first
        if not self.compile_probe(probe_name):
            raise RuntimeError(f"Probe compilation failed: {probe_name}")

        # Get the probe class name
        class_name = f"Probe{probe_name.capitalize()}"

        # Run the probe
        print(f"\nRunning probe: {class_name}")
        returncode, stdout, stderr = self._run_command(
            [str(JAVA), "-cp", str(PROBES_DIR), class_name], cwd=PROBES_DIR
        )

        if returncode != 0 and stderr:
            print(f"Probe exited with error: {stderr}")

        # Parse the output
        execution = self._parse_probe_output(probe_name, stdout)

        return execution

    def _parse_probe_output(self, probe_name: str, output: str) -> ProbeExecution:
        """Parse probe output into structured data."""
        objectives = {
            "filesystem": "Determine filesystem constraints in sandbox",
            "network": "Determine network capabilities and constraints",
            "services": "Determine available services and system capabilities",
        }

        execution = ProbeExecution(
            probe_name=probe_name,
            timestamp=datetime.now(timezone.utc).isoformat(),
            objective=objectives.get(probe_name, f"Probe {probe_name}"),
        )

        current_test = None

        for line in output.split("\n"):
            line = line.rstrip()

            # Test start markers
            if line.startswith("✓") or line.startswith("✗"):
                # Save previous test if exists
                if current_test:
                    execution.add_test(
                        self._interpret_test(current_test, current_test["details"])
                    )

                # Parse new test
                parts = line.split(" ", 1)
                status = parts[0]
                test_info = parts[1] if len(parts) > 1 else ""

                current_test = {"status": status, "test_info": test_info, "details": []}
            elif current_test:
                # Accumulate details for current test
                if (
                    line.strip().startswith("-")
                    or line.strip().startswith("Error:")
                    or line.strip().startswith("Content:")
                    or line.strip().startswith("Action:")
                    or line.strip().startswith("Cleanup:")
                    or line.strip().startswith("Path:")
                ):
                    current_test["details"].append(line.strip())

        # Don't forget the last test
        if current_test:
            execution.add_test(
                self._interpret_test(current_test, current_test["details"])
            )

        # Generate conclusions based on results
        execution.conclusions = self._generate_conclusions(execution, probe_name)

        # Suggest next probe
        execution.next_probe = self._suggest_next_probe(probe_name)

        return execution

    def _interpret_test(self, test: dict, lines: list) -> ProbeResult:
        """Interpret a single test result."""
        success = test["status"] == "✓"
        test_info = test["test_info"]
        details = test["details"]

        # Extract test name from test_info (handle various formats)
        parts = test_info.split()
        test_name = parts[0] if parts else "unknown"
        test_path = parts[1] if len(parts) > 1 else ""

        if success:
            # Successful test
            observation = None
            for detail in details:
                if detail.startswith("Content:"):
                    observation = detail[8:].strip()
                elif detail.startswith("Path:"):
                    observation = detail[5:].strip()

            # For tests without explicit observation, use the path
            if not observation and test_path:
                observation = test_path

            return ProbeResult(
                test_name=f"{test_name} {test_path}".strip(),
                success=True,
                observation=observation,
            )
        else:
            # Failed test - extract error details
            error = None
            interpretation = None
            constraint = None

            for detail in details:
                if detail.startswith("Error:"):
                    error = detail[6:].strip()

            # Generate interpretation based on test and error
            interpretation = self._interpret_failure(
                f"{test_name} {test_path}".strip(), error
            )
            constraint = self._infer_constraint(
                f"{test_name} {test_path}".strip(), error
            )

            return ProbeResult(
                test_name=f"{test_name} {test_path}".strip(),
                success=False,
                error=error,
                interpretation=interpretation,
                constraint=constraint,
            )

    def _interpret_failure(self, test_name: str, error: Optional[str]) -> str:
        """Interpret what a test failure means."""
        if not error:
            return "Operation failed without specific diagnostic information"

        error_lower = error.lower()

        if "permissiondenied" in error_lower or "accessdenied" in error_lower:
            return "Permission denied - sandbox enforces access restrictions"
        elif "nosuchfile" in error_lower or "notfound" in error_lower:
            return "Resource does not exist or is not accessible"
        elif "filenotfound" in error_lower:
            return "File not found - path does not exist"
        elif "directorynotfound" in error_lower:
            return "Directory not found - path does not exist or is not a directory"
        else:
            return f"Operation failed with error: {error}"

    def _infer_constraint(self, test_name: str, error: Optional[str]) -> str:
        """Infer what constraint a failure reveals."""
        if not error:
            return "Unknown constraint"

        error_lower = error.lower()

        if "permissiondenied" in error_lower:
            return f"Sandbox forbids {test_name.replace('_', ' ')}"
        elif "nosuchfile" in error_lower or "notfound" in error_lower:
            return f"Resource {test_name.split()[1] if len(test_name.split()) > 1 else ''} does not exist"
        else:
            return f"Sandbox constraint on {test_name.replace('_', ' ')}"

    def _generate_conclusions(
        self, execution: ProbeExecution, probe_name: str
    ) -> List[str]:
        """Generate high-level conclusions from test results."""
        conclusions = []

        if probe_name == "filesystem":
            read_success = any(
                t.success and "READ" in t.test_name for t in execution.tests
            )
            write_success = [
                t for t in execution.tests if t.success and "WRITE" in t.test_name
            ]
            write_failures = [
                t for t in execution.tests if not t.success and "WRITE" in t.test_name
            ]

            if read_success:
                conclusions.append("Agent has read access to system files")

            if write_success:
                writable_paths = [t.test_name.split()[1] for t in write_success]
                conclusions.append(
                    f"Agent has write access to: {', '.join(writable_paths)}"
                )

            if write_failures:
                forbidden_paths = [t.test_name.split()[1] for t in write_failures]
                conclusions.append(
                    f"Agent lacks write access to: {', '.join(forbidden_paths)}"
                )

            cwd_test = [
                t for t in execution.tests if t.test_name == "WORKING_DIRECTORY"
            ]
            if cwd_test:
                conclusions.append(
                    f"Agent working directory is {cwd_test[0].observation}"
                )

        return conclusions

    def _suggest_next_probe(self, current_probe: str) -> Optional[str]:
        """Suggest the next probe to run."""
        probe_order = ["filesystem", "network", "services"]

        try:
            idx = probe_order.index(current_probe)
            if idx + 1 < len(probe_order):
                return probe_order[idx + 1]
        except ValueError:
            pass

        return None

    def save_results(self, execution: ProbeExecution) -> Path:
        """Save probe results to knowledge_core/experiments/."""
        filename = f"{execution.probe_name}_probe_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        filepath = EXPERIMENTS_DIR / filename

        with open(filepath, "w") as f:
            json.dump(execution.to_dict(), f, indent=2)

        print(f"\n✓ Results saved to: {filepath}")
        return filepath


def main():
    parser = argparse.ArgumentParser(description="Run sandbox probes")
    parser.add_argument(
        "--probe",
        required=True,
        choices=["filesystem", "network", "services"],
        help="Which probe to run",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    runner = SandboxProbeRunner(verbose=args.verbose)

    try:
        execution = runner.run_probe(args.probe)
        runner.save_results(execution)

        # Print summary
        print(f"\n{'='*60}")
        print("PROBE EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Probe: {execution.probe_name}")
        print(f"Timestamp: {execution.timestamp}")
        print(f"Tests run: {len(execution.tests)}")
        print(f"Passed: {sum(1 for t in execution.tests if t.success)}")
        print(f"Failed: {sum(1 for t in execution.tests if not t.success)}")

        print("\nCONCLUSIONS:")
        for conclusion in execution.conclusions:
            print(f"  - {conclusion}")

        if execution.next_probe:
            print(f"\nNext recommended probe: {execution.next_probe}")

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
