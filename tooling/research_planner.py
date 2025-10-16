"""
This module is responsible for generating a formal, FSM-compliant research plan
for a given topic. The output is a string that can be executed by the agent's
master controller.
"""

import re


def plan_deep_research(topic: str, research_id: str) -> str:
    """
    Generates a multi-step, FSM-compliant plan for conducting deep research
    using the official project templates.

    Args:
        topic (str): The research topic.
        research_id (str): A unique ID for this research task.

    Returns:
        str: A string containing the executable plan.
    """
    plan_file = f"research/research_plan_{research_id}.md"
    report_file = f"research/research_report_{research_id}.md"

    # 1. Load the plan template
    with open("research/research_plan.md", "r") as f:
        plan_template = f.read()

    # 2. Populate the plan template
    plan_content = plan_template.replace("[Topic]", topic)
    plan_content = plan_content.replace("[RESEARCH_ID]", research_id)
    plan_content = plan_content.replace(
        "A clear, one-sentence statement of what this research aims to achieve.",
        f"To produce a comprehensive research report on the topic of '{topic}'.",
    )

    # 3. Load the report template
    with open("research/research_report_template.md", "r") as f:
        report_template = f.read()

    # 4. Populate the report template
    report_content = report_template.replace("[Topic]", topic)
    report_content = report_content.replace("[RESEARCH_ID]", research_id)

    plan = f"""
# FSM: tooling/research_fsm.json
# ---
# This plan outlines the process for conducting deep research on the topic:
# '{topic}' using Research ID: {research_id}
# ---

# Step 1: Set the overall plan for the user.
set_plan This is the research plan for '{topic}'. I will first create the formal plan and report documents, then proceed with the research.

# Step 2: Create the formal research plan document.
create_file_with_block {plan_file}
{plan_content}

# Step 3: Create the placeholder research report document.
create_file_with_block {report_file}
{report_content}

# Step 4: Inform the user that the setup is complete and research is starting.
message_user The research plan and report structure for '{topic}' have been created. I am now proceeding with the information gathering phase.

# Step 5: Mark the planning step as complete.
plan_step_complete

# Step 6: (This is where the agent would begin executing the actual research steps,
# like using google_search, reading files, etc. This plan only covers the setup.)

# Step 7: Submit the generated research documents.
submit
"""
    return plan.strip()
