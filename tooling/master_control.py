import json
import sys
import time
import os

# Add tooling directory to path to import other tools
sys.path.insert(0, './tooling')
from state import AgentState
from research import execute_research_protocol

class MasterControlGraph:
    """
    A Finite State Machine (FSM) that enforces the agent's protocol.
    This graph reads a state definition and orchestrates the agent's workflow,
    ensuring that all protocol steps are followed in the correct order.
    """
    def __init__(self, fsm_path: str = "tooling/fsm.json"):
        with open(fsm_path, 'r') as f:
            self.fsm = json.load(f)
        self.current_state = self.fsm["initial_state"]

    def get_trigger(self, source_state: str, dest_state: str) -> str:
        """Finds the trigger for a transition between two states."""
        for transition in self.fsm["transitions"]:
            if transition["source"] == source_state and transition["dest"] == dest_state:
                return transition["trigger"]
        raise ValueError(f"No trigger found for transition from {source_state} to {dest_state}")

    def do_orientation(self, agent_state: AgentState) -> str:
        """Executes the L1, L2, and L3 orientation steps."""
        print("[MasterControl] State: ORIENTING")
        try:
            # L1: Self-Awareness
            print("  - Executing L1: Self-Awareness...")
            l1_constraints = {"target": "local_filesystem", "scope": "file", "path": "knowledge_core/agent_meta.json"}
            agent_meta = execute_research_protocol(l1_constraints)
            agent_state.messages.append({"role": "system", "content": f"L1 Orientation Complete. Agent Meta: {agent_meta[:100]}..."})

            # L2: Repo Sync
            print("  - Executing L2: Repository Sync...")
            l2_constraints = {"target": "local_filesystem", "scope": "directory", "path": "knowledge_core/"}
            repo_state = execute_research_protocol(l2_constraints)
            agent_state.messages.append({"role": "system", "content": f"L2 Orientation Complete. Repo State: {repo_state[:100]}..."})

            # L3: Environmental Probe
            print("  - Executing L3: Environmental Probe...")
            # This would call the environmental_probe.py script in a real scenario
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
        """
        Waits for the agent to provide a plan via a file.

        This node will poll the filesystem for a `plan.txt` file. Once the
        file is detected, it reads the plan, updates the agent's state,
        deletes the file, and transitions to the next state.
        """
        print("[MasterControl] State: PLANNING")
        plan_file = "plan.txt"

        # Wait for the agent to create the plan file
        print(f"  - Waiting for agent to create '{plan_file}'...")
        while not os.path.exists(plan_file):
            time.sleep(1) # Poll every second

        print(f"  - Detected '{plan_file}'. Reading plan...")
        with open(plan_file, 'r') as f:
            plan = f.read()

        agent_state.plan = plan
        agent_state.messages.append({"role": "system", "content": f"Plan has been set from {plan_file}."})
        print("[MasterControl] Planning Complete.")

        # Clean up the plan file
        os.remove(plan_file)
        print(f"  - Cleaned up '{plan_file}'.")

        return self.get_trigger("PLANNING", "EXECUTING")

    def do_execution(self, agent_state: AgentState) -> str:
        """Simulates the execution of the plan."""
        print("[MasterControl] State: EXECUTING")
        # Simulate executing each step of the plan
        plan_steps = agent_state.plan.split('\n')
        if agent_state.current_step_index < len(plan_steps):
            step = plan_steps[agent_state.current_step_index]
            print(f"  - Executing: {step}")
            agent_state.messages.append({"role": "system", "content": f"Completed step: {step}"})
            agent_state.current_step_index += 1
            time.sleep(0.1) # Simulate work
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

    def run(self, initial_agent_state: AgentState):
        """Runs the agent's workflow through the FSM."""
        agent_state = initial_agent_state

        while self.current_state not in self.fsm["final_states"]:
            if self.current_state == "START":
                self.current_state = "ORIENTING"
                continue

            if self.current_state == "ORIENTING":
                trigger = self.do_orientation(agent_state)
            elif self.current_state == "PLANNING":
                trigger = self.do_planning(agent_state)
            elif self.current_state == "EXECUTING":
                trigger = self.do_execution(agent_state)
            elif self.current_state == "POST_MORTEM":
                trigger = self.do_post_mortem(agent_state)
            else:
                agent_state.error = f"Unknown state: {self.current_state}"
                self.current_state = "ERROR"
                break

            # Find the next state based on the trigger
            found_transition = False
            for transition in self.fsm["transitions"]:
                if transition["source"] == self.current_state and transition["trigger"] == trigger:
                    self.current_state = transition["dest"]
                    found_transition = True
                    break

            if not found_transition:
                agent_state.error = f"No transition found for state {self.current_state} with trigger {trigger}"
                self.current_state = "ERROR"

        print(f"[MasterControl] Workflow finished in state: {self.current_state}")
        if agent_state.error:
            print(f"  - Error: {agent_state.error}")
        return agent_state

if __name__ == '__main__':
    print("--- Initializing Master Control Graph Demonstration ---")
    # 1. Initialize the agent's state for a new task
    task = "Demonstrate the self-enforcing protocol."
    initial_state = AgentState(task=task)

    # 2. Initialize and run the master control graph
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 3. Print the final report
    print("\n--- Final State ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print("--- Demonstration Complete ---")