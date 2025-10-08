import json
import re
from typing import Dict, Any

def generate_with_model(system_prompt: str, platform_model: str) -> str:
    """
    MOCK IMPLEMENTATION of a function that interacts with an LLM.

    This has been updated to return a detailed, structured JSON object that
    conforms to the new data models defined in `data_models.py`.
    """
    print(f"--- MOCK LLM: Generating response for model {platform_model} ---")

    # This single mock response is designed for the `generate_final_report` tool,
    # as it's the primary producer of the complex Report object.
    mock_response = {
        "title": "Dual-Use Output Architecture Analysis",
        "summary": "This report outlines a new architecture for producing dual-use (human- and machine-readable) outputs from the research suite.",
        "sections": [
            {
                "title": "Core Data Model",
                "content": "The new architecture is built on a set of core dataclasses (`Report`, `Section`, `Source`, `Entity`) that provide a structured representation of the research findings. This model is the single source of truth.",
                "entities": [
                    {"name": "FSM", "type": "Concept", "description": "Finite State Machine"},
                    {"name": "JSON-LD", "type": "Standard", "description": "JSON for Linking Data"}
                ]
            },
            {
                "title": "Serialization Layer",
                "content": "The data model includes serializer methods (`to_markdown`, `to_json_ld`) to convert the structured data into different output formats. This decouples the data from its presentation.",
                "entities": []
            }
        ],
        "sources": [
            {"id": "source-1", "name": "Developer Plan", "url": "local://plan.txt"},
            {"id": "source-2", "name": "TOOLCHAIN_README.md", "url": "local://TOOLCHAIN_README.md"}
        ],
        "used_sources": [1, 2]
    }

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