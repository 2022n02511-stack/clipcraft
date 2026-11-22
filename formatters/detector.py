
import re


def contains_math_expression(text: str) -> bool:
    patterns = [
        r"\\(?:frac|sum|int|lim|sqrt)",
        r"[=<>]\s*[\w(]",
        r"\b(?:lim|sin|cos|tan|log)\s*\(",
        r"\b[a-zA-Z]\s*['′]?\s*\([^)]*\)\s*=",
        r"\b[a-zA-Z]\s*=\s*[\w(]",
    ]

    return any(re.search(pattern, text) for pattern in patterns)

def contains_code(text: str) -> bool:
    code_patterns = [
        r"#include\s*<",
        r"\busing\s+namespace\b",
        r"\bint\s+main\s*\(",
        r"\bvector\s*<",
        r"\bmap\s*<",
        r"\bclass\s+\w+",
        r"\bdef\s+\w+\s*\(",
        r"\breturn\b",
        r"\bfor\s*\(",
        r"\bwhile\s*\(",
        r"[{};]"
    ]

    score = sum(
        bool(re.search(pattern, text))
        for pattern in code_patterns
    )

    return score >= 2


def contains_math(text: str) -> bool:
    math_patterns = [
        r"[∑∫√≤≥≠∞∏∂∇≈±×÷∈∉⊂⊆∀∃]",
        r"\\frac|\\sum|\\int|\\lim|\\sqrt",
        r"\b[a-zA-Z]\s*['′]?\s*\([^)]*\)\s*=",
        r"\blim\s*\(",
        r"\b[a-zA-Z]\s*\([^)]*\)\s*=",
    ]

    return any(
        re.search(pattern, text)
        for pattern in math_patterns
    )


def contains_prose(text: str) -> bool:
    remaining_lines = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        # Ignore lines that look like programming code.
        if re.search(
            r"[{};]|"
            r"^\s*#include\b|"
            r"^\s*using\s+namespace\b|"
            r"\b(?:int|void|bool|string|float|double)\s+\w+\s*\(",
            stripped
        ):
            continue

        remaining_lines.append(stripped)

    remaining_text = " ".join(remaining_lines)
    words = re.findall(r"\b[A-Za-z]{3,}\b", remaining_text)

    return len(words) >= 5


def detect_content(text: str) -> str:
    if not text.strip():
        return "empty"

    code = contains_code(text)
    math = contains_math(text)
    prose = contains_prose(text)

    if code and prose:
        return "mixed"

    if math and prose and contains_math_expression(text):
        return "mixed"

    if code:
        return "code"

    if math:
        return "mathematics"

    lines = text.splitlines()

    list_lines = sum(
        bool(re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line))
        for line in lines
    )

    if list_lines >= 2:
        return "structured_notes"

    return "prose"
