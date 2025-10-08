import json
from typing import Dict, Any

# --- Import all the research tools using relative imports ---
from .tools import search as search_tool
from .tools import fetch_content as fetch_content_tool
from .tools import parse_document as parse_document_tool
from .tools import optimize_research as optimize_research_tool
from .tools import analyze_results as analyze_results_tool
from .tools import consolidate_report as consolidate_report_tool
from .tools import generate_final_report as generate_final_report_tool
from .tools import download as download_tool

# A mapping from task names to their corresponding functions
TASK_DISPATCHER = {
    "search": search_tool.perform_search,
    "fetch_content": fetch_content_tool.fetch_content,
    "parse_document": parse_document_tool.parse_document,
    "optimize_research": optimize_research_tool.optimize_research,
    "analyze_results": analyze_results_tool.analyze_results,
    "consolidate_report": consolidate_report_tool.consolidate_report,
    "generate_final_report": generate_final_report_tool.generate_final_report,
    "download_report": download_tool.download_report,
}

def run_research_task(constraints: Dict[str, Any]) -> str:
    """
    Orchestrates the research workflow by dispatching tasks to the
    appropriate tools within the research suite.

    The `constraints` dictionary must contain a 'task' key, which
    determines which tool to run. The rest of the keys in `constraints`
    are passed as keyword arguments to the selected tool.

    Args:
        constraints: A dictionary containing the task and its arguments.

    Returns:
        A JSON string representing the result from the executed tool.
    """
    task = constraints.get("task")
    if not task:
        return json.dumps({"error": "A 'task' must be specified in the constraints", "status": 400})

    if task not in TASK_DISPATCHER:
        return json.dumps({"error": f"Unknown task: {task}", "status": 400})

    task_function = TASK_DISPATCHER[task]
    task_args = {k: v for k, v in constraints.items() if k != 'task'}

    try:
        result = task_function(**task_args)
        # Assuming the tool function returns a dictionary that is JSON serializable
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"An error occurred while executing task '{task}': {e}", "status": 500})