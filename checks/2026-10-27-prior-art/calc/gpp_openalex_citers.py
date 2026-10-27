"""List works citing GPP PRL 93, 240401 according to OpenAlex (not INSPIRE), to find non-arXiv citers."""
import json, sys, time, urllib.request, urllib.parse, ssl, urllib.error

def get(url, tries=2):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(url))
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, file=sys.stderr)
            if i == tries-1: raise
            time.sleep(15)

base = "https://api.openalex.org/works"
src = get(base + "/doi:10.1103/PhysRevLett.93.240401")
wid = src["id"].split("/")[-1]
print("OpenAlex id", wid, "cited_by_count", src["cited_by_count"])
out = []
cursor = "*"
while cursor:
    url = f"{base}?filter=cites:{wid}&per-page=100&cursor={urllib.parse.quote(cursor)}&select=id,doi,title,publication_year,primary_location,type"
    d = get(url)
    out += d["results"]
    cursor = d["meta"].get("next_cursor")
    if not d["results"]:
        break
print(len(out), "citing works")
for w in sorted(out, key=lambda x: x["publication_year"] or 0):
    loc = (w.get("primary_location") or {}).get("source") or {}
    print(w["publication_year"], "|", (w["title"] or "")[:110], "|", loc.get("display_name"), "|", w.get("doi"))
