# Structured Logging Schema for Agent Activity

## Overview

This document defines the mandatory JSON schema for all log entries recorded in `logs/activity.log.jsonl`. Each line in the log file MUST be a valid JSON object conforming to this schema. The purpose of this structured format is to enable automated analysis of agent behavior, performance, and decision-making for debugging, auditing, and long-term learning.

## Schema Definition

| Field               | Type          | Required | Description                                                                                                                                                             | Example                                                              |
| ------------------- | ------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `timestamp_iso8601` | String        | Yes      | An ISO 8601 formatted timestamp indicating when the event occurred (UTC).                                                                                               | `"2025-10-26T10:00:00Z"`                                             |
| `agent_id`          | String        | Yes      | A unique identifier for the agent instance or session performing the task.                                                                                              | `"jules-session-1667853600"`                                         |
| `task_id`           | String        | Yes      | A unique identifier for the overall task assigned by the user.                                                                                                          | `"task-refactor-auth-module"`                                        |
| `plan_step_id`      | Integer       | Yes      | The specific step number from the agent's generated plan, linking the action to its original intent.                                                                    | `3`                                                                  |
| `action_type`       | String (Enum) | Yes      | A standardized string representing the type of action taken. See below for the list of valid enum values.                                                               | `"TOOL_EXEC"`                                                        |
| `action_params`     | JSON Object   | Yes      | A JSON object containing the parameters for the action. The structure of this object depends on the `action_type`.                                                      | `{"tool_name": "run_in_bash_session", "command": "ls -l"}`            |
| `llm_reasoning`     | String        | No       | The LLM's brief, self-generated rationale for taking this specific action at this point in the plan.                                                                    | `"Listing files to verify the previous file creation step."`         |
| `critic_feedback`   | String        | No       | If the action was preceded by a critical review phase, this field contains the output from the critic model.                                                            | `"The plan to use 'rm -rf' is too risky. Suggest using 'mv' instead."` |
| `status`            | String (Enum) | Yes      | The outcome of the action. Must be one of: `SUCCESS`, `FAILURE`, `RETRY`.                                                                                               | `"SUCCESS"`                                                          |
| `output_summary`    | String        | No       | A brief, machine-generated summary of the action's result (e.g., hash of file contents after a write, exit code of a tool, summary of search results).                  | `{"exit_code": 0, "stdout_char_count": 256}`                          |

## `action_type` Enum Values

- `FILE_READ`: Reading the contents of a file.
  - `action_params`: `{"file_path": "path/to/file.py"}`
- `FILE_WRITE`: Writing or overwriting a file.
  - `action_params`: `{"file_path": "path/to/file.py", "content_sha256": "..."}`
- `TOOL_EXEC`: Executing a tool or command.
  - `action_params`: `{"tool_name": "...", "parameters": {...}}`
- `INTERNAL_RAG_QUERY`: Querying an internal knowledge source.
  - `action_params`: `{"source": "symbols.json", "query": "find function 'foo'"}`
- `EXTERNAL_RAG_QUERY`: Querying an external source (e.g., web search).
  - `action_params`: `{"engine": "google_search", "query": "React best practices 2025"}`
- `PLAN_GENERATION`: Generating or revising a plan.
  - `action_params`: `{"plan": "...", "revision_count": 2}`
- `MESSAGE_USER`: Sending a message to the user.
  - `action_params`: `{"message": "..."}`

## Example Log Entry (`activity.log.jsonl`)

```json
{"timestamp_iso8601": "2025-10-26T10:01:15Z", "agent_id": "jules-session-1667853600", "task_id": "task-refactor-auth-module", "plan_step_id": 4, "action_type": "FILE_WRITE", "action_params": {"file_path": "projects/react-app/src/Auth.js", "content_sha256": "a1b2c3d4..."}, "llm_reasoning": "Applying the refactoring as per the validated plan.", "critic_feedback": null, "status": "SUCCESS", "output_summary": null}
```