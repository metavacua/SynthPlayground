# Structured Activity Log Schema

This document defines the JSON schema for entries in `logs/activity.log.jsonl`. Each line in the log file is a JSON object that must conform to this schema.

## Schema Definition

```json
{
  "type": "object",
  "properties": {
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "The ISO 8601 timestamp of the event."
    },
    "task_id": {
      "type": "string",
      "description": "A unique identifier for the current task."
    },
    "action": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "FILE_READ",
            "FILE_WRITE",
            "TOOL_EXEC",
            "EXTERNAL_RAG_QUERY",
            "PLAN_UPDATE",
            "CRITIC_FEEDBACK"
          ],
          "description": "The type of action being logged."
        },
        "details": {
          "type": "object",
          "description": "A flexible object containing details specific to the action type."
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
        }
      },
      "required": ["status"]
    },
    "evidence_citation": {
      "type": "string",
      "description": "A citation to the source (e.g., external documentation, internal artifact) that justifies the action, as per protocol."
    }
  },
  "required": ["timestamp", "task_id", "action", "outcome"]
}
```

## Example Entry

```json
{"timestamp":"2025-10-05T14:40:07Z","task_id":"bootstrap-repository-01","action":{"type":"FILE_WRITE","details":{"path":"LOGGING_SCHEMA.md","content_hash":"..."}},"outcome":{"status":"SUCCESS","message":"Created the logging schema file."},"evidence_citation":"Agent.md, Phase 5: Execution & Structured Logging"}
```