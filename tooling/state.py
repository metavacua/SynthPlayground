"""
Defines the core data structures for managing the agent's state.

This module provides the `AgentState` and `PlanContext` dataclasses, which are
fundamental to the operation of the Context-Free Development Cycle (CFDC). These
structures allow the `master_control.py` orchestrator to maintain a complete,
snapshot-able representation of the agent's progress through a task.

- `AgentState`: The primary container for all information related to the current
  task, including the plan execution stack, message history, and error states.
- `PlanContext`: A specific structure that holds the state of a single plan
  file, including its content and the current execution step. This is the
  element that gets pushed onto the `plan_stack` in `AgentState`.

Together, these classes enable the hierarchical, stack-based planning and
execution that is the hallmark of the CFDC.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# The Command dataclass is now defined in the central plan_parser module.
from tooling.plan_parser import Command


@dataclass
class PlanContext:
    """
    Represents the execution context of a single plan file within the plan stack.

    This class holds the state of a specific plan being executed, including its
    file path, its content (as a list of parsed Command objects), and a pointer
    to the current step being executed.
    """

    plan_path: str
    commands: List[Command]
    current_step: int = 0
    plan_content: List[str] = field(default_factory=list)


@dataclass
class AgentState:
    """
    Represents the complete, serializable state of the agent's workflow.

    This dataclass acts as a central container for all information related to the
    agent's current task. It is designed to be passed between the different states
    of the `MasterControlGraph` FSM, ensuring that context is maintained
    throughout the lifecycle of a task.

    Attributes:
        task: A string describing the overall objective.
        plan_path: The file path to the root plan for the current task.
        plan_stack: A list of `PlanContext` objects, forming the execution
            stack for the CFDC. The plan at the top of the stack is the one
            currently being executed.
        messages: A history of messages, typically for interaction with an LLM.
        orientation_complete: A flag indicating if the initial orientation
            phase has been successfully completed.
        vm_capability_report: A string summarizing the results of the
            environmental probe.
        research_findings: A dictionary to store the results of research tasks.
        draft_postmortem_path: The file path to the draft post-mortem report
            generated during the AWAITING_ANALYSIS state.
        final_report: A string containing a summary of the final, completed
            post-mortem report.
        error: An optional string that holds an error message if the FSM
            enters an error state, providing a clear reason for the failure.
    """

    task: str
    task_description: str = ""
    plan_path: Optional[str] = None
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
    background_processes: Dict[str, Any] = field(default_factory=dict)
    current_thought: Optional[str] = None

    def to_json(self):
        return {
            "task": self.task,
            "plan_path": self.plan_path,
            "plan_stack": [
                {
                    "plan_path": ctx.plan_path,
                    "current_step": ctx.current_step,
                    "plan_length": len(ctx.commands),
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
