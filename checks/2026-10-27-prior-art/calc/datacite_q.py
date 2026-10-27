"""Helper: query DataCite (indexes arXiv DOIs with titles+abstracts) for recent arXiv papers.
Usage: datacite_q.py "<lucene query>" [size] [created_from]
Prints created date, arXiv id, title. Used as an index independent of INSPIRE/arXiv-API/S2 (all rate-limited or lagging).
"""
import sys, json, urllib.parse, urllib.request

q = sys.argv[1]
size = sys.argv[2] if len(sys.argv) > 2 else "25"
since = sys.argv[3] if len(sys.argv) > 3 else "2026-07-27"
full = f"({q}) AND created:[{since} TO 2026-10-28] AND publisher:arXiv"
params = urllib.parse.urlencode({"query": full, "page[size]": size, "sort": "-created"})
url = "https://api.datacite.org/dois?" + params
req = urllib.request.Request(url, headers={"Accept": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=60))
print("query:", q, "| since", since, "| total:", d["meta"]["total"])
for it in d["data"]:
    a = it["attributes"]
    ident = [i["identifier"] for i in a.get("identifiers", []) if i.get("identifierType") == "arXiv"]
    t = a["titles"][0]["title"] if a.get("titles") else ""
    au = a["creators"][0]["name"] if a.get("creators") else ""
    print(a.get("created", "")[:10], ident, "|", t[:110], "|", au)
