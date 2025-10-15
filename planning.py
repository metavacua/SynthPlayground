class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

    def __repr__(self):
        return f"Action({self.name}, {self.preconditions}, {self.effects})"

class Goal:
    def __init__(self, name, conditions):
        self.name = name
        self.conditions = conditions

    def __repr__(self):
        return f"Goal({self.name}, {self.conditions})"

class State:
    def __init__(self, facts):
        self.facts = facts

    def __repr__(self):
        return f"State({self.facts})"

def create_action(name, preconditions, effects):
    return Action(name, preconditions, effects)

def create_goal(name, conditions):
    return Goal(name, conditions)

def create_state(facts):
    return State(set(facts))

def apply_action(state, action):
    if set(action.preconditions).issubset(state.facts):
        new_facts = state.facts.copy()
        for effect in action.effects:
            if effect.startswith("not "):
                fact = effect[4:]
                if fact in new_facts:
                    new_facts.remove(fact)
            else:
                new_facts.add(effect)
        return State(new_facts)
    return None

def is_goal(state, goal):
    return set(goal.conditions).issubset(state.facts)