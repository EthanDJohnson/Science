"""Post-process hits.txt from vdb_citer_fulltext_grep.py. fetch_text prints "NO MATCH for 'Broeck'" when absent,
which the first pass mis-counted. Here a record counts only if it has real [p. N] passages.
Prints, per record, the passages in which 'Broeck' occurs within 350 chars of a QI/parameter/error word."""
import sys, re
txt = open(sys.argv[1], errors="replace").read()
blocks = txt.split("=" * 100 + "\n")[1:]
KEY = re.compile(r"inequalit|\bQIs?\b|Planck|pocket|femto|10\s*-\s*15|erratum|mistake|error|inconsist|amply|not satisf|violat", re.I)
real = 0
for b in blocks:
    head, _, body = b.partition("\n")
    if "NO MATCH" in body[:300] or "[p." not in body:
        continue
    real += 1
    passages = re.split(r"\n(?=\[p\.)", body)
    out = []
    for p in passages:
        if "[p." not in p[:6]:
            continue
        # window around each Broeck occurrence
        for m in re.finditer(r"Broeck", p):
            w = p[max(0, m.start() - 350): m.end() + 350]
            hits = sorted(set(k.group(0).lower() for k in KEY.finditer(w)))
            if hits:
                out.append((hits, w.replace("\n", " ")))
                break
    print("=" * 90)
    print(head[:200])
    print("   passages with Broeck:", sum(1 for p in passages if p.startswith("[p.")), "| flagged:", len(out))
    for hits, w in out[:3]:
        print("   FLAGS", hits)
        print("   ...", w[:700])
print("records with real Broeck passages:", real)
