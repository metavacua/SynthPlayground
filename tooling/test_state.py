import unittest
from tooling.state import AgentState, PlanContext
from tooling.plan_parser import Command


class TestState(unittest.TestCase):

    def test_agent_state_initialization(self):
        """Tests the initialization of an AgentState object."""
        state = AgentState(task="test_task")
        self.assertEqual(state.task, "test_task")
        self.assertEqual(state.plan_stack, [])
        self.assertIsNone(state.error)

    def test_plan_context_initialization(self):
        """Tests the initialization of a PlanContext object."""
        commands = [Command("set_plan", "A")]
        context = PlanContext(plan_path="test.plan", commands=commands)
        self.assertEqual(context.plan_path, "test.plan")
        self.assertEqual(context.commands, commands)
        self.assertEqual(context.current_step, 0)

    def test_agent_state_to_json(self):
        """Tests the to_json method of AgentState."""
        state = AgentState(task="test_task")
        state.plan_stack.append(
            PlanContext(plan_path="plan_a", commands=[Command("A", "B")])
        )
        state.messages.append({"role": "user", "content": "Hello"})

        json_state = state.to_dict()

        self.assertEqual(json_state["task"], "test_task")
        self.assertEqual(len(json_state["plan_stack"]), 1)
        self.assertEqual(json_state["plan_stack"][0]["plan_path"], "plan_a")
        self.assertEqual(json_state["plan_stack"][0]["current_step"], 0)
        self.assertEqual(len(json_state["plan_stack"][0]["commands"]), 1)
        self.assertEqual(json_state["plan_stack"][0]["commands"][0]["tool_name"], "A")
        self.assertEqual(len(json_state["messages"]), 1)
        self.assertEqual(json_state["messages"][0]["content"], "Hello")


if __name__ == "__main__":
    unittest.main()
