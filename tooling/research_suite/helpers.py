import json
import re
from typing import Dict, Any

def generate_with_model(system_prompt: str, platform_model: str) -> str:
    """
    MOCK IMPLEMENTATION of a function that interacts with an LLM.

    In a real implementation, this would make an API call to the specified
    platform and model (e.g., OpenAI, Google Gemini). For this integration,
    it returns a pre-defined, successful JSON response that mimics the
    expected output for the optimize_research tool.
    """
    print(f"--- MOCK LLM: Generating response for model {platform_model} ---")

    # This is a sample response that the `optimize_research` tool expects.
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

    # Return it as a JSON string, similar to a real API response
    return f"Some text before the json... ```json\n{json.dumps(mock_response, indent=2)}\n``` ... and some text after."


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