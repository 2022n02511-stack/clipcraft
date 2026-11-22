
from formatters.detector import detect_content
from formatters.cleaner import clean_text

notes_sample = """
1. Graphs
2. Trees
3. Hash tables
4. Sorting algorithms
"""

print("\nExpected: structured_notes")
print("Detected:", detect_content(notes_sample))


math_mixed_sample = """
The derivative measures the rate of change
of a function.

The derivative is defined as:
f'(x) = lim(h -> 0) (f(x+h)-f(x))/h
"""

print("\nExpected: mixed")
print("Detected:", detect_content(math_mixed_sample))


mixed_sample = """
The following function calculates the sum of two numbers:

int add(int a, int b) {
    return a + b;
}

The result is represented mathematically as:
x + y = z
"""

print("\nExpected: mixed")
print("Detected:", detect_content(mixed_sample))


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
