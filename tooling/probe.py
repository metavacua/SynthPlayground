import os
import time
import urllib.request

def probe_filesystem():
    """Checks if the agent can create and delete a temporary file."""
    try:
        test_file = "probe_test.tmp"
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return "Read/Write OK"
    except Exception as e:
        return f"Read/Write FAILED: {e}"

def probe_network():
    """Measures latency to a reliable external service."""
    url = "http://example.com"
    try:
        start_time = time.time()
        with urllib.request.urlopen(url, timeout=5) as response:
            response.read()
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # in milliseconds
        return f"Network OK (Latency: {latency:.2f} ms)"
    except Exception as e:
        return f"Network FAILED: {e}"

def main():
    """Runs all probes and prints a capability report."""
    print("--- VM Capability Report ---")
    print(f"File System: {probe_filesystem()}")
    print(f"Network    : {probe_network()}")
    print("--------------------------")

if __name__ == "__main__":
    main()