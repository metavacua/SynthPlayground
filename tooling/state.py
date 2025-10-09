import json
from typing import List, Dict, Any

class AgentState:
    """
    A class to represent and manage the agent's state throughout its lifecycle.
    """

    def __init__(self, task: str):
        """
        Initializes the agent's state for a new task.

        Args:
            task (str): The high-level description of the task to be performed.
        """
        self.task: str = task
        self.plan: str = ""
        self.messages: List[Dict[str, Any]] = [{"role": "user", "content": task}]
        self.orientation_complete: bool = False
        self.current_step_index: int = 0
        self.error: str = None
        self.draft_postmortem_path: str = ""
        self.final_report: str = ""
        self.vm_capability_report: str = ""

    def to_json(self, indent: int = 2) -> str:
        """
        Serializes the agent's state to a JSON string.

        Args:
            indent (int): The indentation level for the JSON output.

        Returns:
            str: A JSON string representation of the agent's state.
        """
        return json.dumps(
            {
                "task": self.task,
                "plan": self.plan,
                "messages": self.messages,
                "orientation_complete": self.orientation_complete,
                "current_step_index": self.current_step_index,
                "error": self.error,
                "draft_postmortem_path": self.draft_postmortem_path,
                "final_report": self.final_report,
                "vm_capability_report": self.vm_capability_report,
            },
            indent=indent,
        )

    def __repr__(self) -> str:
        return f"AgentState(task='{self.task}', current_step={self.current_step_index}, error='{self.error}')"