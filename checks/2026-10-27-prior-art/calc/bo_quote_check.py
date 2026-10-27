"""Check every double-quoted B&O passage in section 2 of the Blas-Oller check report against
the v2 (and v1) text dumped by fetch_text.py.

Usage: python3 -I bo_quote_check.py report.md v2_full.txt v1_full.txt

A quote is "found" if, after deleting ALL whitespace from both sides, it is a substring of the
paper text.  Deleting whitespace is the allowance for the PDF extraction dropping/adding spaces.
Quotes that are not found are retried after also dropping hyphen-plus-space line-break artefacts.
Section 2 is taken as the lines between '## 2.' and '## 3.'.
"""
import re
import sys

report, v2p, v1p = sys.argv[1:4]


def strip_ws(s):
    return re.sub(r"[\s\x00-\x1f]+", "", s)  # whitespace and control glyphs (big-bracket pieces)


def load(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    if t.startswith("SOURCE:"):
        t = t.split("\n", 1)[1]
    return t


v2 = strip_ws(load(v2p))
v1 = strip_ws(load(v1p))

lines = open(report, encoding="utf-8").read().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("## 2."))
end = next(i for i, l in enumerate(lines) if l.startswith("## 3."))
sec = lines[start + 1:end]

n = 0
bad = 0
for ln, line in enumerate(sec, start=start + 2):
    # label = bold text at start
    m = re.match(r"\s*-\s*\*\*(.+?)\*\*", line)
    label = m.group(1) if m else ""
    for q in re.findall(r'"([^"]+)"', line):
        n += 1
        k = strip_ws(q)
        in2 = k in v2
        in1 = k in v1
        # retry ignoring hyphen artefacts
        if not in2:
            k2 = k.replace("-", "")
            in2b = k2 in v2.replace("-", "")
        else:
            in2b = True
        status = "FOUND-v2" if in2 else ("FOUND-v2-ignoring-hyphens" if in2b else "NOT-FOUND-v2")
        if not in2b:
            bad += 1
        print(f"report line {ln} [{label}] {status}; in v1: {in1}; len={len(q)}")
        print(f"    {q[:110]}{'...' if len(q) > 110 else ''}")
print(f"TOTAL quotes {n}; not found in v2: {bad}")
