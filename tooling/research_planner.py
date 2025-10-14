"""
This module is responsible for planning deep research tasks.
"""

def plan_deep_research(task_description: str) -> dict:
    """
    Generates a plan for deep research.
    For this stress test, it returns a dummy plan.
    """
    return {
        "task": task_description,
        "keywords": ["agent", "FSM", "stress test"],
        "urls": ["http://example.com/fsm", "http://example.com/agent"],
    }