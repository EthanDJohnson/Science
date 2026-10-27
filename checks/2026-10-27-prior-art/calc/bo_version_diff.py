"""Word-level diff of Blas & Oller arXiv:2607.24930 v1 vs v2 text (dumped by fetch_text.py).

Usage: python3 -I bo_version_diff.py v1.txt v2.txt [min_words]
Prints each differing block (removed / added words) with a few words of context.
Citation numbers shift between versions ([19, 20] vs [18, 19]), so blocks that are
only digits/brackets/commas are suppressed.
"""
import difflib
import re
import sys

a_path, b_path = sys.argv[1], sys.argv[2]
min_words = int(sys.argv[3]) if len(sys.argv) > 3 else 1


def load(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    t = t.split("\n", 1)[1] if t.startswith("SOURCE:") else t
    return t.split()


a, b = load(a_path), load(b_path)
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    old = " ".join(a[i1:i2])
    new = " ".join(b[j1:j2])
    # skip pure citation-number churn
    if re.fullmatch(r"[\d\[\]\s,\-–]*", old) and re.fullmatch(r"[\d\[\]\s,\-–]*", new):
        continue
    if max(i2 - i1, j2 - j1) < min_words:
        continue
    n += 1
    ctx_b = " ".join(a[max(0, i1 - 6):i1])
    ctx_a = " ".join(a[i2:i2 + 6])
    print(f"--- block {n} [{tag}] v1 words {i1}-{i2}, v2 words {j1}-{j2}")
    print(f"  ...{ctx_b}")
    print(f"  - v1: {old}")
    print(f"  + v2: {new}")
    print(f"  {ctx_a}...")
print(f"TOTAL blocks printed: {n}; v1 words {len(a)}, v2 words {len(b)}")
