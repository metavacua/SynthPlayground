from typing import Dict, Any
from officeparserpy import parse_office

def parse_document(file_content: bytes) -> Dict[str, Any]:
    """
    Parses a document from its binary content to extract text.
    This is a Python port of the logic in `app/api/parse-document/route.ts`,
    using the officeparserpy library.

    Args:
        file_content: The binary content of the file to parse.

    Returns:
        A dictionary containing the extracted content or an error message.
    """
    if not file_content:
        return {"error": "No file content provided", "status": 400}

    try:
        # The config should be a standard Python dictionary, not an instantiated class.
        config = {
            "output_error_to_console": False,
            "newline_delimiter": '\n',
            "ignore_notes": False,
            "put_notes_at_last": False
        }

        # Parse the document from the buffer
        content = parse_office(file_content, config)

        return {"content": content, "status": 200}

    except Exception as e:
        # Handle any exception during parsing as a failure
        return {"error": f"Failed to extract content from document: {e}", "status": 500}