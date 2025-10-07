import json
import sys
import time

# Add tooling directory to path to import other tools
sys.path.insert(0, './tooling')
from state import AgentState
from research import execute_research_protocol

class MasterControlGraph:
    """
    A Finite State Machine (FSM) that enforces the agent's protocol.
    This graph is designed to be driven by an external loop, executing one
    step at a time to allow for interactive and resource-bounded operation.
    """
    def __init__(self, fsm_path: str = "tooling/fsm.json", max_tool_calls: int = 20, max_tokens: int = 50000):
        with open(fsm_path, 'r') as f:
            self.fsm = json.load(f)
        self.max_tool_calls = max_tool_calls
        self.max_tokens = max_tokens

    def get_trigger(self, source_state: str, dest_state: str) -> str:
        """Finds the trigger for a transition between two states."""
        for transition in self.fsm["transitions"]:
            if transition["source"] == source_state and transition["dest"] == dest_state:
                return transition["trigger"]
        raise ValueError(f"No trigger found for transition from {source_state} to {dest_state}")

    def _check_resources(self, agent_state: AgentState) -> bool:
        """Checks if resource limits have been exceeded."""
        if agent_state.cumulative_tool_calls >= self.max_tool_calls:
            agent_state.error = f"Resource limit exceeded: Tool calls ({agent_state.cumulative_tool_calls}) >= {self.max_tool_calls}"
            return False
        if agent_state.cumulative_tokens >= self.max_tokens:
            agent_state.error = f"Resource limit exceeded: Tokens ({agent_state.cumulative_tokens}) >= {self.max_tokens}"
            return False
        return True

    def do_orientation(self, agent_state: AgentState) -> str:
        """Executes the L1, L2, and L3 orientation steps."""
        print("[MasterControl] State: ORIENTING")
        try:
            # L1: Self-Awareness
            l1_constraints = {"target": "local_filesystem", "scope": "file", "path": "knowledge_core/agent_meta.json"}
            agent_meta = execute_research_protocol(l1_constraints)
            agent_state.messages.append({"role": "system", "content": f"L1 Orientation Complete. Agent Meta: {agent_meta[:100]}..."})
            agent_state.cumulative_tool_calls += 1
            agent_state.cumulative_tokens += len(agent_meta) # Mock token counting

            # L2: Repo Sync
            l2_constraints = {"target": "local_filesystem", "scope": "directory", "path": "knowledge_core/"}
            repo_state = execute_research_protocol(l2_constraints)
            agent_state.messages.append({"role": "system", "content": f"L2 Orientation Complete. Repo State: {repo_state[:100]}..."})
            agent_state.cumulative_tool_calls += 1
            agent_state.cumulative_tokens += len(repo_state)

            # L3: Environmental Probe
            agent_state.vm_capability_report = "Mock VM Capability Report: Filesystem OK, Network OK."
            agent_state.messages.append({"role": "system", "content": "L3 Orientation Complete."})

            agent_state.orientation_complete = True
            print("[MasterControl] Orientation Succeeded.")
            return self.get_trigger("ORIENTING", "PLANNING")
        except Exception as e:
            agent_state.error = f"Orientation failed: {e}"
            print(f"[MasterControl] Orientation Failed: {e}")
            return self.get_trigger("ORIENTING", "ERROR")

    def do_planning(self, agent_state: AgentState) -> str:
        """Simulates the planning phase."""
        print("[MasterControl] State: PLANNING")
        if not agent_state.plan:
            agent_state.plan = "1. *Step 1:* Do the first thing.\n2. *Step 2:* Do the second thing."
            agent_state.messages.append({"role": "system", "content": "Plan has been set."})
        print("[MasterControl] Planning Complete.")
        return self.get_trigger("PLANNING", "EXECUTING")

    def do_execution(self, agent_state: AgentState) -> str:
        """Simulates the execution of one step of the plan."""
        print("[MasterControl] State: EXECUTING")
        plan_steps = agent_state.plan.split('\n')
        if agent_state.current_step_index < len(plan_steps):
            step = plan_steps[agent_state.current_step_index]
            print(f"  - Executing: {step}")
            agent_state.messages.append({"role": "system", "content": f"Completed step: {step}"})
            agent_state.current_step_index += 1
            agent_state.cumulative_tool_calls += 1 # Each step is a "tool call"
            agent_state.cumulative_tokens += 100 # Mock token cost per step
            return self.get_trigger("EXECUTING", "EXECUTING")
        else:
            print("[MasterControl] Execution Complete.")
            return self.get_trigger("EXECUTING", "POST_MORTEM")

    def do_post_mortem(self, agent_state: AgentState) -> str:
        """Simulates the post-mortem phase."""
        print("[MasterControl] State: POST_MORTEM")
        agent_state.final_report = f"Final report for task: {agent_state.task}. All steps completed successfully."
        print("[MasterControl] Post-Mortem Complete.")
        return self.get_trigger("POST_MORTEM", "DONE")

    def step(self, agent_state: AgentState) -> AgentState:
        """Executes a single step of the FSM based on the current state."""
        current_state = agent_state.current_state

        if current_state in self.fsm["final_states"]:
            print(f"[MasterControl] Workflow is already in a final state: {current_state}")
            return agent_state

        if not self._check_resources(agent_state):
            print(f"[MasterControl] Resource limit exceeded. Halting workflow.")
            agent_state.current_state = "ERROR"
            return agent_state

        if current_state == "START":
            agent_state.current_state = "ORIENTING"
            return agent_state

        if current_state == "ORIENTING":
            trigger = self.do_orientation(agent_state)
        elif current_state == "PLANNING":
            trigger = self.do_planning(agent_state)
        elif current_state == "EXECUTING":
            trigger = self.do_execution(agent_state)
        elif current_state == "POST_MORTEM":
            trigger = self.do_post_mortem(agent_state)
        else:
            agent_state.error = f"Unknown state: {current_state}"
            agent_state.current_state = "ERROR"
            return agent_state

        # Find the next state based on the trigger
        found_transition = False
        for transition in self.fsm["transitions"]:
            if transition["source"] == current_state and transition["trigger"] == trigger:
                agent_state.current_state = transition["dest"]
                found_transition = True
                break

        if not found_transition:
            agent_state.error = f"No transition found for state {current_state} with trigger {trigger}"
            agent_state.current_state = "ERROR"

        return agent_state

if __name__ == '__main__':
    print("--- Initializing Step-Wise Master Control Graph Demonstration ---")
    # 1. Initialize the agent's state for a new task
    task = "Demonstrate the interactive, step-wise protocol."
    state = AgentState(task=task)

    # 2. Initialize the master control graph
    graph = MasterControlGraph()

    # 3. Drive the graph with an external loop
    while state.current_state not in graph.fsm["final_states"]:
        print(f"\n--- External Loop: Current State is '{state.current_state}' ---")
        state = graph.step(state)
        time.sleep(0.2) # Simulate agent thinking/acting

    # 4. Print the final report
    print(f"\n--- Task Complete ---")
    print(f"Final State: {state.current_state}")
    if state.error:
        print(f"Error: {state.error}")
    else:
        print("\n--- Final Report ---")
        print(state.final_report)

    print("\n--- Full State Log ---")
    print(json.dumps(state.to_json(), indent=2))
    print("--- Demonstration Complete ---")