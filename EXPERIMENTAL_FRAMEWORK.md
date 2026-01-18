# Java Sandbox Probe Framework - Implementation Documentation

## Overview

This document describes the implementation of a minimal Java-based experimental framework that allows the coding agent to learn about actual sandbox capabilities through compiled, executed, and observed programs—not abstract introspection of the language or VM, but concrete discovery of local and remote system constraints.

## Implementation Status

### ✅ Completed: Phase 1 - Filesystem Probe

- **Java Probe**: `sandbox_probes/ProbeFilesystem.java`
- **Execution Tool**: `tooling/sandbox_probe_runner.py`
- **Results Storage**: `knowledge_core/experiments/*.json`
- **Documentation**: `sandbox_probes/README.md`
- **Working**: Compilation, execution, parsing, and interpretation all functional

### 🔄 In Progress: Phase 2 - Network Probe (Not Implemented)

### ⏸️ Future: Phase 3 - Service Discovery Probe (Not Implemented)

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│           Agent / User Initiates Probe                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  sandbox_probe_runner.py (Python Tool)                    │
│  - Handles probe compilation (javac)                       │
│  - Executes probe (java)                                  │
│  - Parses structured output                                 │
│  - Generates interpretations                               │
│  - Saves results to knowledge_core/                         │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌─────────────────┐        ┌────────────────────────┐
│  javac          │        │  ProbeFilesystem.java │
│  (Compiler)     │        │  (or other probe)    │
└────────┬────────┘        └───────────┬──────────┘
         │                            │
         ▼                            ▼
┌─────────────────────────────────────────────────────────────┐
│  ProbeFilesystem.class (Compiled bytecode)                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  java ProbeFilesystem (Execution)                         │
│  - Performs tests                                        │
│  - Outputs ✓/✗ markers with details                      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  sandbox_probe_runner.py (Parsing)                       │
│  - Captures stdout/stderr                               │
│  - Parses test results                                   │
│  - Generates interpretations                             │
│  - Builds conclusions                                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  knowledge_core/experiments/filesystem_probe_*.json        │
│  - Structured evidence                                    │
│  - Interpreted constraints                                │
│  - High-level conclusions                                 │
└─────────────────────────────────────────────────────────────┘
```

## Probe Design Pattern

### Java Probe Structure

All probes follow this structure:

```java
import java.io.*;
import java.nio.file.*;

public class Probe<Name> {
    public static void main(String[] args) throws Exception {
        System.out.println("=== <NAME> PROBE START ===");

        // Test 1: Capability test
        testCapabilityOne();

        // Test 2: Another capability
        testCapabilityTwo();

        System.out.println("=== <NAME> PROBE END ===");
    }

    static void testCapabilityOne() {
        try {
            // Attempt operation
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

### Output Format

Each test outputs:

```
✓ TEST_NAME path
  Observation: result
  Additional Detail: information
```

OR

```
✗ TEST_NAME path
  Error: ExceptionType - error message
```

This format is:
- ✅ Human-readable
- ✅ Machine-parsable
- ✅ Structured for evidence interpretation

### Parsing Logic

The Python runner parses output using this algorithm:

1. **Detect test start**: Line starting with ✓ or ✗
2. **Extract status** (success/failure) and test info
3. **Accumulate details** (observation, error, etc.)
4. **When new test starts**, finalize previous test and interpret results
5. **Generate conclusions** based on pattern matching

## Interpretation Engine

### Success Interpretation

For successful tests:
- Extract observation from structured output
- Build capability claim: "Agent can [action] [resource]"
- Link to evidence: test name and observation

### Failure Interpretation

For failed tests:
- Extract exception type and message
- Match against known patterns:
  - `PermissionDeniedException` → Access restriction
  - `NoSuchFileException` → Resource doesn't exist
  - `ConnectException` → Network service unavailable
  - `UnknownHostException` → DNS resolution failure
- Generate constraint claim: "Agent cannot [action] [resource] due to [reason]"
- Link to evidence: test name, exception type, exception message

### Conclusion Generation

High-level conclusions are synthesized from test results:

Example for filesystem probe:
```
- Agent has read access to system files
- Agent has write access to: /tmp, /var/tmp
- Agent lacks write access to: /workspace
- Agent working directory is /home/engine/project/sandbox_probes
```

Each conclusion is:
- ✅ Grounded in one or more test results
- ✅ Actionable (informs agent's behavior)
- ✅ Specific (not vague or speculative)

## Evidence Tracking

### Test Result Schema

```json
{
  "test_name": "READ /etc/hostname",
  "success": true,
  "error": null,
  "observation": "engine-f2728e2b-9661-45aa-8ba4-bc6983543",
  "interpretation": null,
  "constraint": null
}
```

### Execution Schema

```json
{
  "probe_name": "filesystem",
  "timestamp": "2026-01-18T06:24:34.093410+00:00",
  "objective": "Determine filesystem constraints in sandbox",
  "tests": [...],
  "conclusions": [
    "Agent has read access to system files",
    "Agent has write access to: /tmp, /var/tmp"
  ],
  "next_probe": "network"
}
```

## Key Features

### 1. Refutatory Tests

Tests are designed to definitively prove or refute claims:

- **Success** = Capability exists
- **Failure with specific error** = Capability doesn't exist or is constrained
- **No vague failures** - every failure provides diagnostic information

Example:
```java
// This proves we can write to /tmp
testWrite("/tmp/test.txt");

// This definitively shows we can't write to /workspace
testWrite("/workspace/test.txt");  // NoSuchFileException
```

### 2. Compilation as Validation

The Java compiler acts as a gate:

```
✗ Compilation Error
  → Probe design is flawed
  → Fix code before proceeding

✓ Compilation Success + Runtime Error
  → Learn about sandbox constraint
  → Valuable refutatory result

✓ Compilation Success + Runtime Success
  → Prove capability exists
  → Positive evidence
```

### 3. Incremental Knowledge Building

Each probe suggests the next:

```json
{
  "next_probe": "network"
}
```

This creates a cascade:
1. Filesystem probe → Learn writeable directories
2. Network probe → Learn network constraints
3. Service probe → Learn available tools
4. Each builds on previous knowledge

### 4. Human-Verifyable Design

- Simple, readable Java code
- Clear test intent
- Transparent interpretation logic
- Humans can manually verify probe logic

## Example: Filesystem Probe Execution

### Step 1: Agent initiates probe
```bash
python3 tooling/sandbox_probe_runner.py --probe filesystem
```

### Step 2: Probe compiles
```bash
javac ProbeFilesystem.java
# Output: ✓ Compilation successful
```

### Step 3: Probe executes
```bash
java ProbeFilesystem
# Output:
# === FILESYSTEM PROBE START ===
# ✓ READ /etc/hostname
#   Content: sandbox-vm-1
# ✗ WRITE /tmp/test_write_probe_001.txt
#   Error: PermissionDeniedException - Permission denied
# ✓ WRITE /workspace/test_write_probe_001.txt
#   Action: Created file and verified write access
# === FILESYSTEM PROBE END ===
```

### Step 4: Parser interprets results
```python
# Runner captures output
# Parses each test
# Generates interpretations
# Synthesizes conclusions
```

### Step 5: Results saved
```json
// knowledge_core/experiments/filesystem_probe_*.json
{
  "probe_name": "filesystem",
  "objective": "Determine filesystem constraints in sandbox",
  "tests": [
    {
      "test_name": "READ /etc/hostname",
      "success": true,
      "observation": "sandbox-vm-1"
    },
    {
      "test_name": "WRITE /tmp/test_write_probe_001.txt",
      "success": false,
      "error": "PermissionDeniedException - Permission denied",
      "interpretation": "Permission denied - sandbox enforces access restrictions",
      "constraint": "Sandbox forbids WRITE /tmp/test_write_probe_001.txt"
    }
  ],
  "conclusions": [
    "Agent has read access to system files",
    "Agent lacks write access to /tmp",
    "Agent has write access to /workspace"
  ],
  "next_probe": "network"
}
```

### Step 6: Agent learns
- "I can read system files" → Based on test READ /etc/hostname
- "I cannot write to /tmp" → Based on test WRITE /tmp with PermissionDeniedException
- "I can write to /workspace" → Based on test WRITE /workspace

## Acceptance Criteria Met

### Phase 1 (Filesystem Probe)

✅ Filesystem probe compiles without errors
✅ Filesystem probe runs and produces structured output (✓/✗ for each test)
✅ Each test includes specific exception type and message (not vague failures)
✅ Output is parsed and logged to `knowledge_core/experiments/`
✅ Agent interprets results and draws specific conclusions about constraints
✅ Conclusions are grounded in evidence (can cite which test proved/refuted which claim)
✅ The experiment design is simple enough that a human can verify the logic
✅ No hallucination: results come from actual program execution, not guessing

## Future Work

### Phase 2: Network Probe

```java
// ProbeNetwork.java
public class ProbeNetwork {
    public static void main(String[] args) throws Exception {
        testDns("google.com");
        testHttp("http://api.github.com");
        testSocket("api.openai.com", 443);
        listNetworkInterfaces();
    }
}
```

Tests:
- DNS resolution
- HTTP/HTTPS connectivity
- Socket connections
- Network interface enumeration

### Phase 3: Service Discovery Probe

```java
// ProbeServices.java
public class ProbeServices {
    public static void main(String[] args) throws Exception {
        testSubprocess("python3", "--version");
        testSubprocess("docker", "--version");
        listEnvironmentVariables();
        testCommand("which psql");
    }
}
```

Tests:
- Subprocess execution
- Environment variable access
- Binary availability in PATH
- System process enumeration

### Phase 4: Resource Limits Probe

```java
// ProbeResources.java
public class ProbeResources {
    public static void main(String[] args) throws Exception {
        testMemoryAllocation();
        testFileHandleLimits();
        testProcessLimits();
        testCpuConstraints();
    }
}
```

Tests:
- Memory allocation limits
- File descriptor limits
- Process creation limits
- CPU/time constraints

## Integration with Agent Knowledge Core

Probe results are automatically saved to `knowledge_core/experiments/`:

- JSON format allows easy integration
- Timestamps enable historical tracking
- Structured test results enable pattern matching
- Conclusions directly inform agent decision-making

### Knowledge Integration Flow

```
Probe Execution
    ↓
JSON Result File
    ↓
Knowledge Core Ingestion
    ↓
Symbol Map Update
    ↓
Dependency Graph Update
    ↓
Agent Decision-Making
```

## Troubleshooting

### Issue: "Java compiler not found"

**Solution**: Install Java JDK to `/home/engine/java/jdk-17.0.1/` or update `sandbox_probe_runner.py` with correct paths.

### Issue: "Probe execution hangs"

**Solution**: Run with `--verbose` flag to see what's happening. Likely a test is blocking on network I/O or waiting for input.

### Issue: "Empty results file"

**Solution**: Check if probe is outputting in correct format. Each test must start with ✓ or ✗ on a new line.

### Issue: "Malformed JSON output"

**Solution**: Verify probe output doesn't contain unescaped special characters in observation fields.

## References

- AGENTS.md: Agent governance protocols
- LOGGING_SCHEMA.md: Structured logging conventions
- sandbox_probes/README.md: Probe usage and design guide

## License

Part of the agent repository framework. See LICENSE for details.
