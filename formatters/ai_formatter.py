
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

    def format_text(self, text, content_type):

        if not text.strip():
            return text

        # Never rewrite programming code.
        if content_type == "code":
            return text

        if content_type == "mixed":
            instructions = """
        You are ClipCraft, a precise document formatter.

        The input contains a mixture of prose, programming code,
        and/or mathematical notation.

        Rules:
        1. Preserve all original meaning and information.
        2. Never rewrite or modify programming code.
        3. Preserve code indentation and syntax exactly.
        4. Preserve all mathematical expressions and symbols.
        5. Format prose into readable paragraphs.
        6. Organize headings and lists where appropriate.
        7. Use Markdown where helpful.
        8. Never invent or summarize content.
        9. Return only the formatted text.
        """

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
10. If text is already properly formatted, leave it alone.
11. Return only the formatted text.

Your priority is accuracy, not creativity.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"""
Content type: {content_type}

Text to format:

{text}
""",
            config={
                "system_instruction": instructions,
                "temperature": 0.1,
                "max_output_tokens": 8192
            }
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()
