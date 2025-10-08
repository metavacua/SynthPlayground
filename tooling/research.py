import os
import requests
from typing import Dict, Any

# --- Configuration ---
# In a real scenario, this might be an environment variable or a config file.
EXTERNAL_REPO_BASE_URL = (
    "https://api.github.com/repos/example_user/example_repo/contents/"
)


def execute_research_protocol(constraints: Dict[str, Any]) -> str:
    """
    Executes a research query based on a structured set of constraints.

    This function acts as a unified interface for various research targets,
    including the local filesystem, external repositories, and the web.
    """
    target = constraints.get("target")

    if target == "local_filesystem":
        return _research_local_filesystem(constraints)
    elif target == "external_repository":
        return _research_external_repository(constraints)
    elif target == "external_web":
        return _research_external_web(constraints)
    else:
        return f"Error: Unknown research target '{target}'."


def _research_local_filesystem(constraints: Dict[str, Any]) -> str:
    """Performs research on the local filesystem."""
    scope = constraints.get("scope", "file")
    path = constraints.get("path", ".")

    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    if scope == "file":
        with open(path, "r") as f:
            return f.read()
    elif scope == "directory":
        return "\n".join(os.listdir(path))
    else:
        return f"Error: Unknown scope '{scope}' for local_filesystem target."


def _research_external_repository(constraints: Dict[str, Any]) -> str:
    """Performs research on a remote GitHub repository."""
    path = constraints.get("path", "")
    url = f"{EXTERNAL_REPO_BASE_URL}{path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching from external repository: {e}"


def _research_external_web(constraints: Dict[str, Any]) -> str:
    """Performs research on the external web (simulated)."""
    query = constraints.get("query", "")
    # In a real implementation, this would use a search API (e.g., Tavily).
    # For this simulation, we return a mock result.
    return f"Simulated web search results for query: '{query}'"


if __name__ == "__main__":
    # Example usage for testing
    print("--- Testing Local Filesystem Research ---")
    file_constraints = {
        "target": "local_filesystem",
        "scope": "file",
        "path": "AGENTS.md",
    }
    dir_constraints = {
        "target": "local_filesystem",
        "scope": "directory",
        "path": "tooling/",
    }
    print(f"File content: {execute_research_protocol(file_constraints)[:100]}...")
    print(f"Directory content: {execute_research_protocol(dir_constraints)}")

    print("\n--- Testing External Repository Research ---")
    repo_constraints = {"target": "external_repository", "path": "README.md"}
    print(f"Repo file content: {execute_research_protocol(repo_constraints)}")

    print("\n--- Testing External Web Research ---")
    web_constraints = {"target": "external_web", "query": "latest advancements in AI"}
    print(execute_research_protocol(web_constraints))
