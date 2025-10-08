from typing import Dict, Any
from ..helpers import generate_with_model, extract_and_parse_json

def _create_prompt(prompt: str) -> str:
    """Creates the system prompt for the LLM to optimize a research topic."""
    return f"""You are a research assistant tasked with optimizing a research topic into an effective search query.

Given this research topic: "{prompt}"

Your task is to:
1. Generate ONE optimized search query that will help gather comprehensive information
2. Create an optimized research prompt that will guide the final report generation
3. Suggest a logical structure for organizing the research

The query should:
- Cover the core aspects of the topic
- Use relevant technical terms and synonyms
- Be specific enough to return high-quality results
- Be comprehensive yet concise

Format your response as a JSON object with this structure:
{{
  "query": "the optimized search query",
  "optimizedPrompt": "The refined research prompt that will guide report generation",
  "explanation": "Brief explanation of the optimization strategy",
  "suggestedStructure": [
    "Key aspect 1 to cover",
    "Key aspect 2 to cover",
    "Key aspect 3 to cover"
  ]
}}

Make the query clear and focused, avoiding overly complex or lengthy constructions."""

def optimize_research(prompt: str, platform_model: str) -> Dict[str, Any]:
    """
    Optimizes a research prompt using an LLM to generate a search query,
    refined prompt, and report structure.
    """
    if not prompt:
        return {"error": "Prompt is required", "status": 400}

    if prompt.lower() == 'test':
        return {
            "query": "test",
            "optimizedPrompt": "Analyze and compare different research methodologies...",
            "explanation": "Test optimization strategy",
            "suggestedStructure": ["Test Structure 1", "Test Structure 2"],
            "status": 200
        }

    system_prompt = _create_prompt(prompt)

    try:
        llm_response = generate_with_model(system_prompt, platform_model)
        if not llm_response:
            raise ValueError("No response from model")

        parsed_response = extract_and_parse_json(llm_response)
        parsed_response["status"] = 200
        return parsed_response

    except Exception as e:
        return {"error": f"Failed to optimize research: {e}", "status": 500}