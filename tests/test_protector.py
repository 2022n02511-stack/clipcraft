
from formatters.protector import ContentProtector

original = r"""
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

protector = ContentProtector()

modified, saved = protector.protect_code(original)

print("PROTECTED TEXT:")
print(modified)

restored = protector.restore_code(modified, saved)

print("\nRESTORED TEXT:")
print(restored)

print("\nPROTECTED ITEMS:", len(saved))
print("EXACT MATCH:", restored == original)
