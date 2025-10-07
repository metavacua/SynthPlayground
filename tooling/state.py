from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AgentState:
    """
    Represents the complete state of the agent's workflow at any given time.
    This object is passed between nodes in the master control graph.
    """
    task: str
    plan: Optional[str] = None
    messages: List[Dict[str, Any]] = field(default_factory=list)

    # Orientation Status
    orientation_complete: bool = False
    vm_capability_report: Optional[str] = None

    # Research & Execution
    current_step_index: int = 0
    research_findings: Dict[str, Any] = field(default_factory=dict)

    # Final Output
    final_report: Optional[str] = None

    # Meta
    error: Optional[str] = None

    def to_json(self):
        return {
            "task": self.task,
            "plan": self.plan,
            "messages": self.messages,
            "orientation_complete": self.orientation_complete,
            "vm_capability_report": self.vm_capability_report,
            "current_step_index": self.current_step_index,
            "research_findings": self.research_findings,
            "final_report": self.final_report,
            "error": self.error,
        }