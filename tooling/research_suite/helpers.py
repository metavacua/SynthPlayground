import json
import re
from typing import Dict, Any

def generate_with_model(system_prompt: str, platform_model: str) -> str:
    """
    MOCK IMPLEMENTATION of a function that interacts with an LLM.

    This has been updated to be "smarter". It inspects the system prompt
    to determine which tool is likely calling it and returns an appropriately
    structured mock JSON response.
    """
    print(f"--- MOCK LLM: Generating response for model {platform_model} ---")

    # Determine the context based on keywords in the prompt. These checks are now
    # more robust and don't break on newlines.
    if "optimizing a research topic" in system_prompt:
        # This is for the `optimize_research` tool
        mock_response = {
            "query": "comprehensive analysis of AI-driven software development workflows",
            "optimizedPrompt": "Provide a detailed analysis of the impact of AI on modern software development lifecycles, including code generation, testing, and deployment.",
            "explanation": "The optimized query focuses on specific, high-impact areas of the software development lifecycle to yield more relevant and technical results.",
            "suggestedStructure": [
                "Introduction: The Rise of AI in Software Engineering",
                "AI-Powered Code Generation and Completion Tools",
                "Automated Testing and Bug Detection with AI",
                "AI in CI/CD and DevOps Pipelines",
                "Future Trends and Challenges"
            ]
        }
    elif "report based on multiple sources" in system_prompt:
        # This is for the `generate_final_report` tool
        mock_response = {
            "title": "Meta-Analysis of the FSM Toolchain Development Process",
            "summary": "The development process involved identifying a key architectural pattern (FSM), constructing a new toolchain based on it, and then using that toolchain to integrate further capabilities. The process was iterative, involving bug fixes and refactoring based on testing and code reviews, demonstrating a robust, self-correcting development loop.",
            "sections": [
                {
                    "title": "Initial Problem and Objective",
                    "content": "The initial objective was to analyze an external repository to find useful concepts for improving our own agentic development toolchain. The core problem was the lack of a reliable, enforceable protocol for development tasks."
                },
                {
                    "title": "Implemented Solution: The FSM Toolchain",
                    "content": "The implemented solution is a Finite State Machine (FSM) that orchestrates the entire development workflow. Key components include the FSM engine (`master_control.py`), a state definition file (`fsm.json`), and a mandatory entry point (`run_task.py`) that ensures all tasks are governed by the protocol. This provides a robust and auditable system."
                },
                {
                    "title": "Integration and Self-Correction",
                    "content": "The toolchain was then used to integrate a 'research suite'. This process revealed and led to the correction of several bugs, including a critical recursion error in the FSM and a logging issue in the test suite. This demonstrates the toolchain's value in enforcing a structured process that catches errors early."
                }
            ],
            "usedSources": [1, 2]
        }
    else:
        # A default fallback response
        mock_response = {"error": "Mock response for this prompt is not implemented."}

    # Return it as a JSON string, similar to a real API response
    return f"```json\n{json.dumps(mock_response, indent=2)}\n```"


def extract_and_parse_json(text: str) -> Dict[str, Any]:
    """
    Extracts a JSON object from a string that may contain other text
    (like markdown code blocks) and parses it.
    """
    # Use a regex to find the content between ```json and ```
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)

    if json_match:
        json_str = json_match.group(1)
    else:
        # As a fallback, find the first '{' and the last '}'
        start = text.find('{')
        end = text.rfind('}')
        if start == -1 or end == -1:
            raise ValueError("No JSON object found in the provided text.")
        json_str = text[start:end+1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse extracted JSON: {e}")