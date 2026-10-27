"""List OpenAlex citers of Van Den Broeck 1999 (W2093785929) and mark those without an arXiv version
(theses, books, non-arXiv journals, proceedings), which the arXiv-only full-text sweep could not reach."""
import json, urllib.request, urllib.parse
rows = []
cursor = "*"
while cursor:
    p = urllib.parse.urlencode({"filter": "cites:W2093785929", "per-page": 100, "cursor": cursor,
                                "select": "id,title,publication_year,type,doi,primary_location,locations,authorships"})
    import time
    for _try in range(4):
        try:
            d = json.load(urllib.request.urlopen("https://api.openalex.org/works?" + p, timeout=60)); break
        except Exception as e:
            print("retry", e); time.sleep(20)
    else:
        raise SystemExit("openalex rate-limited")
    rows += d["results"]
    cursor = d["meta"].get("next_cursor")
    if not d["results"]:
        break
print("total citers:", len(rows))
for r in rows:
    locs = r.get("locations") or []
    arx = any("arxiv.org" in ((l.get("landing_page_url") or "") + (l.get("pdf_url") or "")) for l in locs)
    src = ((r.get("primary_location") or {}).get("source") or {}).get("display_name")
    au = (r["authorships"][0]["author"]["display_name"] if r.get("authorships") else "")
    print(r["publication_year"], "|", "ARXIV" if arx else "NOARX", "|", r.get("type"), "|", (r["title"] or "")[:85], "|", au, "|", src, "|", r.get("doi"))
