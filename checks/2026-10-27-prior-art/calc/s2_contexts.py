"""Summarise Semantic Scholar citation contexts for a saved /citations JSON. Usage: s2_contexts.py <json>
Prints total citers, how many have contexts, and every context that mentions QI / quantum inequality /
Planck / femto / 10^-15 / curvature radius / energy density."""
import sys, json, re
d = json.load(open(sys.argv[1]))
rows = d["data"]
print("citers returned:", len(rows), "| next:", d.get("next"))
withctx = [r for r in rows if r.get("contexts")]
print("with contexts:", len(withctx))
pat = re.compile(r"quantum inequal|\bQIs?\b|planck|femto|10\s*-?\s*15|curvature radius|negative energy|energy density|satisf", re.I)
for r in rows:
    p = r["citingPaper"]
    hits = [c for c in (r.get("contexts") or []) if pat.search(c)]
    if hits:
        print(f"\n## {p.get('year')} | {p.get('title')}")
        for c in hits:
            print("   -", c[:600])
