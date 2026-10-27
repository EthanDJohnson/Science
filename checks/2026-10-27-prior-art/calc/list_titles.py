"""Compact list of titles/years/arXiv ids from a saved lit_search output. Usage: list_titles.py <file>"""
import sys, re
lines = open(sys.argv[1]).read().splitlines()
i = 0
n = 0
while i < len(lines):
    l = lines[i]
    if l.startswith("- "):
        title = l[2:]
        meta = lines[i+1].strip() if i+1 < len(lines) else ""
        ax = ""
        for j in range(i+2, min(i+5, len(lines))):
            m = re.search(r"arXiv:(\S+)", lines[j])
            if m:
                ax = m.group(1); break
        n += 1
        print(f"{n:3d} | {meta[:60]} | {ax} | {title[:110]}")
    i += 1
