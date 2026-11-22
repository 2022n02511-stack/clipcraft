
from formatters.ai_formatter import AIFormatter
from formatters.detector import detect_content

sample = """
A graph consists of vertices and edges.

The following C++ code creates an adjacency list:

```cpp
vector<vector<int>> adj(n);
```

The degree of a vertex is the number of edges
connected to it.
"""

# Initialize the AI formatter
formatter = AIFormatter()

# Detect content type
content_type = detect_content(sample)

print("DETECTED TYPE:", content_type)

# Format the text
result = formatter.format_text(sample, content_type)

print("\nINTEGRATED PROTECTION TEST:\n")
print(result)
