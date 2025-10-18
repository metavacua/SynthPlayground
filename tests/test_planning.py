import unittest
from planning import *

class TestPlanning(unittest.TestCase):
    def test_create_action(self):
        action = create_action("move", ["at A"], ["at B", "not at A"])
        self.assertIsInstance(action, Action)
        self.assertEqual(action.name, "move")
        self.assertEqual(action.preconditions, ["at A"])
        self.assertEqual(action.effects, ["at B", "not at A"])

    def test_create_goal(self):
        goal = create_goal("at B", ["at B"])
        self.assertIsInstance(goal, Goal)
        self.assertEqual(goal.name, "at B")
        self.assertEqual(goal.conditions, ["at B"])

    def test_create_state(self):
        state = create_state(["at A", "at C"])
        self.assertIsInstance(state, State)
        self.assertEqual(state.facts, {"at A", "at C"})

    def test_apply_action_success(self):
        state = create_state(["at A", "at C"])
        action = create_action("move", ["at A"], ["at B", "not at A"])
        new_state = apply_action(state, action)
        self.assertIsNotNone(new_state)
        self.assertEqual(new_state.facts, {"at B", "at C"})

    def test_apply_action_fail(self):
        state = create_state(["at C"])
        action = create_action("move", ["at A"], ["at B", "not at A"])
        new_state = apply_action(state, action)
        self.assertIsNone(new_state)

    def test_is_goal_success(self):
        state = create_state(["at B", "at C"])
        goal = create_goal("at B", ["at B"])
        self.assertTrue(is_goal(state, goal))

    def test_is_goal_fail(self):
        state = create_state(["at C"])
        goal = create_goal("at B", ["at B"])
        self.assertFalse(is_goal(state, goal))

if __name__ == '__main__':
    unittest.main()