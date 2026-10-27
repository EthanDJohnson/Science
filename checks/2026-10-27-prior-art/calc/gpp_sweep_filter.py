"""Filter hits.txt from gpp_citer_fulltext_sweep.py: keep body passages (not reference lists) where a GPP author
name is within 600 chars of black-hole / information-loss language. Prints compact snippets.
Usage: gpp_sweep_filter.py hits.txt [skip_ids_comma_sep]
"""
import re, sys
txt = open(sys.argv[1]).read()
skip = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else set()
BH = re.compile(r"black[\s-]*hole|evaporat|information (loss|paradox|puzzle)|Hawking", re.I)
NAME = re.compile(r"Gambini et|Gambini and Pullin|Gambini, Porto,? and Pullin|Gambini[- ]Porto[- ]Pullin|\bGPP\b|Pullin et|Gambini, Pullin|Pullin and collab|Gambini,? [A-Z]\.? ?(and|&) Pullin|Gambini et")
blocks = txt.split("=" * 100 + "\n")[1:]
seen = set()
for b in blocks:
    head, _, body = b.partition("\n")
    aid = head.split("|")[0].strip()
    if aid in skip:
        continue
    out = []
    for seg in re.split(r"\n?\[p\. \d+\] ", body):
        if not NAME.search(seg):
            continue
        refs = len(re.findall(r"\[\d+\]\s*[A-Z]\.", seg)) + len(re.findall(r"\d+\]\s+[A-Z]\. [A-Z]", seg))
        for m in NAME.finditer(seg):
            lo, hi = max(0, m.start() - 450), min(len(seg), m.end() + 450)
            w = seg[lo:hi]
            if BH.search(w) and refs < 3 and w[:80] not in seen:
                seen.add(w[:80])
                out.append(w)
                break
    if out:
        print("=" * 90)
        print(head)
        for w in out[:3]:
            print("   >>", w.replace("\n", " "))
