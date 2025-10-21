import os
import google.generativeai as genai


class GeminiApiClient:
    """A client for interacting with the Gemini API."""

    def __init__(self, api_key=None):
        """Initializes the Gemini API client.
        Args:
            api_key: The API key for the Gemini API. If not provided, it will be
                read from the GEMINI_API_KEY environment variable.
        """
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key not provided.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            "gemini-pro-vision"
        )  # Use a vision-capable model

    def generate_text(self, prompt):
        """Generates text using the Gemini API.
        Args:
            prompt: The prompt to use for text generation.
        Returns:
            The generated text.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def process_document(
        self, document_path, prompt="Extract the text from this document."
    ):
        """Processes a document using the Gemini API.
        Args:
            document_path: The path to the document to process.
            prompt: The prompt to use for document processing.
        Returns:
            The processed document content.
        """
        try:
            with open(document_path, "rb") as f:
                document_bytes = f.read()

            document_part = genai.types.Part.from_binary(
                data=document_bytes, mime_type="application/pdf"
            )

            response = self.model.generate_content([prompt, document_part])
            return response.text
        except Exception as e:
            return f"Error processing document {document_path} with Gemini API: {e}"
