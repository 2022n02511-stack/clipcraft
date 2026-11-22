
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


print("\n--- CLEANER TESTS ---")

cleaner_samples = {
    "code": """
#include <iostream>


using namespace std;


int main() {
    int x = 10;

    return 0;
}
""",

    "prose": """
A connected component is a maximal set


of vertices where every vertex can reach


every other vertex.
""",

"mathematics": r"""
The derivative is:

$$
f'(x) = \lim_{h \to 0}
\frac{f(x+h)-f(x)}{h}
$$


The integral is $\int 2x\,dx = x^2 + C$.
""",

    "structured_notes": """
1. Graphs


2. Trees


3. Hash tables
"""
}

for content_type, original in cleaner_samples.items():
    cleaned = clean_text(original, content_type)

    print(f"\nType: {content_type}")
    print(cleaned)

print("\n--- IDEMPOTENCY TEST ---")

original = """
A paragraph with extra spacing.


Another paragraph.
"""

once = clean_text(original, "prose")
twice = clean_text(once, "prose")

print("First and second results identical:", once == twice)    
assert clean_text(once, "prose") == once

# Code indentation must remain unchanged.
assert clean_text(cleaner_samples["code"], "code") == (
    cleaner_samples["code"].replace("\r\n", "\n").replace("\r", "\n").strip("\n")
)

# Prose should not contain more than one consecutive blank line.
assert "\n\n\n" not in clean_text(cleaner_samples["prose"], "prose")

# Mathematical notation must survive unchanged.
assert r"\lim" in clean_text(cleaner_samples["mathematics"], "mathematics")
assert r"\frac" in clean_text(cleaner_samples["mathematics"], "mathematics")

assert clean_text("", "prose") == ""
assert clean_text("   \n\n  ", "prose") == ""
assert clean_text("", "code") == ""

print("EMPTY INPUT TESTS PASSED")

print("ALL CLEANER ASSERTIONS PASSED")