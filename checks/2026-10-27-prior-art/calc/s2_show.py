"""Show the S2 citation rows whose title contains a given string. Usage: s2_show.py <json> <substring>"""
import sys, json
d = json.load(open(sys.argv[1]))
for r in d["data"]:
    p = r["citingPaper"]
    if sys.argv[2].lower() in (p.get("title") or "").lower():
        print(json.dumps(r, indent=1)[:3500])
