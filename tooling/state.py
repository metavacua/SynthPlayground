from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
import os
import datetime

@dataclass
class AgentState:
    """
    Represents the complete state of the agent's workflow for a single task.
    This object is initialized by the main runner and passed through the FSM.
    """
    task: str
    plan: Optional[str] = None
    current_step_index: int = 0
    messages: List[Dict[str, Any]] = field(default_factory=list)
    code_changes: List[str] = field(default_factory=list)
    validation_passed: bool = False
    initial_research_report: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    final_summary: Optional[str] = None

    def to_json(self):
        """Returns a JSON-serializable dictionary of the agent's state."""
        return {
            "task": self.task,
            "plan": self.plan,
            "current_step_index": self.current_step_index,
            "messages": self.messages,
            "code_changes": self.code_changes,
            "validation_passed": self.validation_passed,
            "initial_research_report": self.initial_research_report,
            "error": self.error,
            "final_summary": self.final_summary
        }

    def save_to_log(self, log_dir="logs"):
        """Saves the final state to a timestamped log file."""
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_task_name = "".join(c for c in self.task if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
        filename = f"{log_dir}/{timestamp}-{safe_task_name}.json"

        with open(filename, 'w') as f:
            json.dump(self.to_json(), f, indent=2)

        print(f"  - Saved final state to {filename}")