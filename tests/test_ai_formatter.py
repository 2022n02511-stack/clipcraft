
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

messy_sample = """
Graphs are mathematical structures
consisting of vertices and edges.

Types of graphs

1. Directed graphs
2. Undirected graphs


A graph can be represented using
an adjacency list.
"""

messy_type = detect_content(messy_sample)

messy_result = formatter.format_text(
    messy_sample,
    messy_type
)

print("\nMESSY TEXT TEST:\n")
print(messy_result)

assert messy_result.strip()

mixed_messy_sample = r"""
MIXED CONTENT TEST:

A graph consists of vertices and edges.

The degree of a vertex is calculated using:

$$
degree(v) = number\ of\ edges\ connected\ to\ v
$$

We can store a graph using an adjacency list:

```cpp
vector<vector<int>> adj(n);

void addEdge(int u, int v) {
    adj[u].push_back(v);
}
```

For an undirected graph, each edge is stored in both directions.

The time complexity is `O(V + E)`.

ALL MIXED CONTENT ASSERTIONS PASSED
"""


messy_type = detect_content(mixed_messy_sample)

messy_result = formatter.format_text(
    mixed_messy_sample,
    messy_type
)

print("\nMESSY TEXT TEST:\n")
print(messy_result)

assert messy_result.strip()

print("\n--- FAILURE HANDLING TEST ---")

class MockResponse:
    text = ""


class MockModels:
    def generate_content(self, **kwargs):
        return MockResponse()


class MockClient:
    models = MockModels()


# Temporarily replace the real Gemini client.
original_client = formatter.client
formatter.client = MockClient()

try:
    formatter.format_text(
        "A graph consists of vertices and edges.",
        "prose"
    )

    assert False, "Expected an empty response error."

except RuntimeError as error:
    print("ERROR CAUGHT:", error)

finally:
    formatter.client = original_client

print("FAILURE HANDLING TEST PASSED")

print("\n--- API EXCEPTION TEST ---")


class FailingModels:
    def generate_content(self, **kwargs):
        raise ConnectionError("Simulated network failure")


class FailingClient:
    models = FailingModels()


original_client = formatter.client
formatter.client = FailingClient()

try:
    formatter.format_text(
        "A graph consists of vertices and edges.",
        "prose"
    )

    assert False, "Expected API failure."

except RuntimeError as error:
    print("ERROR CAUGHT:", error)

finally:
    formatter.client = original_client

print("API EXCEPTION TEST PASSED")