"""Summarise Semantic Scholar citation contexts for a saved /citations JSON of hep-th/0406260.
Usage: gpp_s2_contexts.py <json>
Prints counts, then every citing paper that has at least one context (title, year, intents, contexts).
"""
import sys, json

d = json.load(open(sys.argv[1]))
rows = d["data"]
print("citers returned:", len(rows), "| next:", d.get("next"))
withctx = [r for r in rows if r.get("contexts")]
print("with contexts:", len(withctx))
for r in withctx:
    p = r["citingPaper"]
    print(f"\n## {p.get('year')} | {p.get('title')} | intents={r.get('intents')}")
    for c in r["contexts"]:
        print("   -", c[:700].replace("\n", " "))
