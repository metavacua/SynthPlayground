from typing import Dict, Any, Tuple
from .documents import generate_docx, generate_pdf

def _generate_txt(report: Dict[str, Any]) -> bytes:
    """Generates a plain text representation of a report."""
    content = f"{report.get('title', 'Untitled Report')}\n\n"
    content += f"{report.get('summary', '')}\n\n"

    for section in report.get('sections', []):
        content += f"--- {section.get('title', 'Untitled Section')} ---\n"
        content += f"{section.get('content', '')}\n\n"

    return content.strip().encode('utf-8')

def download_report(report: Dict[str, Any], file_format: str) -> Dict[str, Any]:
    """
    Generates a downloadable file (PDF, DOCX, or TXT) from a report.
    This is a Python port of the logic from `app/api/download/route.ts`.

    Args:
        report: The report data dictionary.
        file_format: The desired format ('pdf', 'docx', or 'txt').

    Returns:
        A dictionary containing the file content and the appropriate content type.
    """
    try:
        if file_format == 'pdf':
            content = generate_pdf(report)
            content_type = 'application/pdf'
        elif file_format == 'docx':
            content = generate_docx(report)
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_format == 'txt':
            content = _generate_txt(report)
            content_type = 'text/plain'
        else:
            return {"error": f"Unsupported format: {file_format}", "status": 400}

        return {
            "content": content,
            "content_type": content_type,
            "filename": f"report.{file_format}",
            "status": 200
        }

    except Exception as e:
        return {"error": f"Failed to generate download for format {file_format}: {e}", "status": 500}