# AGENTS.md

This file provides instructions for AI coding agents to interact with this project.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture.

## Build & Commands

This repository uses a hierarchical, decentralized protocol system. Each of the following directories contains a self-contained set of protocols and is compiled by its own local build script.
- [Compliance](protocols/compliance/AGENTS.md)
- [Core](protocols/core/AGENTS.md)
- [Critic](protocols/critic/AGENTS.md)
- [Experimental](protocols/experimental/AGENTS.md)
- [Security](protocols/security/AGENTS.md)
- [Self-improvement](protocols/self_improvement/AGENTS.md)
- [Testing](protocols/testing/AGENTS.md)

### Dependency Installation

General protocols are defined in the [root protocol module](./protocols/AGENTS.md).
To install all required Python packages, run:
```bash
make install
```

### Running Tests

To run the full suite of unit tests, use the following command:
```bash
make test
```

## Code Style

This project uses standard Python code quality tools.

### Linting

To check the code for style issues, run the linter:
```bash
make lint
```

### Formatting

To automatically format the code, run:
```bash
make format
```

## Executable Agent Instructions

This `AGENTS.md` file can be executed to perform the tasks described above. To run the agent, use the following command:

```bash
python3 AGENTS.md
```

```python
import subprocess
import re

def execute_commands_from_agents_md():
    with open(__file__, 'r') as f:
        content = f.read()

    commands = re.findall(r'```bash\n(.*?)\n```', content, re.DOTALL)

    for command in commands:
        print(f"Executing command: {command}")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Command executed successfully.")
            if stdout:
                print("Output:")
                print(stdout.decode())
        else:
            print("Command failed.")
            if stderr:
                print("Error:")
                print(stderr.decode())

if __name__ == '__main__':
    execute_commands_from_agents_md()
```
