
import os
import warnings
import logging

warnings.filterwarnings(
    "ignore",
    message=r"Direct use of automatic function calling.*"
)

logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("google.genai").setLevel(logging.ERROR)

from google import genai
from formatters.protector import ContentProtector


class AIFormatter:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.1-flash-lite"
        self.protector = ContentProtector()

    
    def format_text(self, text, content_type):

        if not text.strip():
            return text

        if content_type == "code":
            return text

        # Protect code before sending text to Gemini.
        protected_text, saved_code = self.protector.protect_code(text)

        instructions = """
    You are ClipCraft, an intelligent text formatting engine.

    Your job is to reconstruct messy copied text into
    clean, readable, well-structured Markdown.

    STRICT RULES:

    1. Preserve the original meaning and all factual information.
    2. Never invent information or complete missing sentences.
    3. Repair broken lines caused by PDF text extraction.
    4. Identify headings and subheadings.
    5. Reconstruct numbered and bulleted lists.
    6. Preserve mathematical equations, symbols and notation.
    7. Preserve technical terminology exactly.
    8. Do not simplify or summarize the material.
    9. Do not add explanations or commentary.
    10. Do not modify, remove, or rearrange placeholders.
    11. If text is already properly formatted, leave it alone.
    12. Return only the formatted text.
    """

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"""
    Content type: {content_type}

    Text to format:

    {protected_text}
    """,
            config={
                "system_instruction": instructions,
                "temperature": 0.1,
                "max_output_tokens": 8192
            }
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        formatted_text = response.text.strip()

        # Verify that Gemini preserved every placeholder.
        for placeholder, _ in saved_code:
            if formatted_text.count(placeholder) != 1:
                raise RuntimeError(
                    f"Code placeholder was changed or lost: {placeholder}"
                )

        # Restore the original code.
        formatted_text = self.protector.restore_code(
            formatted_text,
            saved_code
        )

        return formatted_text

