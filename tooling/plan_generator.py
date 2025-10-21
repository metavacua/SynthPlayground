import json
import os

AGENT_REPOSITORY_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "agent_repository.json")
)


def find_agent_that_produces(resource_name):
    """Finds an agent in the repository that produces the given resource."""
    with open(AGENT_REPOSITORY_PATH, "r") as f:
        repository = json.load(f)
    for agent_info in repository["agents"]:
        with open(agent_info["manifest_path"], "r") as f:
            manifest = json.load(f)
        for postcondition in manifest["postconditions"]:
            if postcondition["name"] == resource_name:
                return manifest
    return None


def generate_plan(goal):
    """
    Generates a plan to accomplish the given goal using backward-chaining.
    """
    plan = []

    # Find the agent that can produce the final goal.
    goal_agent = find_agent_that_produces(goal)
    if not goal_agent:
        return f"# No agent found that can produce the goal: {goal}"

    # This is a simple implementation of backward-chaining. It assumes that
    # each precondition can be satisfied by a single agent.

    sub_goals = [pre["name"] for pre in goal_agent["preconditions"]]

    while sub_goals:
        current_sub_goal = sub_goals.pop(0)

        # Find an agent that can produce the current sub-goal.
        sub_goal_agent = find_agent_that_produces(current_sub_goal)
        if not sub_goal_agent:
            return f"# No agent found that can produce the sub-goal: {current_sub_goal}"

        # Add the agent to the front of the plan.
        plan.insert(0, sub_goal_agent)

        # Add the agent's preconditions to the list of sub-goals.
        for pre in sub_goal_agent["preconditions"]:
            sub_goals.insert(0, pre["name"])

    # Add the final goal agent to the end of the plan.
    plan.append(goal_agent)

    # Construct the plan string.
    plan_string = ""
    for i, agent_manifest in enumerate(plan):
        args = []
        for pre in agent_manifest["preconditions"]:
            args.append(f"--{pre['name']} '<{pre['name']}>'")
        plan_string += f"{agent_manifest['name']} {' '.join(args)}"
        if i < len(plan) - 1:
            plan_string += "\n---\n"

    return plan_string
