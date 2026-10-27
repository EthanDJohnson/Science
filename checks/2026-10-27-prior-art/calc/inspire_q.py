"""Helper: run an INSPIRE literature query and print compact rows. Usage: inspire_q.py "<query>" [size]"""
import sys, json, urllib.parse, urllib.request
q = sys.argv[1]
size = sys.argv[2] if len(sys.argv) > 2 else "25"
params = urllib.parse.urlencode({"q": q, "size": size, "sort": "mostrecent",
                                 "fields": "titles,arxiv_eprints,authors.full_name,preprint_date,citation_count"})
url = "https://inspirehep.net/api/literature?" + params
d = json.load(urllib.request.urlopen(url, timeout=60))
print("query:", q, "| total:", d["hits"]["total"])
for h in d["hits"]["hits"]:
    m = h["metadata"]
    ax = [e["value"] for e in m.get("arxiv_eprints", [])]
    au = m["authors"][0]["full_name"] if m.get("authors") else ""
    print(m.get("preprint_date"), ax, "|", m["titles"][0]["title"][:120], "|", au, "| cites", m.get("citation_count"))
