import json
from typing import Dict, Any, List
from ..helpers import generate_with_model, extract_and_parse_json

def _create_prompt(articles: List[Dict[str, Any]], user_prompt: str) -> str:
    """Creates the system prompt for the LLM to generate the final report."""

    articles_str = "\n".join(
        f"""[{index + 1}] Title: {article.get('title', 'N/A')}
URL: {article.get('url', 'N/A')}
Content: {article.get('content', 'N/A')}
---"""
        for index, article in enumerate(articles)
    )

    return f"""You are a research assistant tasked with creating a comprehensive
 report based on multiple sources.
The report should specifically address this request: "{user_prompt}"

Your report should:
1. Have a clear title that reflects the specific analysis requested
2. Begin with a concise executive summary
3. Be organized into relevant sections based on the analysis requested
4. Use markdown formatting for emphasis, lists, and structure
5. Use citations ONLY when necessary for specific claims, statistics, direct quotes, or important facts
6. Maintain objectivity while addressing the specific aspects requested in the prompt
7. Compare and contrast the information from sources, noting areas of consensus or points of contention
8. Showcase key insights, important data, or innovative ideas

Here are the source articles to analyze (numbered for citation purposes):
{articles_str}

Format the report as a JSON object with the following structure:
{{
  "title": "Report title",
  "summary": "Executive summary (can include markdown)",
  "sections": [
    {{
      "title": "Section title",
      "content": "Section content with markdown formatting and selective citations"
    }}
  ],
  "usedSources": [1, 2]
}}

CITATION GUIDELINES:
1. Only use citations when truly necessary for direct quotes, stats, or non-obvious facts.
2. DO NOT use citations for general knowledge or your own analysis.
3. When needed, use superscript citation numbers in square brackets [¹], [²], etc.
4. Track which sources you actually cite and include their numbers in the "usedSources" array.
"""

def generate_final_report(
    selected_results: List[Dict[str, Any]],
    sources: List[Dict[str, Any]],
    prompt: str,
    platform_model: str
) -> Dict[str, Any]:
    """
    Generates a final, detailed research report from a list of articles.
    This is a Python port of `app/api/report/route.ts`.
    """
    if not prompt or not selected_results:
        return {"error": "Prompt and selected results are required", "status": 400}

    system_prompt = _create_prompt(selected_results, prompt)

    try:
        llm_response = generate_with_model(system_prompt, platform_model)
        if not llm_response:
            raise ValueError("No response from model")

        report_data = extract_and_parse_json(llm_response)

        # Add the original sources to the final report object
        report_data["sources"] = sources
        report_data["status"] = 200
        return report_data

    except Exception as e:
        return {"error": f"Failed to generate final report: {e}", "status": 500}