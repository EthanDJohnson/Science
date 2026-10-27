"""Full-text sweep of arXiv papers that cite GPP (PRL 93, 240401) or the authors' follow-ups
(Braz.J.Phys gr-qc/0501027, GRG review gr-qc/0603090, essay gr-qc/0611148, gr-qc/0505023, IJMPD hep-th/0405183).
For each citer with an arXiv ID, print every passage around 'Gambini' that also mentions black-hole /
evaporation / information-loss language (reference-list entries are filtered out heuristically).
Usage: gpp_citer_fulltext_sweep.py OUTDIR
"""
import sys, os, json, re, subprocess, urllib.parse, urllib.request, time
from concurrent.futures import ThreadPoolExecutor

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
FETCH = ".claude/skills/conundrum/scripts/fetch_text.py"
SEEDS = {  # arXiv id -> tag; resolved to INSPIRE recid (refersto:arxiv:<slash id> misparses in the raw API)
    "hep-th/0406260": "prl",
    "gr-qc/0501027": "braz",
    "gr-qc/0603090": "grg",
    "gr-qc/0611148": "essay",
    "gr-qc/0505023": "discrete",
    "hep-th/0405183": "ijmpd",
}
BH = re.compile(r"black[\s-]*hole|evaporat|information (loss|paradox|puzzle)|Hawking", re.I)


def inspire(q, size=150):
    params = urllib.parse.urlencode({"q": q, "size": size, "sort": "mostrecent",
                                     "fields": "titles,arxiv_eprints,authors.full_name,preprint_date,citation_count"})
    url = "https://inspirehep.net/api/literature?" + params
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(url, timeout=90))
        except Exception:
            time.sleep(4)
    raise RuntimeError("inspire failed " + q)


recs = {}
QUERIES = {}
for aid, tag in SEEDS.items():
    d0 = inspire("arxiv:" + aid)
    recid = d0["hits"]["hits"][0]["id"]
    QUERIES[tag] = "refersto:recid:" + str(recid)
    print(tag, aid, "recid", recid, file=sys.stderr)
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
                                "date": m.get("preprint_date"), "via": []})
        r["via"].append(tag)
json.dump(list(recs.values()), open(os.path.join(OUT, "citers.json"), "w"), indent=1)
print("unique arxiv records:", len(recs), file=sys.stderr)


def grep(a):
    url = "https://arxiv.org/pdf/" + a
    for attempt in range(3):
        try:
            p = subprocess.run(["python3", "-I", FETCH, url, "--regex", r"Gambini|Porto,? ?R|Pullin", "--context", "500",
                                "--max-matches", "25"], capture_output=True, text=True, timeout=180)
            out = p.stdout + p.stderr
            if "429" in out[:500] or "Too Many" in out[:500]:
                time.sleep(12)
                continue
            return out
        except subprocess.TimeoutExpired:
            return "TIMEOUT"
    return "RATE-LIMITED"


def work(r):
    out = grep(r["arxiv"])
    r["raw"] = out
    r["bh_hit"] = bool(BH.search(out))
    return r


with ThreadPoolExecutor(max_workers=4) as ex:
    res = list(ex.map(work, list(recs.values())))
with open(os.path.join(OUT, "hits.txt"), "w") as f:
    for r in res:
        f.write("=" * 100 + "\n%s | %s | %s | via %s | BH=%s\n" % (r["arxiv"], r["author"], r["title"], r["via"], r["bh_hit"]))
        f.write(r["raw"][:6000] + "\n")
with open(os.path.join(OUT, "summary.txt"), "w") as f:
    for r in sorted(res, key=lambda x: (not x["bh_hit"], x["date"] or "")):
        raw = r["raw"]
        status = "NOFETCH" if raw.startswith(("UNAVAILABLE", "TIMEOUT", "RATE")) else ("BH" if r["bh_hit"] else "nohit")
        f.write("%s | %s | %s | %s | %s\n" % (status, r["arxiv"], r["author"], r["date"], r["title"][:90]))
print("done", len(res), file=sys.stderr)
