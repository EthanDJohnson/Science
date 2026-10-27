"""Free-text INSPIRE searches (title+abstract+keywords) for work related to clock/intrinsic decoherence and BH information.
Usage: gpp_inspire_free.py "query 1" "query 2" ...   Prints date, first author, title, citations, arXiv id."""
import sys, json, urllib.parse, urllib.request, time
for q in sys.argv[1:]:
    params = urllib.parse.urlencode({"q": q, "size": 15, "sort": "mostrecent",
                                     "fields": "titles,arxiv_eprints,authors.full_name,preprint_date,citation_count"})
    url = "https://inspirehep.net/api/literature?" + params
    for attempt in range(3):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=60)); break
        except Exception as e:
            time.sleep(4); d = None
    print("#####", q, "| total", d["hits"]["total"] if d else "FAIL")
    for h in (d or {"hits": {"hits": []}})["hits"]["hits"]:
        m = h["metadata"]
        ax = [e["value"] for e in m.get("arxiv_eprints", [])]
        print(" ", m.get("preprint_date"), "|", (m.get("authors") or [{}])[0].get("full_name", ""), "|", m["titles"][0]["title"][:95], "|", m.get("citation_count"), "|", ax[:1])
