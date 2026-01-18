#!/usr/bin/env python3
"""
Sandbox Probe Runner - Enhanced Version

Enhanced to handle both filesystem and network probes correctly.
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

        current_test_name = None
        current_test_lines = []

        for line in output.split("\n"):
            line_stripped = line.strip()

            # Network probe format: TEST: test_name
            if line_stripped.startswith("TEST:"):
                # Save previous test if exists
                if current_test_name:
                    self._add_test_to_execution(
                        execution, current_test_name, current_test_lines
                    )

                # Extract test name from TEST: line
                parts = line_stripped.split(" ", 1)
                current_test_name = parts[1].strip() if len(parts) > 1 else ""
                current_test_lines = []

            # Result line (filesystem probe)
            elif (
                line_stripped.startswith("✓") or line_stripped.startswith("✗")
            ) and not line_stripped.startswith("TEST"):
                # Save previous test if exists
                if current_test_name:
                    self._add_test_to_execution(
                        execution, current_test_name, current_test_lines
                    )
                    current_test_lines = []

                # This is a result line
                current_test_lines.append(line_stripped)
            # Detail line
            elif current_test_name:
                # Accumulate details for current test
                if line_stripped:
                    current_test_lines.append(line_stripped)

        # Don't forget the last test
        if current_test_name:
            self._add_test_to_execution(
                execution, current_test_name, current_test_lines
            )

        # Generate conclusions based on results
        execution.conclusions = self._generate_conclusions(execution, probe_name)

        # Suggest next probe
        execution.next_probe = self._suggest_next_probe(probe_name)

        return execution

    def _add_test_to_execution(
        self, execution: ProbeExecution, test_name: str, lines: List[str]
    ):
        """Add a test to the execution by parsing its lines."""
        # Determine if success or failure
        success = False
        observation = None
        error = None
        interpretation = None
        constraint = None

        for line in lines:
            if line.startswith("✓"):
                success = True
            elif line.startswith("✗"):
                success = False
            elif line.startswith("Error:"):
                error = line[6:].strip()
            elif line.startswith("Content:"):
                observation = line[8:].strip()
            elif line.startswith("Observation:") or line.startswith("Observation:"):
                # Handle both spellings
                idx = line.index(":") + 1
                observation = line[idx:].strip()
            elif line.startswith("Operation:"):
                # Extract operation type for network probes
                idx = line.index(":") + 1
                operation = line[idx:].strip()
                if not observation and operation:
                    observation = operation

        # Generate interpretation and constraint for failures
        if not success and error:
            interpretation = self._interpret_failure(test_name, error)
            constraint = self._infer_constraint(test_name, error)

        execution.add_test(
            ProbeResult(
                test_name=test_name,
                success=success,
                error=error,
                observation=observation,
                interpretation=interpretation,
                constraint=constraint,
            )
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
        elif "unknownhost" in error_lower:
            return "DNS resolution failed - hostname not found or DNS unavailable"
        elif "connection refused" in error_lower:
            return "Service is not listening on this port"
        elif "connection timeout" in error_lower or "timeout" in error_lower:
            return "Host is not reachable within timeout period"
        elif "sockettimeout" in error_lower:
            return "Network operation timed out"
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
        elif "unknownhost" in error_lower:
            return "DNS resolution failed or blocked"
        elif "connection refused" in error_lower:
            return f"Port not listening for {test_name}"
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

        elif probe_name == "network":
            dns_tests = [t for t in execution.tests if "dns" in t.test_name.lower()]
            tcp_tests = [t for t in execution.tests if "tcp" in t.test_name.lower()]
            http_tests = [t for t in execution.tests if "http" in t.test_name.lower()]

            dns_success = any(t.success for t in dns_tests)
            tcp_success = any(t.success for t in tcp_tests)
            http_success = any(t.success for t in http_tests)

            dns_failure_count = sum(1 for t in dns_tests if not t.success)
            tcp_failure_count = sum(1 for t in tcp_tests if not t.success)
            http_failure_count = sum(1 for t in http_tests if not t.success)

            if dns_success and dns_failure_count > 0:
                dns_valid = [t for t in dns_tests if t.success]
                dns_invalid = [t for t in dns_tests if not t.success]
                conclusions.append(
                    f"DNS resolution works for {len(dns_valid)}/{len(dns_tests)} hosts (fails for invalid hostnames)"
                )
            elif dns_success and dns_failure_count == 0:
                conclusions.append("DNS resolution works for all tested hostnames")
            elif not dns_success:
                conclusions.append("DNS resolution is unavailable or blocked")

            if tcp_success:
                tcp_valid = [t for t in tcp_tests if t.success]
                tcp_invalid = [t for t in tcp_tests if not t.success]
                conclusions.append(
                    f"TCP connectivity available to {len(tcp_valid)}/{len(tcp_tests)} targets"
                )
                if tcp_valid and tcp_invalid:
                    conclusions.append(
                        f"Some TCP services are reachable ({len(tcp_valid)}), but others are not ({len(tcp_invalid)})"
                    )

            if http_success:
                http_valid = [t for t in http_tests if t.success]
                http_invalid = [t for t in http_tests if not t.success]
                conclusions.append(
                    f"HTTP requests work for {len(http_valid)}/{len(http_tests)} endpoints"
                )

            if not tcp_success and not http_success and not dns_success:
                conclusions.append("Network access appears to be completely blocked")

            if dns_success and not tcp_success and not http_success:
                conclusions.append(
                    "DNS works but connectivity is blocked (likely firewall rules)"
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
