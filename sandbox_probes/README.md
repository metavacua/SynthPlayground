# Java Sandbox Probe Framework

## Overview

This framework allows an AI agent to learn about its operational environment through **designed experiments**: write a small Java program, compile it, run it, observe the result, and interpret what the outcome reveals about the sandbox's actual capabilities and constraints.

Success is measured by what the LLM learns about its local and remote operational space—whether through successful experiments that prove a capability exists, or through well-designed *refutatory* experiments that definitively show a capability is absent or constrained.

## Critical Design Principles

### 1. Evidence-Based Interpretation

**Not acceptable**: "Docker probably isn't installed because I don't remember seeing it mentioned"

**Acceptable**: "Docker is not in PATH. Attempted `docker --version`, got ProcessBuilder exception: 'docker: command not found'. Conclusion: Docker binary is not installed or not accessible in this sandbox."

### 2. Structured Failure Diagnostics

Each test failure must include:
- **What was attempted**: The exact operation
- **What happened**: Specific exception type and message
- **What it means**: Interpretation of why it failed
- **What constraint this reveals**: What sandbox boundary does this hit?

### 3. Incremental Validation

- Start with Phase 1 (filesystem) until it's solid
- Don't move to Phase 2 until Phase 1 works reliably
- Each new probe is built on what the previous learned
- Library of experiments grows slowly but with high confidence in each one

### 4. Compilation as Validation Gate

The Java compiler is a hard filter:
- **If it doesn't compile**, the experiment design is flawed (syntax/type error)
- **If it compiles but crashes at runtime**, we've learned something about the sandbox
- **If it runs successfully**, we've proven a capability

No hallucination possible: either the program compiles or it doesn't; either it runs or it doesn't.

## Directory Structure

```
sandbox_probes/
├── README.md                          # This file
├── ProbeFilesystem.java               # Phase 1: Filesystem constraints
├── ProbeNetwork.java                  # Phase 2: Network capabilities (future)
└── ProbeServices.java                 # Phase 3: Service discovery (future)

tooling/
└── sandbox_probe_runner.py            # Probe execution and result parsing

knowledge_core/experiments/
├── filesystem_probe_20260118_062434.json    # Execution results
├── network_probe_*.json                      # (future)
└── services_probe_*.json                    # (future)
```

## Usage

### Running a Probe

```bash
# Run the filesystem probe
python3 tooling/sandbox_probe_runner.py --probe filesystem

# Run with verbose output for debugging
python3 tooling/sandbox_probe_runner.py --probe filesystem --verbose
```

### Understanding Probe Output

Each probe produces structured JSON output saved to `knowledge_core/experiments/`:

```json
{
  "probe_name": "filesystem",
  "timestamp": "2026-01-18T06:24:34.093410+00:00",
  "objective": "Determine filesystem constraints in sandbox",
  "tests": [
    {
      "test_name": "READ /etc/hostname",
      "success": true,
      "observation": "engine-f2728e2b-9661-45aa-8ba4-bc6983543",
      "interpretation": null,
      "constraint": null
    },
    {
      "test_name": "WRITE /tmp/test_write_probe_001.txt",
      "success": true,
      "observation": "/tmp/test_write_probe_001.txt",
      "interpretation": null,
      "constraint": null
    },
    {
      "test_name": "WRITE /workspace/test_write_probe_001.txt",
      "success": false,
      "error": "NoSuchFileException - /workspace/test_write_probe_001.txt",
      "observation": null,
      "interpretation": "Resource does not exist or is not accessible",
      "constraint": "Resource /workspace/test_write_probe_001.txt does not exist"
    }
  ],
  "conclusions": [
    "Agent has read access to system files",
    "Agent has write access to: /tmp, /var/tmp",
    "Agent lacks write access to: /workspace",
    "Agent working directory is /home/engine/project/sandbox_probes"
  ],
  "next_probe": "network"
}
```

### Creating a New Probe

1. **Write the Java probe class** in `sandbox_probes/ProbeName.java`

Example structure:
```java
import java.io.*;
import java.nio.file.*;

public class ProbeName {
    public static void main(String[] args) throws Exception {
        System.out.println("=== PROBE_NAME PROBE START ===");

        // Test 1: What you're testing
        testSomething();

        // Test 2: Another test
        testSomethingElse();

        System.out.println("=== PROBE_NAME PROBE END ===");
    }

    static void testSomething() {
        try {
            // Attempt the operation
            doOperation();
            System.out.println("✓ TEST_NAME path_or_target");
            System.out.println("  Observation: " + result);
        } catch (SpecificException e) {
            System.out.println("✗ TEST_NAME path_or_target");
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }
}
```

2. **Update the probe runner** in `tooling/sandbox_probe_runner.py`:
   - Add the probe name to the `objectives` dictionary
   - Optionally add probe-specific conclusion generation logic in `_generate_conclusions()`

3. **Test the probe**:
   ```bash
   python3 tooling/sandbox_probe_runner.py --probe your-probe-name --verbose
   ```

## Phase 1: Filesystem Probe

### Tests Performed

1. **Read** `/etc/hostname` - Test if system files are readable
2. **Write** to `/workspace` - Test if workspace directory allows writes
3. **Write** to `/tmp` - Test if temp directory allows writes
4. **Write** to `/var/tmp` - Test if alternative temp directory allows writes
5. **Working Directory** - Identify the current working directory
6. **List** `/workspace` - Test if workspace directory exists and is listable
7. **List** `/tmp` - Test if temp directory exists and is listable
8. **Read** from project directory - Test if agent can read its own project files
9. **Create Directory** in workspace - Test if directories can be created
10. **Delete Directory** in workspace - Test if directories can be deleted

### Acceptance Criteria (Phase 1)

✓ Filesystem probe compiles without errors
✓ Filesystem probe runs and produces structured output (✓/✗ for each test)
✓ Each test includes specific exception type and message (not vague failures)
✓ Output is parsed and logged to `knowledge_core/experiments/`
✓ Agent interprets results and draws specific conclusions about constraints
✓ Conclusions are grounded in evidence (can cite which test proved/refuted which claim)
✓ The experiment design is simple enough that a human can verify the logic
✓ No hallucination: results come from actual program execution, not guessing

### Example Results

```
✓ READ /etc/hostname
  Content: sandbox-vm-1
✗ WRITE /tmp/test_write_probe_001.txt
  Error: PermissionDeniedException - Permission denied
✓ WRITE /workspace/test_write_probe_001.txt
  Action: Created file and verified write access
  Cleanup: Successfully deleted test file
✓ WORKING_DIRECTORY
  Path: /workspace
✗ LIST /workspace
  Error: DirectoryNotFound - Directory does not exist
```

**Interpretation**:
- "I can read /etc/hostname" → Proof: successfully read it
- "I cannot write to /tmp" → Proof: PermissionDeniedException on write attempt
- "My working directory is /workspace" → Fact: direct observation
- **Conclusion**: Sandbox filesystem is constrained; I have write access only to /workspace

## Future Phases

### Phase 2: Network Access Probe

Test DNS resolution, HTTP/HTTPS connections, network interfaces, and socket operations to determine network capabilities and constraints.

### Phase 3: Service Discovery Probe

Test subprocess execution, environment variables, available binaries, and system processes to discover what services and tools are available in the sandbox.

### Phase 4: Resource Limits Probe

Test memory allocation, CPU usage, file handles, process limits, and other resource constraints.

## Java Requirements

The framework uses Java 17 (OpenJDK) installed locally at:
- JDK path: `/home/engine/java/jdk-17.0.1`
- Compiler: `/home/engine/java/jdk-17.0.1/bin/javac`
- Runtime: `/home/engine/java/jdk-17.0.1/bin/java`

Environment variables are automatically set by the probe runner.

## Key Benefits

1. **Concrete Evidence**: All claims about sandbox capabilities are backed by actual program execution, not speculation
2. **Refutable Tests**: Failures are just as valuable as successes, providing clear diagnostic information
3. **Reproducible**: Experiments can be re-run to verify results across different environments or time periods
4. **Incremental Knowledge**: Each probe builds on the knowledge gained from previous probes
5. **Human-Readable**: Both the Java code and the JSON output are designed for human understanding
6. **Machine-Parsable**: Structured JSON output allows automated analysis and knowledge integration

## Troubleshooting

### "Java compiler not found"
Ensure Java JDK is installed and the `JAVA_HOME` environment variable points to the JDK directory.

### "Probe file not found"
Ensure the probe Java file exists in the `sandbox_probes/` directory with the correct naming convention (e.g., `ProbeFilesystem.java`).

### Empty or malformed output
Run with `--verbose` flag to see raw probe output and diagnose parsing issues.

## Contributing

When adding new probes:

1. Follow the existing naming convention: `Probe<Name>.java`
2. Use the same output format (✓/✗ markers, structured details)
3. Update this README with the new probe's documentation
4. Add test cases for the new probe
5. Ensure conclusions are grounded in evidence

## License

Part of the agent repository framework. See LICENSE for details.
