import unittest
import planning
from tooling.aal.domain import Domain, Fluent, Action, CausalLaw

class TestPlanning(unittest.TestCase):
    def setUp(self):
        # Reset the global state in the planning module for each test
        planning.domain = None
        planning.current_state = set()

    def _setup_simple_domain(self):
        """Helper to create a simple AAL domain for testing."""
        test_domain = Domain()

        # Define fluents and actions
        at_a = Fluent("at_a")
        at_b = Fluent("at_b")
        at_c = Fluent("at_c")
        move_to_b_action = Action("move_to_b")

        # Add to domain
        test_domain.fluents.update([at_a, at_b, at_c])
        test_domain.actions.add(move_to_b_action)

        # Define causal law: move_to_b causes at_b if at_a is true
        law = CausalLaw(
            action=move_to_b_action,
            effect=at_b,
            conditions=frozenset([at_a])
        )
        test_domain.causal_laws.add(law)

        planning.domain = test_domain

    def test_find_plan_simple(self):
        self._setup_simple_domain()
        planning.create_state(["at_a"])
        plan = planning.find_plan(["at_b"])
        self.assertEqual(plan, ["move_to_b"])

    def test_find_plan_goal_already_satisfied(self):
        self._setup_simple_domain()
        planning.create_state(["at_b"])
        plan = planning.find_plan(["at_b"])
        self.assertEqual(plan, [])

    def test_find_plan_no_plan_exists(self):
        self._setup_simple_domain()
        planning.create_state(["at_a"])
        plan = planning.find_plan(["at_c"])
        self.assertIsNone(plan)

    def test_find_plan_longer_plan(self):
        # Setup a domain that requires a multi-step plan
        test_domain = Domain()

        a = Fluent("a")
        b = Fluent("b")
        c = Fluent("c")

        act1 = Action("a_to_b")
        act2 = Action("b_to_c")

        test_domain.fluents.update([a, b, c])
        test_domain.actions.update([act1, act2])

        law1 = CausalLaw(action=act1, effect=b, conditions=frozenset([a]))
        law2 = CausalLaw(action=act2, effect=c, conditions=frozenset([b]))
        test_domain.causal_laws.update([law1, law2])

        planning.domain = test_domain

        planning.create_state(["a"])
        plan = planning.find_plan(["c"])
        self.assertEqual(plan, ["a_to_b", "b_to_c"])

if __name__ == '__main__':
    unittest.main()
