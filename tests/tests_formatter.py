
from formatters.detector import detect_content
from formatters.cleaner import clean_text


samples = {
    "code": """
#include <iostream>
using namespace std;

int main() {
    return 0;
}
""",

    "mathematics": """
The summation is represented by ∑.
The integral is represented by ∫.
""",

    "prose": """
A connected component is a maximal set
of vertices where every vertex can reach
every other vertex.
"""
}


for expected, original in samples.items():
    detected = detect_content(original)
    cleaned = clean_text(original, detected)

    print(f"\nExpected: {expected}")
    print(f"Detected: {detected}")
    print(f"Cleaned:\n{cleaned}")
