# Quick Start Guide: Java Sandbox Probe Framework

## Installation (Already Complete)

Java 17 (OpenJDK) is installed at `/home/engine/java/jdk-17.0.1/`

## Run a Probe

```bash
# Basic usage
python3 tooling/sandbox_probe_runner.py --probe filesystem

# With verbose output (for debugging)
python3 tooling/sandbox_probe_runner.py --probe filesystem --verbose
```

## View Results

Results are automatically saved to `knowledge_core/experiments/`:

```bash
# List all experiment results
ls -l knowledge_core/experiments/

# View the latest filesystem probe
cat knowledge_core/experiments/filesystem_probe_*.json | jq .
```

## Understanding Results

### Example JSON Result

```json
{
  "probe_name": "filesystem",
  "timestamp": "2026-01-18T06:29:31Z",
  "objective": "Determine filesystem constraints in sandbox",
  "tests": [
    {
      "test_name": "READ /etc/hostname",
      "success": true,
      "error": null,
      "observation": "sandbox-vm-1",
      "interpretation": null,
      "constraint": null
    }
  ],
  "conclusions": [
    "Agent has read access to system files"
  ],
  "next_probe": "network"
}
```

### Key Fields

- **test_name**: What was tested
- **success**: Whether the test succeeded (true/false)
- **observation**: What was observed (if successful)
- **error**: Exception details (if failed)
- **interpretation**: What the failure means
- **constraint**: What sandbox boundary was hit
- **conclusions**: High-level learnings
- **next_probe**: Suggested next probe to run

## Run Tests

```bash
# Run all probe framework tests
python3 tests/test_sandbox_probe_runner.py
```

Expected output: 21 tests passing

## Create a New Probe

1. Write Java probe in `sandbox_probes/ProbeName.java`
2. Follow output format (✓/✗ markers, structured details)
3. Add probe name to `tooling/sandbox_probe_runner.py` objectives dictionary
4. Test the new probe
5. Update documentation

Example probe structure:

```java
import java.io.*;

public class ProbeMyTest {
    public static void main(String[] args) throws Exception {
        System.out.println("=== MY_TEST PROBE START ===");

        // Test something
        try {
            doSomething();
            System.out.println("✓ MY_TEST target");
            System.out.println("  Observation: " + result);
        } catch (Exception e) {
            System.out.println("✗ MY_TEST target");
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }

        System.out.println("=== MY_TEST PROBE END ===");
    }
}
```

## File System Probe Results

The filesystem probe tests:

1. **Read** `/etc/hostname` - System file access
2. **Write** to `/workspace` - Workspace write access
3. **Write** to `/tmp` - Temp directory write access
4. **Write** to `/var/tmp` - Alternative temp write access
5. **Working Directory** - Current directory identification
6. **List** `/workspace` - Directory listing
7. **List** `/tmp` - Temp directory listing
8. **Read** from project - Project file access
9. **Create Directory** - Directory creation
10. **Delete Directory** - Directory deletion

## Common Commands

```bash
# Run filesystem probe
python3 tooling/sandbox_probe_runner.py --probe filesystem

# Run with verbose mode
python3 tooling/sandbox_probe_runner.py --probe filesystem --verbose

# View latest results
ls -lt knowledge_core/experiments/ | head -5

# Read latest JSON result
cat knowledge_core/experiments/filesystem_probe_*.json | jq .

# Run tests
python3 tests/test_sandbox_probe_runner.py

# View Java probe code
cat sandbox_probes/ProbeFilesystem.java

# Check for compiled .class files
ls -l sandbox_probes/*.class
```

## Troubleshooting

### Issue: "Java compiler not found"
```bash
# Check Java installation
ls -l /home/engine/java/jdk-17.0.1/bin/javac
ls -l /home/engine/java/jdk-17.0.1/bin/java
```

### Issue: "Probe file not found"
```bash
# Check probe exists
ls -l sandbox_probes/Probe*.java
```

### Issue: "Empty results"
```bash
# Run with verbose to see what's happening
python3 tooling/sandbox_probe_runner.py --probe filesystem --verbose
```

## Documentation

- **User Guide**: `sandbox_probes/README.md`
- **Implementation Docs**: `EXPERIMENTAL_FRAMEWORK.md`
- **Phase 1 Summary**: `PHASE1_COMPLETION_SUMMARY.md`
- **AGENTS.md**: Agent governance protocols

## Quick Reference: Test Output Format

### Success
```
✓ TEST_NAME path_or_target
  Observation: result
  Additional Detail: information
```

### Failure
```
✗ TEST_NAME path_or_target
  Error: ExceptionType - error message
```

## What the Agent Learned

From filesystem probe execution:

✅ Can read: `/etc/hostname`, project files
✅ Can write to: `/tmp`, `/var/tmp`
❌ Cannot write to: `/workspace` (doesn't exist)
📍 Working directory: `/home/engine/project/sandbox_probes`

This evidence allows the agent to:
- Use `/tmp` for temporary files
- Avoid `/workspace` operations
- Read system configuration
- Store results with confidence

## Next Steps

After filesystem probe, the framework suggests:
- **Next probe**: `network`

(Implementation of network probe is Phase 2, not yet implemented)

## Support

For issues or questions:
1. Check documentation in `sandbox_probes/README.md`
2. Review implementation in `EXPERIMENTAL_FRAMEWORK.md`
3. Run tests to verify: `python3 tests/test_sandbox_probe_runner.py`
4. Check Phase 1 summary: `PHASE1_COMPLETION_SUMMARY.md`
