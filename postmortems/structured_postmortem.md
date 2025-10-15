# Structured Post-Mortem and Lesson Generation

**Task ID:** `[TASK_ID]`
**Completion Date:** `[COMPLETION_DATE]`
**Final Status:** `[SUCCESS | FAILURE]`

---

## 1. Objective vs. Outcome Analysis

**Stated Objective:**
*A concise, one-sentence summary of the original goal.*

**Final Outcome:**
*A concise, one-sentence summary of the final result.*

**Discrepancy Analysis:**
*If there was a difference between the objective and outcome, describe it here. If not, state "No discrepancy."*

---

## 2. Causal Analysis of Failures and Inefficiencies

*This section is for identifying specific, individual causal chains that led to undesirable outcomes. For each distinct issue, create a new entry.*

### Issue 1: [Short Description of the Issue]

*   **Observation:** *What specific, observable event occurred? (e.g., "The `npm install` command failed with a peer dependency error.")*
*   **Immediate Cause:** *What was the direct technical reason for the observation? (e.g., "Package A requires version 1.x of Package B, but Package C requires version 2.x.")*
*   **Root Cause:** *Why did the immediate cause happen? Was it a knowledge gap, a process failure, or a tool limitation? (e.g., "The planning phase did not include a step to check for dependency conflicts before attempting installation.")*
*   **Log Evidence:** *Provide `log_id`s or `session_id`s from `activity.log.jsonl` that support this analysis.*

---

## 3. Generation of Structured Lessons

*Based on the root causes identified above, generate structured lessons for the `knowledge_core/lessons.jsonl` file. This is the most critical part of the process. Each lesson MUST be a single, valid JSON object.*

### Lesson 1:
```json
{
  "lesson_id": "[UUID]",
  "task_id": "[TASK_ID]",
  "date": "[YYYY-MM-DD]",
  "category": "[Process | Knowledge | Tooling]",
  "severity": "[High | Medium | Low]",
  "description": "A concise, one-sentence summary of the lesson learned. (e.g., 'Dependency conflicts should be proactively identified before running installation commands.')",
  "actionable_change": {
    "type": "[UPDATE_PROTOCOL | ADD_TOOL | MODIFY_PLAN_TEMPLATE]",
    "details": {
      "target_file": "[e.g., protocols/dependency-management.protocol.json]",
      "change_description": "A detailed description of the change to be made.",
      "proposed_content": "The new content or change to be applied by the protocol_updater.py tool."
    }
  },
  "status": "pending"
}
```

### Lesson 2:
```json
{
  "lesson_id": "[UUID]",
  "task_id": "[TASK_ID]",
  "date": "[YYYY-MM-DD]",
  "category": "[Process | Knowledge | Tooling]",
  "severity": "[High | Medium | Low]",
  "description": "...",
  "actionable_change": {
    "type": "...",
    "details": {
      "target_file": "...",
      "change_description": "...",
      "proposed_content": "..."
    }
  },
  "status": "pending"
}
```

---

## 4. General Reflections

*A section for more general, non-actionable observations or reflections that might be useful for future human or agent review.*