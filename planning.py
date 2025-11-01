# planning.py - AAL Integration Layer

from typing import Set, List
from tooling.aal.parser import parse_aal
from tooling.aal.domain import Domain, Fluent
from tooling.aal.interpreter import Interpreter as AALInterpreter

# --- Module-level state ---
# This will hold the loaded AAL domain and the current world state.
domain: Domain = None
current_state: Set[Fluent] = set()
aal_interpreter = AALInterpreter()
# -------------------------

class PlanningError(Exception):
    pass

def load_domain(filepath: str) -> None:
    """Loads an AAL domain from a file."""
    global domain
    try:
        with open(filepath, 'r') as f:
            aal_string = f.read()
        domain = parse_aal(aal_string)
    except FileNotFoundError:
        raise PlanningError(f"AAL domain file not found: {filepath}")
    except Exception as e:
        raise PlanningError(f"Failed to parse AAL domain: {e}")

def create_state(initial_facts: List[str]) -> Set[Fluent]:
    """Initializes the current world state from a list of fluent names."""
    global current_state, domain
    if domain is None:
        raise PlanningError("Cannot create state before loading a domain.")

    # Validate that the initial facts are defined as fluents in the domain
    domain_fluent_names = {f.name for f in domain.fluents}
    for fact in initial_facts:
        if fact not in domain_fluent_names:
            raise PlanningError(f"Initial fact '{fact}' is not a declared fluent in the domain.")

    current_state = {Fluent(name=fact) for fact in initial_facts}
    return current_state

def apply_action(action_name: str) -> Set[Fluent]:
    """
    Applies an action to the current state using the AAL interpreter
    and updates the current state.
    """
    global current_state, domain
    if domain is None:
        raise PlanningError("Cannot apply action before loading a domain.")

    # Find the action object in the domain
    action_to_apply = next((a for a in domain.actions if a.name == action_name), None)
    if action_to_apply is None:
        raise PlanningError(f"Action '{action_name}' not found in the AAL domain.")

    # Use the AAL interpreter to get the next state
    next_state = aal_interpreter.get_next_state(current_state, action_to_apply, domain)

    # Update the global state
    current_state = next_state
    return current_state

def is_goal(goal_conditions: List[str]) -> bool:
    """Checks if the current state satisfies a set of goal conditions."""
    if domain is None:
        raise PlanningError("Cannot check goal before loading a domain.")

    goal_fluents = {Fluent(name=cond) for cond in goal_conditions}
    return goal_fluents.issubset(current_state)

def get_current_state() -> List[str]:
    """Returns the names of the fluents in the current state."""
    return [fluent.name for fluent in sorted(list(current_state), key=lambda f: f.name)]


class Node:
    """A node in a search tree for planning."""
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(frozenset(self.state))

    def __lt__(self, other):
        return self.f < other.f


import heapq

def calculate_heuristic(state: Set[Fluent], goal: Set[Fluent]) -> int:
    """Estimates the cost to reach the goal from the current state."""
    return len(goal.difference(state))


def find_plan(goal_conditions: List[str]) -> List[str]:
    """
    Finds a sequence of actions to achieve a goal using A* Search.
    """
    if domain is None:
        raise PlanningError("Cannot find plan before loading a domain.")

    goal_fluents = {Fluent(name=cond) for cond in goal_conditions}

    initial_h = calculate_heuristic(current_state, goal_fluents)
    initial_node = Node(current_state, g=0, h=initial_h)

    if not goal_fluents.difference(initial_node.state):
        return []  # Goal is already satisfied

    open_set = [initial_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if frozenset(current_node.state) in closed_set:
            continue

        closed_set.add(frozenset(current_node.state))

        if not goal_fluents.difference(current_node.state):
            # Goal found, reconstruct the plan
            plan = []
            while current_node.parent is not None:
                plan.insert(0, current_node.action.name)
                current_node = current_node.parent
            return plan

        for action in domain.actions:
            # Create a temporary interpreter to avoid modifying the global state
            temp_interpreter = AALInterpreter()
            next_state = temp_interpreter.get_next_state(current_node.state, action, domain)

            if frozenset(next_state) in closed_set:
                continue

            g = current_node.g + 1
            h = calculate_heuristic(next_state, goal_fluents)
            new_node = Node(next_state, parent=current_node, action=action, g=g, h=h)

            heapq.heappush(open_set, new_node)

    return None # No plan found
