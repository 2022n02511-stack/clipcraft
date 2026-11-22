
import re


def clean_text(text: str, content_type="prose") -> str:
    if not text:
        return text

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u200b", "").replace("\ufeff", "")

    # Never destroy code indentation.
    if content_type == "code":
        return text.strip("\n")

    lines = []

    for line in text.split("\n"):
        # Preserve leading indentation if present.
        lines.append(line.rstrip())

    text = "\n".join(lines)

    # Limit excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
