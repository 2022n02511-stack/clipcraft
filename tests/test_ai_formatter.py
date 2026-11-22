
from formatters.ai_formatter import AIFormatter
from formatters.detector import detect_content
from formatters.protector import ContentProtector


sample = r"""
The derivative of a function is written as $f'(x)$.

The following C++ code creates an adjacency list:

```cpp
vector<vector<int>> adj(n);

for (int i = 0; i < n; i++) {
    cout << i;
}
```

The derivative formula is:

$$
f'(x) = \lim_{h \to 0}
\frac{f(x+h)-f(x)}{h}
$$

We can also write `vector<int>` for an integer vector.

The integral is $\int 2x\,dx = x^2 + C$.
"""


# Initialize the AI formatter
formatter = AIFormatter()
protector = ContentProtector()


# Detect content type
content_type = detect_content(sample)

print("DETECTED TYPE:", content_type)


# Identify protected content
_, protected_items = protector.protect_code(sample)


# Format the text using Gemini
result = formatter.format_text(sample, content_type)


# Display formatted result
print("\nINTEGRATED PROTECTION TEST:\n")
print(result)


# Verify that every protected element survived unchanged
for _, item in protected_items:
    assert item in result, (
        f"Protected content changed or lost: {item}"
    )


print("\nALL PROTECTED CONTENT PRESERVED:", True)
