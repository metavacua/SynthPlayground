"""
Performs a series of checks to assess the capabilities of the execution environment.

This script is a critical diagnostic tool run at the beginning of a task to
ensure the agent understands its operational sandbox. It verifies fundamental
capabilities required for most software development tasks:

1.  **Filesystem I/O:** Confirms that the agent can create, write to, read from,
    and delete files. It also provides a basic latency measurement for these
    operations.
2.  **Network Connectivity:** Checks for external network access by attempting to
    connect to a highly-available public endpoint (google.com). This is crucial
    for tasks requiring `git` operations, package downloads, or API calls.
3.  **Environment Variables:** Verifies that standard environment variables are
    accessible, which is a prerequisite for many command-line tools.

The script generates a human-readable report summarizing the results of these
probes, allowing the agent to quickly identify any environmental constraints
that might impact its ability to complete a task.
"""

import os
import time
import uuid
import requests
import datetime


def probe_filesystem():
    """
    Tests file system write/read/delete capabilities and measures latency.
    """
    test_filename = f"probe_{uuid.uuid4()}.tmp"
    test_content = "environmental probe"
    try:
        start_time = time.monotonic()

        # Write
        with open(test_filename, "w") as f:
            f.write(test_content)

        # Read
        with open(test_filename, "r") as f:
            content_read = f.read()

        # Delete
        os.remove(test_filename)

        end_time = time.monotonic()

        if content_read != test_content:
            return "FAIL", "Content mismatch during read-back", "N/A"

        latency_ms = (end_time - start_time) * 1000
        return (
            "PASS",
            "Write, read, and delete operations successful.",
            f"{latency_ms:.2f} ms",
        )

    except Exception as e:
        return "FAIL", f"An exception occurred: {e}", "N/A"


def probe_network():
    """
    Tests network connectivity and measures latency to a reliable external endpoint.
    """
    # Using a reliable, high-availability domain for the test.
    # We use HEAD request as it's lightweight.
    url = "https://www.google.com"
    try:
        start_time = time.monotonic()
        response = requests.head(url, timeout=5)
        end_time = time.monotonic()

        latency_ms = (end_time - start_time) * 1000

        if 200 <= response.status_code < 400:
            return (
                "PASS",
                f"Successfully connected to {url} (Status: {response.status_code})",
                f"{latency_ms:.2f} ms",
            )
        else:
            return (
                "WARN",
                f"Connected to {url}, but received non-OK status: {response.status_code}",
                f"{latency_ms:.2f} ms",
            )

    except requests.Timeout:
        return "FAIL", f"Request to {url} timed out.", "N/A"
    except requests.ConnectionError:
        return "FAIL", f"Connection error when trying to reach {url}.", "N/A"
    except Exception as e:
        return "FAIL", f"An unexpected network error occurred: {e}", "N/A"


def probe_environment_variables():
    """
    Checks for the presence of a common environment variable.
    """
    var_name = "PATH"
    if os.getenv(var_name):
        return "PASS", f"Environment variable '{var_name}' is present.", "N/A"
    else:
        return "WARN", f"Standard environment variable '{var_name}' is not set.", "N/A"


def main():
    """
    Runs all environmental probes and prints a summary report.
    """
    print("--- VM Capability Report ---")
    print(f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    print("-" * 30)

    # Filesystem Probe
    fs_status, fs_msg, fs_latency = probe_filesystem()
    print(f"File System Probe....: {fs_status}")
    print(f"  - Details..........: {fs_msg}")
    print(f"  - Latency..........: {fs_latency}")
    print("-" * 30)

    # Network Probe
    net_status, net_msg, net_latency = probe_network()
    print(f"Network Probe........: {net_status}")
    print(f"  - Details..........: {net_msg}")
    print(f"  - Latency..........: {net_latency}")
    print("-" * 30)

    # Environment Variables Probe
    env_status, env_msg, _ = probe_environment_variables()
    print(f"Environment Vars.....: {env_status}")
    print(f"  - Details..........: {env_msg}")
    print("-" * 30)
    print("--- End of Report ---")


if __name__ == "__main__":
    main()
