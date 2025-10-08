from typing import Dict, Any, List
from ..helpers import generate_with_model, extract_and_parse_json

def _create_prompt(prompt: str, results: List[Dict[str, Any]]) -> str:
    """Creates the system prompt for the LLM to analyze search results."""

    results_str = "\n".join(
        f"""Result {index + 1}:
Title: {result.get('title', 'N/A')}
URL: {result.get('url', 'N/A')}
Snippet: {result.get('snippet', 'N/A')}
{'Full Content: ' + result['content'] if result.get('content') else ''}
---"""
        for index, result in enumerate(results)
    )

    return f"""You are a research assistant tasked with analyzing search results
 for relevance to a research topic.

Research Topic: "{prompt}"

Analyze these search results and score them based on:
1. Relevance to the research topic
2. Information quality and depth
3. Source credibility
4. Uniqueness of perspective

For each result, assign a score from 0 to 1, where:
- 1.0: Highly relevant, authoritative, and comprehensive
- 0.7-0.9: Very relevant with good information
- 0.4-0.6: Moderately relevant or basic information
- 0.1-0.3: Tangentially relevant
- 0.0: Not relevant or unreliable

Here are the results to analyze:
{results_str}

Format your response as a JSON object with this structure:
{{
  "rankings": [
    {{
      "url": "result url",
      "score": 0.85,
      "reasoning": "Brief explanation of the score"
    }}
  ],
  "analysis": "Brief overall analysis of the result set"
}}

Focus on finding results that provide unique, high-quality information relevant
to the research topic."""


def analyze_results(
    prompt: str,
    results: List[Dict[str, Any]],
    platform_model: str,
    is_test_query: bool = False
) -> Dict[str, Any]:
    """
    Analyzes and ranks search results based on a research prompt using an LLM.
    This is a Python port of `app/api/analyze-results/route.ts`.
    """
    if not prompt or not results:
        return {"error": "Prompt and results are required", "status": 400}

    # Return test results for test queries
    if is_test_query or any("example.com/test" in r.get("url", "") for r in results):
        return {
            "rankings": [
                {"url": result["url"], "score": 1.0 if i == 0 else 0.5, "reasoning": "Test ranking result"}
                for i, result in enumerate(results)
            ],
            "analysis": "Test analysis of search results",
            "status": 200
        }

    system_prompt = _create_prompt(prompt, results)

    try:
        # Generate the analysis using the existing LLM function
        llm_response = generate_with_model(system_prompt, platform_model)

        if not llm_response:
            raise ValueError("No response from model")

        # Parse the JSON response
        parsed_response = extract_and_parse_json(llm_response)
        parsed_response["status"] = 200
        return parsed_response

    except Exception as e:
        return {"error": f"Failed to analyze results: {e}", "status": 500}