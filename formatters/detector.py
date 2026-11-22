
import re




def contains_mixed_content(text: str) -> bool:
    # Detect common programming constructs.
    code_patterns = [
        r"#include\s*<",
        r"\bvector\s*<",
        r"\bmap\s*<",
        r"\bset\s*<",
        r"\bstring\s+\w+",
        r"\bint\s+\w+\s*\(",
        r"\bdef\s+\w+\s*\(",
        r"\bclass\s+\w+",
        r"\breturn\b",
        r"[{};]"
    ]

    has_code = any(
        re.search(pattern, text)
        for pattern in code_patterns
    )

    # Detect mathematical notation.
    math_patterns = [
        r"[∑∫√≤≥≠∞∏∂∇≈±×÷∈∉⊂⊆∀∃]",
        r"\\frac|\\sum|\\int|\\lim|\\sqrt",
        r"\b[a-zA-Z]\s*\([^)]*\)\s*="
    ]

    has_math = any(
        re.search(pattern, text)
        for pattern in math_patterns
    )

    # Mixed content means prose combined with code or mathematics.
    has_prose = bool(re.search(r"[A-Za-z]{3,}\s", text))

    return has_prose and (has_code or has_math)



def detect_content(text: str) -> str:
    if not text.strip():
        return "empty"

    if contains_mixed_content(text):
        return "mixed"

    lines = text.splitlines()

    # Code detection
    code_patterns = [
        r"#include\s*<",
        r"\bdef\s+\w+\s*\(",
        r"\bclass\s+\w+",
        r"\b(int|float|double|void|bool|string)\s+\w+\s*\(",
        r"\bfor\s*\(",
        r"\bwhile\s*\(",
        r"\breturn\b",
        r"[{};]"
    ]

    code_score = sum(
        bool(re.search(pattern, text))
        for pattern in code_patterns
    )

    if code_score >= 2:
        return "code"

   
    # Mathematical notation
    math_symbols = "∑∫√≤≥≠∞∏∂∇≈±×÷∈∉⊂⊆∀∃"

    math_patterns = [
        r"\\frac",
        r"\\sum",
        r"\\int",
        r"\\alpha",
        r"\\beta",
        r"\\lim",
        r"\\sqrt",
        r"\\infty",
        r"\b(?:lim|sin|cos|tan|log)\s*[\(\w]",
        r"\b[a-zA-Z]\s*=\s*[-\d]",
        r"\b[a-zA-Z]\s*\([^)]*\)\s*="
    ]

    math_score = sum(
        bool(re.search(pattern, text))
        for pattern in math_patterns
    )

    if (
        any(symbol in text for symbol in math_symbols)
        or math_score >= 1
    ):
        return "mathematics"


    # Structured lists
    list_lines = sum(
        bool(re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line))
        for line in lines
    )

    if list_lines >= 2:
        return "structured_notes"

    return "prose"
