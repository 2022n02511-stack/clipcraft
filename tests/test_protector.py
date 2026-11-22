
from formatters.protector import ContentProtector

original = """
Here is a graph implementation:

```cpp
vector<vector<int>> adj(n);

for (int i = 0; i < n; i++) {
    cout << i;
}
```

This creates an adjacency list.
"""

protector = ContentProtector()

modified, saved = protector.protect_code(original)

print("PROTECTED TEXT:")
print(modified)

restored = protector.restore_code(modified, saved)

print("\nRESTORED TEXT:")
print(restored)

print("\nEXACT MATCH:", restored == original)
