
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
from dotenv import load_dotenv

load_dotenv()


class AIFormatter:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(api_key=api_key)

        # Keep the model that worked in your previous test.
        self.model = "gemini-3.1-flash-lite"

        self.protector = ContentProtector()

    def validate_placeholders(self, text, protected):

        positions = []

        for placeholder, _ in protected:

            count = text.count(placeholder)

            if count != 1:
                raise RuntimeError(
                    f"Protected content was changed or lost: "
                    f"{placeholder}"
                )

            positions.append(text.find(placeholder))

        # Ensure Gemini did not rearrange protected content.
        if positions != sorted(positions):
            raise RuntimeError(
                "Protected content was rearranged by Gemini."
            )

    def format_text(self, text, content_type):

        if not text or not text.strip():
            return text

        # Never send pure programming code for rewriting.
        if content_type == "code":
            return text

        # Protect code and mathematical expressions.
        protected_text, saved_content = (
            self.protector.protect_code(text)
        )

        instructions = """
You are ClipCraft, an intelligent text formatting engine.

Your job is to reconstruct messy copied text into
clean, readable, well-structured Markdown.

STRICT RULES:

1. Preserve the original meaning and factual information.
2. Never invent information or complete missing sentences.
3. Repair broken lines caused by PDF extraction.
4. Identify headings and subheadings.
5. Reconstruct numbered and bulleted lists.
6. Preserve mathematical notation and technical terminology.
7. Do not simplify or summarize the material.
8. Do not add explanations or commentary.
9. Do not modify, remove, duplicate, or rearrange placeholders.
10. Preserve the order of all placeholders.
11. If text is already properly formatted, leave it alone.
12. Return only the formatted text.
"""

        # Request formatting from Gemini.
        try:

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

            formatted_text = response.text

        except Exception as error:

            raise RuntimeError(
                f"Gemini formatting request failed: {error}"
            ) from error

        # Reject empty responses.
        if not formatted_text or not formatted_text.strip():
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        formatted_text = formatted_text.strip()

        # Validate all protected placeholders.
        self.validate_placeholders(
            formatted_text,
            saved_content
        )

        # Restore original code and mathematical expressions.
        restored_text = self.protector.restore_code(
            formatted_text,
            saved_content
        )

        return restored_text
