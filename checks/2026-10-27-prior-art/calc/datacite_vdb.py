"""DataCite sweep (all publishers incl. Zenodo, OSF, Figshare, SSRN-like repositories, theses) for records
mentioning Van Den Broeck / warp drive quantum inequality. Usage: datacite_vdb.py "<lucene>" [size]"""
import sys, json, urllib.parse, urllib.request
q = sys.argv[1]
size = sys.argv[2] if len(sys.argv) > 2 else "40"
params = urllib.parse.urlencode({"query": q, "page[size]": size, "sort": "-created"})
req = urllib.request.Request("https://api.datacite.org/dois?" + params, headers={"Accept": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=60))
print("query:", q, "| total:", d["meta"]["total"])
for it in d["data"]:
    a = it["attributes"]
    t = a["titles"][0]["title"] if a.get("titles") else ""
    pub = a.get("publisher")
    pub = pub.get("name") if isinstance(pub, dict) else pub
    desc = ""
    for x in a.get("descriptions", []) or []:
        desc = x.get("description", "")
        break
    au = a["creators"][0]["name"] if a.get("creators") else ""
    print(a.get("created", "")[:10], "|", pub, "|", a["doi"], "|", t[:100], "|", au, "|", desc[:150].replace("\n", " "))
