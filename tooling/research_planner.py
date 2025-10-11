"""
Generates a structured, executable plan for conducting deep research tasks.

This script provides a standardized, FSM-compliant workflow for the agent when
it needs to perform in-depth research on a complex topic. The `plan_deep_research`
function creates a plan file that is not just a template, but a formal,
verifiable artifact that can be executed by the `master_control.py` orchestrator.

The generated plan adheres to the state transitions defined in `research_fsm.json`,
guiding the agent through the phases of GATHERING, SYNTHESIZING, and REPORTING.
"""

import sys


def plan_deep_research(topic: str) -> str:
    """
    Generates a structured, FSM-compliant executable plan for deep research.

    This function creates a plan that guides an agent through a research
    workflow. The plan is designed to be validated by `fdc_cli.py` against
    the `tooling/research_fsm.json` definition.

    Args:
        topic: The research topic to be investigated.

    Returns:
        A string containing the executable research plan.
    """
    # Sanitize the topic to create safe filenames and task IDs
    safe_topic = "".join(
        c for c in topic.replace(" ", "_") if c.isalnum() or c in ("-", "_")
    ).lower()
    report_filename = f"research_report_{safe_topic}.md"
    task_id = f"research-{safe_topic}"

    # This template creates a clean, 4-step plan that the current executor can parse.
    plan_template = f"""\
# Auto-Generated Deep Research Plan
# FSM: tooling/research_fsm.json

# 1. Set the plan, moving from IDLE to GATHERING
set_plan This is the research plan for the topic: '{topic}'.

# 2. Complete the interactive GATHERING phase, moving to SYNTHESIZING
plan_step_complete

# 3. Create the report file, moving from SYNTHESIZING to REPORTING
create_file_with_block {report_filename}

# 4. Close the task, moving from REPORTING to DONE
run_in_bash_session python3 tooling/fdc_cli.py close --task-id "{task_id}"
"""
    return plan_template.strip()


if __name__ == "__main__":
    # Example usage for testing
    if len(sys.argv) > 1:
        topic_arg = sys.argv[1]
    else:
        topic_arg = "The role of Pushdown Automata in ensuring decidability"

    print(f"--- Generating Research Plan for: '{topic_arg}' ---")
    plan = plan_deep_research(topic=topic_arg)
    print(plan)
