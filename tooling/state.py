import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PlanContext:
    """Represents the execution context of a single plan file."""

    plan_path: str
    plan_content: List[str]
    current_step: int = 0


@dataclass
class AgentState:
    """
    Represents the complete state of the agent's workflow at any given time.
    This object is passed between nodes in the master control graph.
    """

    task: str
    # The plan_stack replaces the old flat plan. The top of the stack is the
    # currently executing plan.
    plan_stack: List[PlanContext] = field(default_factory=list)
    messages: List[Dict[str, Any]] = field(default_factory=list)

    # Orientation Status
    orientation_complete: bool = False
    vm_capability_report: Optional[str] = None

    # Research & Execution
    research_findings: Dict[str, Any] = field(default_factory=dict)
    draft_postmortem_path: Optional[str] = None

    # Final Output
    final_report: Optional[str] = None

    # Meta
    error: Optional[str] = None

    def to_json(self):
        return {
            "task": self.task,
            "plan_stack": [
                {
                    "plan_path": ctx.plan_path,
                    "current_step": ctx.current_step,
                    "plan_length": len(ctx.plan_content),
                }
                for ctx in self.plan_stack
            ],
            "messages": self.messages,
            "orientation_complete": self.orientation_complete,
            "vm_capability_report": self.vm_capability_report,
            "research_findings": self.research_findings,
            "draft_postmortem_path": self.draft_postmortem_path,
            "final_report": self.final_report,
            "error": self.error,
        }