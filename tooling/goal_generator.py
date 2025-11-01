"""
This module provides a simple way to select a plan for the agent.
"""


def find_best_plan(task_description: str) -> str:
    """
    Returns the path to the best plan for the given task description.
    """
    if "research" in task_description.lower():
        return "plans/deep_research.txt"
    elif "test" in task_description.lower():
        return "plans/run_appl_tests.txt"
    elif "improve" in task_description.lower():
        return "plans/self_improvement_model_a.txt"
    elif "audit" in task_description.lower():
        return "plans/full_system_audit.txt"
    else:
        return "plans/code_health_supervisor.txt"
