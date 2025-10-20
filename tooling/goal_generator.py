"""
This module is responsible for the logic of selecting a goal.
"""

import os
from typing import List

def find_best_plan(natural_language_objective: str) -> str:
    """
    Finds the best plan to execute based on a natural language objective.

    Args:
        natural_language_objective: The user's objective in natural language.

    Returns:
        The path to the best plan file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plans_dir = os.path.join(script_dir, "..", "plans")
    available_plans = [f for f in os.listdir(plans_dir) if f.endswith(".txt")]

    # Basic keyword matching heuristic.
    keywords = natural_language_objective.lower().split()
    best_plan = None
    max_score = 0

    for plan in available_plans:
        score = 0
        with open(os.path.join(plans_dir, plan), "r") as f:
            content = f.read().lower()
            for keyword in keywords:
                if keyword in content:
                    score += 1
        if score > max_score:
            max_score = score
            best_plan = plan

    if best_plan:
        return os.path.join(plans_dir, best_plan)
    else:
        # Default to a safe plan if no match is found.
        return os.path.join(plans_dir, "code_health_supervisor.txt")
