"""For a quote that was not found, show where the longest matching prefix ends and the code points there.

Usage: python3 -I bo_quote_debug.py v2_full.txt "<quote>"
"""
import re
import sys
import unicodedata

p, q = sys.argv[1], sys.argv[2]
t = open(p, encoding="utf-8", errors="replace").read()
ws = lambda s: re.sub(r"\s+", "", s)
T, Q = ws(t), ws(q)
best = 0
pos = -1
for L in range(1, len(Q) + 1):
    i = T.find(Q[:L])
    if i < 0:
        break
    best, pos = L, i
print(f"quote length (no ws) {len(Q)}; longest matching prefix {best}")
if best < len(Q):
    print("quote   :", repr(Q[max(0, best - 10):best + 10]))
    print("paper   :", repr(T[pos + max(0, best - 10):pos + best + 10]))
    c = Q[best]
    print("quote next char:", repr(c), hex(ord(c)), unicodedata.name(c, "?"))
    d = T[pos + best] if pos + best < len(T) else ""
    if d:
        print("paper next char:", repr(d), hex(ord(d)), unicodedata.name(d, "?"))
