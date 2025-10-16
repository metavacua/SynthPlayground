# Structured Activity Log Schema v1.2

This document defines the JSON schema for entries in `logs/activity.log.jsonl`. Each line in the log file is a JSON object that must conform to this schema. The goal of this schema is to provide a rich, structured dataset for post-mortem analysis, proactive task generation, and deep debugging of the agent's reasoning process.

## Schema Definition

```json
{
  "type": "object",
  "properties": {
    "log_id": {
      "type": "string",
      "format": "uuid",
      "description": "A unique identifier for this specific log entry."
    },
    "session_id": {
      "type": "string",
      "description": "A unique identifier for the entire work session. Allows grouping of all logs for a single session."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "The ISO 8601 timestamp of the event."
    },
    "phase": {
      "type": "string",
      "enum": ["Phase 0", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6", "Phase 7", "Phase 8"],
      "description": "The protocol phase in which the action occurred."
    },
    "task": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "A unique identifier for the current task."
        },
        "plan_step": {
          "type": "integer",
          "description": "The specific step number in the plan that this action corresponds to."
        }
      },
      "required": ["id", "plan_step"]
    },
    "action": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "TASK_START",
            "FILE_READ",
            "FILE_WRITE",
            "TOOL_EXEC",
            "EXTERNAL_RAG_QUERY",
            "PLAN_UPDATE",
            "CRITIC_FEEDBACK",
            "POST_MORTEM",
            "TASK_END",
            "INFO",
              "SYSTEM_FAILURE",
              "RESEARCH_REPORT"
          ],
          "description": "The type of action being logged."
        },
        "details": {
          "type": "object",
          "description": "A flexible object containing details specific to the action type. See 'Action Details Examples' for best practices."
        }
      },
      "required": ["type", "details"]
    },
    "outcome": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["SUCCESS", "FAILURE", "IN_PROGRESS"],
          "description": "The outcome of the action."
        },
        "message": {
          "type": "string",
          "description": "A human-readable message describing the outcome."
        },
        "error": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "stack_trace": {"type": "string"}
            },
            "description": "Structured error information, present only on FAILURE."
        }
      },
      "required": ["status"]
    },
    "evidence_citation": {
      "type": "string",
      "description": "A citation to the source (e.g., external documentation, internal artifact) that justifies the action, as per protocol."
    },
    "context": {
      "type": "object",
      "description": "Captures the agent's internal state and reasoning at the time of the action. This is crucial for debugging and understanding the 'why' behind an action.",
      "properties": {
        "current_thought": {
          "type": "string",
          "description": "A brief, natural-language description of the agent's immediate thought process or hypothesis being tested by the action."
        },
        "active_memory_summary": {
          "type": "string",
          "description": "A summary of the key information the agent is currently holding in its active memory or scratchpad."
        },
        "plan_execution_stack": {
          "type": "array",
          "items": { "type": "string" },
          "description": "An array representing the current plan execution stack, showing the hierarchy of active plans (e.g., ['main_plan.txt', 'sub_plan_a.txt'])."
        }
      }
    }
  },
  "required": ["log_id", "session_id", "timestamp", "phase", "task", "action", "outcome"]
}
```

## Action Details Examples

- **TASK_START**: `{"origin": "user" | "proactive", "description": "High-level task description.", "justification": "Analysis that led to this proactive task."}`
- **FILE_WRITE**: `{"path": "/path/to/file.md", "content_hash": "sha256_hash_of_content"}`
- **TOOL_EXEC**: `{"command": "ls -l", "stdout": "...", "stderr": "..."}`
- **EXTERNAL_RAG_QUERY**: `{"query": "React best practices 2025", "results_summary": "Top 3 results summarized..."}`
- **POST_MORTEM**: `{"summary": "What worked, what failed, root cause analysis."}`
- **TASK_END**: `{"summary": "Signals the formal end of the development phase of a Finite Development Cycle, post-mortem complete."}`
- **INFO**: `{"summary": "An informational message or observation."}`
- **SYSTEM_FAILURE**: `{"error_message": "...", "stack_trace": "..."}`

## Example Entry

```json
{"log_id":"...","session_id":"...","timestamp":"2025-10-05T18:00:00Z","phase":"Phase 2","task":{"id":"improve-logging-01","plan_step":1},"action":{"type":"FILE_WRITE","details":{"path":"LOGGING_SCHEMA.md","content_hash":"..."}},"outcome":{"status":"SUCCESS","message":"Updated logging schema to v1.2 to include context field."},"evidence_citation":"AGENTS.md, meta-protocol-001","context":{"current_thought":"The existing logging schema lacks fields to capture the agent's internal state. Adding a 'context' object will provide deeper insight for post-mortem analysis.","active_memory_summary":"User requested improvements to logging. Current file is LOGGING_SCHEMA.md. Plan is to add a 'context' field with 'current_thought' and 'plan_execution_stack'.","plan_execution_stack":["improve-agent-processes.txt"]}}
```