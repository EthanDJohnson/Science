"""Scan a saved INSPIRE JSON (curl of refersto:arxiv:hep-th/0406260 with abstracts) and print the
full abstract of every record whose title/abstract contains any keyword.
Usage: gpp_citers_abstracts.py <in_json> [keyword ...]   (no keywords -> print all titles only)
"""
import sys, json

d = json.load(open(sys.argv[1]))
kws = [k.lower() for k in sys.argv[2:]]
rows = d["hits"]["hits"]
print("records:", len(rows), "total reported:", d["hits"]["total"])
for h in rows:
    m = h["metadata"]
    title = m["titles"][0]["title"]
    ab = " ".join(a["value"] for a in m.get("abstracts", []))
    text = (title + " " + ab).lower()
    hit = [k for k in kws if k in text]
    ax = [e["value"] for e in m.get("arxiv_eprints", [])]
    au = m["authors"][0]["full_name"] if m.get("authors") else ""
    if not kws:
        print(m.get("preprint_date"), ax, au, "|", title[:100])
    elif hit:
        print("-" * 80)
        print(m.get("preprint_date"), ax, au, "|", title)
        print("  hits:", hit)
        print("  ABSTRACT:", ab[:2200])
