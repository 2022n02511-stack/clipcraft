from formatters.detector import detect_content
from formatters.cleaner import clean_text
from formatters.ai_formatter import AIFormatter


formatter = AIFormatter()


def process_text(text):
    if not text or not text.strip():
        return text

    content_type = detect_content(text)

    print(f"\n[ClipCraft] Detected type: {content_type}")

    cleaned_text = clean_text(text, content_type)

    formatted_text = formatter.format_text(
        cleaned_text,
        content_type
    )

    return formatted_text


if __name__ == "__main__":

    sample = """
    Graphs are mathematical structures
    consisting of vertices and edges.

    Types of graphs

    1. Directed graphs
    2. Undirected graphs
    """

    result = process_text(sample)

    print("\n[ClipCraft] Final output:\n")
    print(result)