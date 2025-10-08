import os
import sys
from typing import Literal

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from research import execute_research_protocol


def plan_deep_research(
    topic: str, repository: Literal["local", "external"] = "local"
) -> str:
    """
    Generates a structured markdown template for a deep research plan.

    This function reads the relevant protocol document (local or external)
    to provide context and then generates a pre-formatted markdown plan.
    This plan provides a consistent workflow for conducting deep research.

    Args:
        topic: The research topic to be investigated.
        repository: The repository context for the research.

    Returns:
        A string containing the markdown-formatted research plan.
    """
    workflow_file_path = ""
    workflow_content_snippet = ""

    if repository == "local":
        workflow_file_path = "AGENTS.md"
        with open(workflow_file_path, "r") as f:
            workflow_content_snippet = f.read(500) + "..."
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
*   **Action:** For each core question, execute a targeted research query
    using the `execute_research_protocol` tool.
*   **Example Action for Question 1:** `execute_research_protocol(
    constraints={{"target": "external_web", "scope": "narrow", "query": "..."}})`
*   **Output:** A collection of raw findings for each question.

### Phase C: Synthesis and Refinement
*   **Action:** Review the collected findings to identify key insights,
    connections, and contradictions.
*   **Output:** A synthesized summary of the findings. Determine if any
    gaps exist that require follow-up research.

### Phase D: Final Report Generation
*   **Action:** Structure the synthesized findings into a comprehensive and
    well-organized report.
*   **Output:** The final research report, ready for review.

## 3. Protocol Reference Snippet
```
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
