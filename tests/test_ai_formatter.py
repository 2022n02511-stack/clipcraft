
from formatters.ai_formatter import AIFormatter
from formatters.detector import detect_content

samples = {
    "Mixed": """
A graph consists of vertices and edges.

The following C++ code creates an adjacency list:

vector<vector<int>> adj(n);

The degree of a vertex is the number of edges
connected to it.
"""
}

formatter = AIFormatter()

for name, text in samples.items():
    content_type = detect_content(text)
    result = formatter.format_text(text, content_type)

    print(f"\n{'=' * 40}")
    print(f"{name} | Detected: {content_type}")
    print("=" * 40)
    print(result)
