import json
from typing import Dict, Any, List
from ..helpers import generate_with_model

def _create_prompt(reports: List[Dict[str, Any]], source_index: str) -> str:
    """Creates the prompt for the LLM to consolidate reports."""

    reports_str = "\n\n".join(
        f"""Report {index + 1} Title: {report.get('title', 'N/A')}
Report {index + 1} Summary: {report.get('summary', 'N/A')}
Key Findings:
{"".join([f"- {section.get('title', '')}: {section.get('content', '')}" for section in report.get('sections', [])])}
"""
        for index, report in enumerate(reports)
    )

    return f"""Create a comprehensive consolidated report that synthesizes the following research reports:

{reports_str}

Sources for citation:
{source_index}

Analyze and synthesize these reports to create a comprehensive consolidated report that:
1. Identifies common themes and patterns across the reports
2. Highlights key insights and findings
3. Shows how different reports complement or contrast each other
4. Draws overarching conclusions
5. Suggests potential areas for further research
6. Uses citations only when necessary to reference specific claims, statistics, or quotes from sources

Format the response as a structured report with:
- A clear title that encompasses the overall research topic
- An executive summary of the consolidated findings
- Detailed sections that analyze different aspects
- A conclusion that ties everything together
- Judicious use of citations in superscript format [¹], [²], etc. ONLY when necessary

Return the response in the following JSON format:
{{
  "title": "Overall Research Topic Title",
  "summary": "Executive summary of findings",
  "sections": [
    {{
      "title": "Section Title",
      "content": "Section content with selective citations"
    }}
  ],
  "usedSources": [1, 2]
}}

CITATION GUIDELINES:
1. Only use citations when truly necessary.
2. DO NOT use citations for general knowledge or your own analysis.
3. When needed, use superscript citation numbers in square brackets [¹], [²], etc.
4. The citation numbers correspond directly to the source numbers provided.
5. Track which sources you actually cite and include their numbers in the "usedSources" array.
"""

def consolidate_report(reports: List[Dict[str, Any]], platform_model: str) -> Dict[str, Any]:
    """
    Consolidates multiple research reports into a single, comprehensive report.
    This is a Python port of `app/api/consolidate-report/route.ts`.
    """
    if not reports:
        return {"error": "Reports are required", "status": 400}

    # De-duplicate sources from all reports
    all_sources = []
    source_map = {}
    for report in reports:
        for source in report.get("sources", []):
            if source.get("id") not in source_map:
                source_map[source["id"]] = len(all_sources)
                all_sources.append(source)

    # Create the source index for the prompt
    source_index_str = "\n".join(
        f"[{i + 1}] Source: {s.get('name', 'N/A')} - {s.get('url', 'N/A')}"
        for i, s in enumerate(all_sources)
    )

    prompt = _create_prompt(reports, source_index_str)

    try:
        llm_response = generate_with_model(prompt, platform_model)
        if not llm_response:
            raise ValueError("No response from model")

        # Parse the response, with a fallback
        try:
            parsed_response = json.loads(llm_response)
        except json.JSONDecodeError:
            # This is a basic fallback and might not be robust.
            # In a real scenario, you might want more sophisticated error handling.
            parsed_response = {
                "title": "Consolidated Research Report",
                "summary": llm_response.split('\n\n')[0] if '\n\n' in llm_response else llm_response,
                "sections": [{"title": "Findings", "content": llm_response}],
                "usedSources": []
            }

        # Add the de-duplicated sources to the final report
        parsed_response["sources"] = all_sources
        parsed_response["status"] = 200
        return parsed_response

    except Exception as e:
        return {"error": f"Failed to consolidate reports: {e}", "status": 500}