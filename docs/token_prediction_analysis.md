# Token Prediction Analysis

This document analyzes the process of token prediction in Large Language Models (LLMs) and defines it in the context of this agent's operation.

## LLM Token Prediction

Based on research, LLM token prediction is a two-stage process:

1.  **Prediction:** The LLM takes a sequence of tokens as input and generates a probability distribution over its entire vocabulary for the next token. This distribution represents the model's "prediction" of the most likely next token.

2.  **Decoding:** A decoding strategy is then used to select a single token from this probability distribution. Common decoding strategies include:
    *   **Greedy Search:** Always selecting the token with the highest probability.
    *   **Beam Search:** Exploring multiple high-probability sequences.
    *   **Top-k Sampling:** Sampling from the top `k` most probable tokens.
    *   **Top-p (Nucleus) Sampling:** Sampling from the smallest set of tokens whose cumulative probability exceeds a threshold `p`.
    *   **Temperature Sampling:** Adjusting the "sharpness" of the probability distribution to control randomness.

## Token Prediction in the Context of this Agent

For this agent, "token prediction" is not about generating natural language, but about choosing the next action to take. Each action is a "token" in the agent's "language," and the agent's "token prediction" is its decision-making process.

Therefore, testing the agent's token prediction is equivalent to testing its ability to choose the correct tool and arguments based on the current context. A "correct" choice is one that is logical, efficient, and adheres to the repository's established protocols.

This analysis forms the basis for the new "Decision-Making Test Protocol," which will be used to create a suite of tests to verify the agent's core decision-making capabilities.

## Decision-Making Test Protocol

Decision-making tests are defined in YAML files located in the `decision_tests/` directory. Each file can contain one or more tests. The following structure must be used:

```yaml
- id: DMT-001
  scenario: A description of a situation or a user request.
  context:
    - type: file
      path: path/to/file.txt
      content: |
        File content.
    - type: command_output
      command: "ls -l"
      output: |
        -rw-r--r-- 1 user group 123 Oct 29 23:09 file.txt
  expected_action:
    tool: tool_name
    args:
      arg1: value1
      arg2: value2
```

### Fields

*   `id`: A unique identifier for the test (e.g., `DMT-001`).
*   `scenario`: A description of a situation or a user request that the agent must respond to.
*   `context`: A list of contextual elements that the agent must consider.
    *   `type`: The type of context, either `file` or `command_output`.
    *   `path`: For `file` context, the path to the file.
    *   `content`: For `file` context, the content of the file.
    *   `command`: For `command_output` context, the command that was run.
    *   `output`: For `command_output` context, the output of the command.
*   `expected_action`: The single, most logical tool call the agent should make in response to the scenario and context.
    *   `tool`: The name of the tool to be called.
    *   `args`: A dictionary of arguments to be passed to the tool.
