import json
from typing import Dict, Any, List
from ..helpers import generate_with_model, extract_and_parse_json
from ..data_models import Report, Source

def _create_prompt(articles: List[Dict[str, Any]], user_prompt: str) -> str:
    """Creates the system prompt for the LLM to generate the final structured report."""

    articles_str = "\n".join(
        f"""[{index + 1}] Title: {article.get('title', 'N/A')}
URL: {article.get('url', 'N/A')}
Content: {article.get('content', 'N/A')}
---"""
        for index, article in enumerate(articles)
    )

    return f"""You are a research assistant tasked with creating a comprehensive, structured report based on multiple sources.
The report should specifically address this request: "{user_prompt}"

Your report should:
1. Have a clear title that reflects the specific analysis requested.
2. Begin with a concise executive summary.
3. Be organized into relevant sections.
4. Identify key entities (people, organizations, topics) mentioned in the text.

Here are the source articles to analyze (numbered for citation purposes):
{articles_str}

Format the report as a JSON object with the following structure:
{{
  "title": "Report title",
  "summary": "Executive summary of the report's findings.",
  "sections": [
    {{
      "title": "Section title",
      "content": "Section content, in Markdown format.",
      "entities": [
        {{"name": "Entity Name", "type": "Entity Type", "description": "Brief description"}}
      ]
    }}
  ],
  "used_sources": [1, 2]
}}
"""

def generate_final_report(
    selected_results: List[Dict[str, Any]],
    sources: List[Source],
    prompt: str,
    platform_model: str
) -> Report:
    """
    Generates a final, detailed research report as a structured Report object.
    """
    if not prompt or not selected_results:
        raise ValueError("Prompt and selected results are required")

    system_prompt = _create_prompt(selected_results, prompt)

    try:
        llm_response = generate_with_model(system_prompt, platform_model)
        if not llm_response:
            raise ValueError("No response from model")

        report_data = extract_and_parse_json(llm_response)

        # Add the original sources to the report data before creating the object
        report_data["sources"] = [s.__dict__ for s in sources]

        # **BUG FIX**: Validate the used_sources from the LLM to prevent IndexError.
        # This makes the tool robust against the LLM hallucinating invalid source indices.
        valid_used_sources = []
        if 'used_sources' in report_data:
            max_index = len(sources)
            for i in report_data['used_sources']:
                if 1 <= i <= max_index:
                    valid_used_sources.append(i)
        report_data['used_sources'] = valid_used_sources

        # Create a Report object from the dictionary
        report_obj = Report.from_dict(report_data)

        return report_obj

    except Exception as e:
        print(f"Error generating final report object: {e}")
        raise