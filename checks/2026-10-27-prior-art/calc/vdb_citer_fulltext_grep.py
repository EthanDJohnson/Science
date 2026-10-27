"""Full-text sweep of papers that cite Van Den Broeck 1999 (INSPIRE recid 500415),
Krasnikov 2003 (gr-qc/0207057) and Pfenning-Ford 1997 (gr-qc/9702026), looking for any
passage that mentions Van Den Broeck near quantum-inequality / parameter / error language.

Usage: vdb_citer_fulltext_grep.py OUTDIR
Writes OUTDIR/citers.json (list of records), OUTDIR/hits.txt (all Broeck passages with flags),
OUTDIR/summary.txt (records ranked by flag count).
Uses fetch_text.py (the project's own text extractor); no network policy is bypassed.
"""
import sys, os, json, re, subprocess, urllib.parse, urllib.request, time
from concurrent.futures import ThreadPoolExecutor

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
FETCH = ".claude/skills/conundrum/scripts/fetch_text.py"
QUERIES = {
    "vdb": "refersto:recid:500415",
    "krasnikov2003": "refersto:recid:590610",
    "pfenning_ford": "refersto:recid:440391",
}
FLAGS = ["inequalit", "QI", "Planck", "pocket", "10 -15", "10^-15", "femto", "erratum", "error", "mistake",
         "inconsist", "violat", "not satisf", "amply", "corrected", "check"]


def inspire(q, size=150):
    params = urllib.parse.urlencode({"q": q, "size": size, "sort": "mostrecent",
                                     "fields": "titles,arxiv_eprints,authors.full_name,preprint_date,citation_count"})
    url = "https://inspirehep.net/api/literature?" + params
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(url, timeout=90))
        except Exception as e:
            time.sleep(3)
    raise RuntimeError("inspire failed " + q)


recs = {}
for tag, q in QUERIES.items():
    d = inspire(q)
    print(tag, "total", d["hits"]["total"], file=sys.stderr)
    for h in d["hits"]["hits"]:
        m = h["metadata"]
        ax = [e["value"] for e in m.get("arxiv_eprints", [])]
        if not ax:
            continue
        a = ax[0]
        r = recs.setdefault(a, {"arxiv": a, "title": m["titles"][0]["title"],
                                "author": (m.get("authors") or [{}])[0].get("full_name", ""),
                                "date": m.get("preprint_date"), "cites": m.get("citation_count"), "via": []})
        r["via"].append(tag)
json.dump(list(recs.values()), open(os.path.join(OUT, "citers.json"), "w"), indent=1)
print("unique arxiv records:", len(recs), file=sys.stderr)


def grep(a):
    url = "https://arxiv.org/pdf/" + a
    for attempt in range(2):
        try:
            p = subprocess.run(["python3", "-I", FETCH, url, "--grep", "Broeck", "--context", "350",
                                "--max-matches", "8"], capture_output=True, text=True, timeout=150)
            out = p.stdout + p.stderr
            if "429" in out[:400] or "Too Many" in out[:400]:
                time.sleep(10)
                continue
            return out
        except subprocess.TimeoutExpired:
            return "TIMEOUT"
    return "RATE-LIMITED"


def work(r):
    out = grep(r["arxiv"])
    r["raw"] = out
    low = out.lower()
    r["has_broeck"] = "broeck" in low
    r["flags"] = [f for f in FLAGS if f.lower() in low]
    return r


with ThreadPoolExecutor(max_workers=4) as ex:
    done = list(ex.map(work, list(recs.values())))

with open(os.path.join(OUT, "hits.txt"), "w") as f:
    for r in done:
        f.write("=" * 100 + "\n%s | %s | %s | %s | via %s\n" % (r["arxiv"], r["date"], r["author"], r["title"], r["via"]))
        f.write(r["raw"][:6000] + "\n")
with open(os.path.join(OUT, "summary.txt"), "w") as f:
    for r in sorted(done, key=lambda r: -len(r["flags"]) if r["has_broeck"] else 1):
        status = "BROECK" if r["has_broeck"] else ("ERR/none:" + r["raw"][:60].replace("\n", " "))
        f.write("%s | %s | %s | %s | flags=%s | %s\n" % (r["arxiv"], r["date"], r["author"], r["title"][:70], r["flags"], status))
print("done", len(done), file=sys.stderr)
