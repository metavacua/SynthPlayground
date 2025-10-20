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
- [CHC Bootstrap](protocols/chc_protocols/bootstrap/README.md)

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

## Jules API Integration

This section provides instructions for interacting with the Jules API, which allows for programmatic access to Jules's capabilities.

### Authentication

To use the Jules API, you need an API key. Pass the API key in the `X-Goog-Api-Key` header of your API calls.

**Important:** Keep your API keys secure. Do not share them or embed them in public code.

### API Concepts

The Jules API is built around a few core resources:

*   **Source:** An input source for the agent (e.g., a GitHub repository).
*   **Session:** A continuous unit of work within a specific context, similar to a chat session. A session is initiated with a prompt and a source.
*   **Activity:** A single unit of work within a Session. A Session contains multiple activities from both the user and the agent.

### Quickstart: Your First API Call

Here’s a quick guide to making your first API call with `curl`.

**Step 1: List your available sources**

Find the name of the source you want to work with (e.g., your GitHub repo).

```bash
curl 'https://jules.googleapis.com/v1alpha/sources' \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

**Step 2: Create a new session**

Create a new session using the source name from the previous step.

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions' \
    -X POST \
    -H "Content-Type: application/json" \
    -H 'X-Goog-Api-Key: YOUR_API_KEY' \
    -d '{
      "prompt": "Create a boba app!",
      "sourceContext": {
        "source": "sources/github/bobalover/boba",
        "githubRepoContext": {
          "startingBranch": "main"
        }
      },
      "automationMode": "AUTO_CREATE_PR",
      "title": "Boba App"
    }'
```

**Step 3: List activities and interact with the agent**

To list activities in a session:

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?pageSize=30' \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

To send a message to the agent:

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:sendMessage' \
    -X POST \
    -H "Content-Type: application/json" \
    -H 'X-Goog-Api-Key: YOUR_API_KEY' \
    -d '{
      "prompt": "Can you make the app corgi themed?"
    }'
```
