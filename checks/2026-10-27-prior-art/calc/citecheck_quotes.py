"""Batch quote checker for the Blas-Oller prior-art cite-check.

Usage (from the project root):
    python3 -I checks/2026-10-27-prior-art/calc/citecheck_quotes.py SPEC.json OUTDIR [key ...]

SPEC.json is a list of {"key", "url", "quotes": [...], "terms": [...], "abs": "<arxiv abs url>"}.
For each entry the script runs .claude/skills/conundrum/scripts/fetch_text.py on `url` (whole text,
cached in OUTDIR/<key>.txt), then:
  * for each quote, looks for it with whitespace removed and case folded (STRICT), else with every
    non-alphanumeric character removed (LOOSE, covers hyphen-line-break and ligature artefacts), and
    prints the matching passage (+- 350 characters of the source's own text) so the reader can judge
    whether the source says it about this case;
  * for each term, prints the number of hits and the first two passages (used to test absence/presence);
  * if "abs" is given, fetches the arXiv abstract page and prints the submission / revision dates,
    journal reference and comments lines.
Text is the source's own words as printed by fetch_text.py; nothing is paraphrased here.
"""
import json
import re
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FT = ".claude/skills/conundrum/scripts/fetch_text.py"
DASH = {"–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-"}


def fetch(url, path, timeout=90):
    p = Path(path)
    if p.exists() and p.stat().st_size > 200:
        return p.read_text(encoding="utf-8", errors="replace")
    for attempt in range(2):
        r = subprocess.run(["python3", FT, url, "--max-chars", "4000000", "--timeout", "60"],
                           capture_output=True, text=True, timeout=timeout * 2)
        out = r.stdout
        if len(out) > 400 and "BLOCKED" not in out[:300]:
            p.write_text(out, encoding="utf-8")
            return out
    p.write_text(r.stdout + "\n[STDERR]\n" + r.stderr[:500], encoding="utf-8")
    return r.stdout


def norm_map(text, loose):
    chars, idx = [], []
    for i, ch in enumerate(text):
        ch = DASH.get(ch, ch)
        for c in unicodedata.normalize("NFKC", ch).casefold():
            if c.isspace() or c == "\x00":
                continue
            if loose and not c.isalnum():
                continue
            chars.append(c)
            idx.append(i)
    return "".join(chars), idx


def find(text, phrase, maps):
    for mode in ("strict", "loose"):
        loose = mode == "loose"
        s, idx = maps[mode]
        q, _ = norm_map(phrase, loose)
        if not q:
            continue
        pos = s.find(q)
        if pos >= 0:
            a, b = idx[pos], idx[pos + len(q) - 1]
            return mode, a, b
    return None


def show(text, a, b, pad=350):
    return re.sub(r"\s+", " ", text[max(0, a - pad): b + pad + 1])


def check(entry, outdir):
    key = entry["key"]
    lines = [f"===== {key}  {entry['url']}"]
    text = fetch(entry["url"], Path(outdir) / f"{key}.txt")
    lines.append(f"[text length {len(text)}; head: {re.sub(chr(10), ' ', text[:130])}]")
    maps = {"strict": norm_map(text, False), "loose": norm_map(text, True)}
    for q in entry.get("quotes", []):
        f = find(text, q, maps)
        if f:
            mode, a, b = f
            lines.append(f"QUOTE-FOUND({mode}): {q[:90]}...")
            lines.append(f"    CONTEXT: {show(text, a, b)}")
        else:
            lines.append(f"QUOTE-NOT-FOUND: {q[:140]}")
    for t in entry.get("terms", []):
        s, idx = maps["strict"]
        q, _ = norm_map(t, False)
        hits = [m.start() for m in re.finditer(re.escape(q), s)]
        lines.append(f"TERM '{t}': {len(hits)} hits")
        for h in hits[:2]:
            lines.append(f"    ...{show(text, idx[h], idx[min(h + len(q) - 1, len(idx) - 1)], 200)}")
    if entry.get("abs"):
        ab = fetch(entry["abs"], Path(outdir) / f"{key}_abs.txt")
        for pat in (r"\[Submitted on[^\]]*\]", r"Journal reference:.{0,160}", r"Comments:.{0,200}",
                    r"\[v\d+\][^\[]{0,60}", r"DOI:.{0,80}"):
            for m in list(re.finditer(pat, re.sub(r"\s+", " ", ab)))[:6]:
                lines.append(f"ABS: {m.group(0)[:230]}")
    return "\n".join(lines)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    Path(outdir).mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[3:])
    spec = [e for e in spec if not only or e["key"] in only]
    with ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(lambda e: check(e, outdir), spec):
            print(res)
            print()
