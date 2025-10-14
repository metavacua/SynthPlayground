"""
This module contains the logic for executing research tasks based on a set of
constraints. It acts as a dispatcher, calling the appropriate tool (e.g.,
read_file, google_search) based on the specified target and scope.
"""
import time

# These tools are expected to be available in the global scope where this
# module is executed, injected by the agent's runtime environment.
# We define them here as placeholders to avoid linting errors.
read_file = lambda filepath: None
list_files = lambda path: None
google_search = lambda query: None
view_text_website = lambda url: None


def execute_research_protocol(constraints: dict) -> str:
    """
    Executes a research task based on a provided constraints dictionary.

    Args:
        constraints (dict): A dictionary specifying the research target,
                            scope, and other parameters.

    Returns:
        str: The result of the research action, or an error message.
    """
    target = constraints.get("target")

    if target == "local_filesystem":
        scope = constraints.get("scope")
        path = constraints.get("path")
        if not path:
            return "Error: 'path' not specified for local file research."
        if scope == "file":
            return read_file(filepath=path)
        elif scope == "directory":
            files = list_files(path=path)
            return "\n".join(files)

    elif target == "external_web":
        scope = constraints.get("scope")
        if scope == "narrow":
            query = constraints.get("query")
            if not query:
                return "Error: 'query' not specified for narrow web search."
            return google_search(query=query)
        elif scope == "broad":
            url = constraints.get("url")
            if not url:
                return "Error: 'url' not specified for broad web research."
            return view_text_website(url=url)

    elif target == "external_repository":
        url = constraints.get("url")
        if not url:
            return "Error: 'url' not specified for external repository research."
        return view_text_website(url=url)

    return "Error: The provided constraints do not map to a recognized research protocol."