# AGENTS.md

This file provides instructions for AI coding agents to interact with this project.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture.

## Build & Commands

This repository uses a hierarchical, decentralized protocol system. Each of the following directories contains a self-contained set of protocols and is compiled by its own local build script.
- [Browser Control](protocols/browser_control/AGENTS.md)
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

## Capabilities

This agent has the following capabilities:

*   **Document Processing:** The agent can process and understand the content of PDF documents, including text, images, and tables.
*   **Browser Control:** The agent can control a web browser to perform tasks like data entry, automated testing, and web research.

## Gemini API Integration

This section provides instructions for interacting with the Gemini API, which allows for programmatic access to the agent's capabilities.

### Authentication

To use the Gemini API, you need an API key. Pass the API key in the `x-goog-api-key` header of your API calls.

**Important:** Keep your API keys secure. Do not share them or embed them in public code.

### System Instructions

You can use system instructions to guide the behavior of the model. For example, you can use system instructions to:

*   **Define the agent's persona:** You can instruct the agent to act as a helpful and capable software engineering assistant.
*   **Specify the agent's goals:** You can specify the agent's goals for a particular task, such as "implement a new feature" or "fix a bug."
*   **Provide context:** You can provide the agent with the context it needs to understand the task at hand, such as information about the codebase, the project's architecture, and any relevant constraints or requirements.
*   **Enforce protocol adherence:** You can instruct the agent to always use the tools and information provided in the `knowledge_core/` directory.

Here's an example of how to use system instructions to define the agent's persona:

```json
{
  "system_instruction": {
    "parts": [
      {
        "text": "You are a helpful and capable software engineering assistant. Your name is Jules."
      }
    ]
  },
  "contents": [
    {
      "parts": [
        {
          "text": "Hello there"
        }
      ]
    }
  ]
}
```
