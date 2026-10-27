"""Print the source's own words around a regex in a text file saved by fetch_text.py.

Usage (from the project root):
    python3 -I checks/2026-10-27-prior-art/calc/citecheck_grep.py FILE REGEX [PAD] [MAXHITS]

Whitespace is collapsed to single spaces (as fetch_text.py does); nothing else is changed.
Used by the van-den-broeck cite-check to read contexts that the batch quote checker only counted.
"""
import re
import sys

path, pattern = sys.argv[1], sys.argv[2]
pad = int(sys.argv[3]) if len(sys.argv) > 3 else 300
maxhits = int(sys.argv[4]) if len(sys.argv) > 4 else 4
text = re.sub(r"\s+", " ", open(path, encoding="utf-8", errors="replace").read())
hits = list(re.finditer(pattern, text))
print(f"[{path.split('/')[-1]}] /{pattern}/ -> {len(hits)} hits")
for m in hits[:maxhits]:
    print("   ..." + text[max(0, m.start() - pad): m.end() + pad] + "...\n")
