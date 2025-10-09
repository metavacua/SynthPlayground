import json
import sys
from typing import Literal

# Ensure the tooling directory is in the path to import the research tool
sys.path.insert(0, "./tooling")
from research import execute_research_protocol


def plan_deep_research(
    topic: str, repository: Literal["local", "external"] = "local"
) -> str:
    """
    Generates a structured markdown template for a deep research plan.

    This function reads the relevant protocol document (either local or external)
    to provide context and then generates a pre-formatted markdown plan. This
    plan provides a consistent workflow for conducting deep research.

    Args:
        topic: The research topic to be investigated.
        repository: The repository context for the research ('local' or 'external').

    Returns:
        A string containing the markdown-formatted research plan.
    """
    workflow_file_path = ""
    workflow_content_snippet = ""

    if repository == "local":
        workflow_file_path = "AGENTS.md"
        try:
            with open(workflow_file_path, "r") as f:
                content = f.read()
            # Extract content from the json code block
            start_marker = "```json\n"
            end_marker = "\n```"
            start_index = content.find(start_marker) + len(start_marker)
            end_index = content.rfind(end_marker)

            if start_index != -1 and end_index != -1:
                json_content = content[start_index:end_index]
                data = json.loads(json_content)
                # Pretty-print the JSON content for readability
                json_string = json.dumps(data, indent=2)
                workflow_content_snippet = json_string[:500] + "..."
            else:
                workflow_content_snippet = "Error: Could not find JSON block in AGENTS.md"
        except (FileNotFoundError, json.JSONDecodeError):
            workflow_content_snippet = "Error: Could not read or parse AGENTS.md"
    elif repository == "external":
        workflow_file_path = "src/open_deep_research/deep_researcher.py"
        constraints = {"target": "external_repository", "path": workflow_file_path}
        content = execute_research_protocol(constraints)
        workflow_content_snippet = content[:500] + "..."
    else:
        return "Error: Invalid repository specified. Must be 'local' or 'external'."

    plan_template = f"""
# Deep Research Plan

## 1. Research Context
- **Topic:** {topic}
- **Repository Context:** {repository}
- **Governing Protocol:** `{workflow_file_path}`

## 2. Research Phases

### Phase A: Initial Planning & Question Formulation
*   **Action:** Analyze the topic to break it down into fundamental questions.
*   **Output:** A list of 3-5 core research questions.
    -   *Question 1:*
    -   *Question 2:*
    -   *Question 3:*

### Phase B: Parallel Research Execution
*   **Action:** For each core question, execute a targeted research query using the `execute_research_protocol` tool.
*   **Example Action for Question 1:** `execute_research_protocol(constraints={{"target": "external_web", "scope": "narrow", "query": "..."}})`
*   **Output:** A collection of raw findings for each question.

### Phase C: Synthesis and Refinement
*   **Action:** Review the collected findings to identify key insights, connections, and contradictions.
*   **Output:** A synthesized summary of the findings. Determine if any gaps exist that require follow-up research.

### Phase D: Final Report Generation
*   **Action:** Structure the synthesized findings into a comprehensive and well-organized report.
*   **Output:** The final research report, ready for review.

## 3. Protocol Reference Snippet
```json
{workflow_content_snippet}
```
"""
    return plan_template.strip()


if __name__ == "__main__":
    # Example usage for testing
    print("--- Generating Local Research Plan ---")
    local_plan = plan_deep_research(
        "Understand the agent's own protocol", repository="local"
    )
    print(local_plan)

    print("\n" + "=" * 50 + "\n")

    print("--- Generating External Research Plan ---")
    external_plan = plan_deep_research(
        "Understand the external deep research toolchain", repository="external"
    )
    print(external_plan)
