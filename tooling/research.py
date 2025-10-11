"""
A unified, constraint-based interface for all research and data-gathering operations.

This script abstracts the various methods an agent might use to gather information
(reading local files, accessing the web, querying a database) into a single,
standardized function: `execute_research_protocol`. It is a core component of
the Advanced Orientation and Research Protocol (AORP), providing the mechanism
by which the agent fulfills the requirements of each orientation level (L1-L4).

The function operates on a `constraints` dictionary, which specifies the target,
scope, and other parameters of the research task. This design allows the calling
orchestrator (e.g., `master_control.py`) to request information without needing
to know the underlying implementation details of how that information is fetched.

This script is designed to be executed by a system that has pre-loaded the
following native tools into the execution environment:
- `read_file(filepath: str) -> str`
- `list_files(path: str = ".") -> list[str]`
- `google_search(query: str) -> str`
- `view_text_website(url: str) -> str`
"""

from typing import Dict, Any
from tooling.knowledge_integrator import run_knowledge_integration


def execute_research_protocol(constraints: Dict[str, Any]) -> str:
    """
    Executes a research task based on a dictionary of constraints.

    This function delegates to native, pre-loaded tools based on the specified
    target and scope.

    Args:
        constraints: A dictionary specifying the operational parameters.
            - target: 'local_filesystem', 'external_web', 'external_repository', or 'knowledge_graph'.
            - scope: 'file', 'directory', 'narrow', 'broad', or 'enrich'.
            - path: The file or directory path for local filesystem operations.
            - query: The search term for web research.
            - url: The specific URL for direct web access.
            - input_graph_path: Path to the source knowledge graph.
            - output_graph_path: Path to save the enriched knowledge graph.

    Returns:
        A string containing the result of the research operation.
    """
    target = constraints.get("target")
    scope = constraints.get("scope")
    path = constraints.get("path")
    query = constraints.get("query")
    url = constraints.get("url")

    # Level 1: Read a local file
    if target == "local_filesystem" and scope == "file":
        if not path:
            return "Error: 'path' not specified for local file research."
        # Assumes `read_file` is available in the execution environment
        return read_file(filepath=path)  # noqa

    # Level 2: List a local directory
    elif target == "local_filesystem" and scope == "directory":
        # Assumes `list_files` is available in the execution environment
        return "\n".join(list_files(path=path or "."))  # noqa

    # Level 3: Targeted web search
    elif target == "external_web" and scope == "narrow":
        if not query:
            return "Error: 'query' not specified for narrow web research."
        # Assumes `google_search` is available in the execution environment
        return google_search(query=query)  # noqa

    # Level 4: Broad web research (fetch content from a specific URL)
    elif target == "external_web" and scope == "broad":
        if not url:
            return "Error: 'url' not specified for broad web research."
        # Assumes `view_text_website` is available in the execution environment
        return view_text_website(url=url)  # noqa

    # Level 5: Fetch a file from a specific URL (e.g., from a Git repo)
    elif target == "external_repository":
        if not url:
            return "Error: 'url' not specified for external repository research."
        # Assumes `view_text_website` is available in the execution environment
        return view_text_website(url=url)  # noqa

    # New Target: Knowledge Graph Enrichment
    elif target == "knowledge_graph" and scope == "enrich":
        input_path = constraints.get("input_graph_path", "knowledge_core/protocols.ttl")
        output_path = constraints.get(
            "output_graph_path", "knowledge_core/enriched_protocols.ttl"
        )
        return run_knowledge_integration(input_path, output_path)

    else:
        return "Error: The provided constraints do not map to a recognized research protocol."
