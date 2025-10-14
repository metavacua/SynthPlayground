"""
This module is responsible for generating a formal, FSM-compliant research plan
for a given topic. The output is a string that can be executed by the agent's
master controller.
"""
import re

def plan_deep_research(topic: str) -> str:
    """
    Generates a multi-step, FSM-compliant plan for conducting deep research.

    Args:
        topic (str): The research topic.

    Returns:
        str: A string containing the executable plan.
    """
    # Sanitize the topic to create a safe filename and task ID
    safe_topic_name = re.sub(r'[\W_]+', '_', topic.lower()).strip('_')
    report_file = f"research_report_{safe_topic_name}.md"
    task_id = f"research-{safe_topic_name}"

    plan = f"""
# FSM: tooling/research_fsm.json
# ---
# This plan outlines the process for conducting deep research on the topic:
# '{topic}'
# ---

# Step 1: Set the plan and state the goal.
set_plan This is the research plan for the topic: '{topic}'. The goal is to produce a comprehensive report.

# Step 2: Mark the planning step as complete.
plan_step_complete

# Step 3: Create a placeholder for the research report.
# The actual research and synthesis will be done by the research agent.
# For the purpose of this plan, we just create the file.
create_file_with_block {report_file}
# Research Report for {topic} - (This report will be filled in by the research agent.)

# Step 4: Close out the FDC task.
run_in_bash_session python3 tooling/fdc_cli.py close --task-id "{task_id}"
"""
    return plan.strip()
