#!/usr/bin/env python3
"""Physics literature search for /conundrum researchers (standard library only).

Queries INSPIRE-HEP (citation counts, journal refs; best for gr-qc/hep-th) and the
arXiv API, and prints compact records a researcher can cite. When a source is
unreachable (for example under a restrictive network policy) it says so plainly,
so the researcher can fall back to WebSearch and mark evidence as snippet-level.

Usage (from the project root):
    python3 .claude/skills/conundrum/scripts/lit_search.py "alcubierre negative energy"
    python3 .claude/skills/conundrum/scripts/lit_search.py "quantum inequality warp" --source inspire --sort mostcited
    python3 .claude/skills/conundrum/scripts/lit_search.py 't "warp drive" and date>2020' --source inspire
    python3 .claude/skills/conundrum/scripts/lit_search.py "casimir energy density" --source arxiv --max 5 --json

Exit status: 0 if at least one source answered, 3 if every source was unreachable.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

INSPIRE_URL = "https://inspirehep.net/api/literature"
ARXIV_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"
USER_AGENT = "conundrum-skill/1.0 (research assistant; low volume)"
INSPIRE_FIELDS = ",".join([
    "titles.title", "authors.full_name", "abstracts.value", "arxiv_eprints.value",
    "dois.value", "citation_count", "publication_info", "earliest_date", "control_number",
    "document_type",
])
RETRY_STATUSES = (429, 503)  # arXiv in particular throttles automated clients


class SourceUnavailable(Exception):
    pass


def _get(url: str, timeout: float, retries: int = 2) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code in RETRY_STATUSES and attempt < retries:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                wait = float(retry_after) if retry_after and retry_after.isdigit() else 4.0 * (attempt + 1)
                time.sleep(min(wait, 30.0))
                continue
            label = "rate-limited, try again in a minute" if exc.code in RETRY_STATUSES else exc.reason
            raise SourceUnavailable(f"HTTP {exc.code}: {label}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise SourceUnavailable(str(getattr(exc, "reason", exc))) from exc
    raise SourceUnavailable("no response")  # pragma: no cover - loop always returns or raises


def _clip(text: str, limit: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def parse_inspire(payload: dict) -> list[dict]:
    records = []
    for hit in payload.get("hits", {}).get("hits", []):
        md = hit.get("metadata", {})
        authors = [a.get("full_name", "") for a in md.get("authors", [])]
        pubs = md.get("publication_info") or [{}]
        pub = pubs[0]
        journal = " ".join(str(p) for p in [pub.get("journal_title"), pub.get("journal_volume"),
                                            pub.get("artid") or pub.get("page_start")] if p)
        arxiv = (md.get("arxiv_eprints") or [{}])[0].get("value", "")
        doi = (md.get("dois") or [{}])[0].get("value", "")
        recid = md.get("control_number") or hit.get("id")
        year = str(pub.get("year") or (md.get("earliest_date") or "")[:4])
        records.append({
            "source": "inspire",
            "title": (md.get("titles") or [{}])[0].get("title", ""),
            "authors": authors,
            "year": year,
            "arxiv": arxiv,
            "doi": doi,
            "journal": journal,
            "doc_type": ", ".join(md.get("document_type") or []),
            "citations": md.get("citation_count"),
            "url": f"https://inspirehep.net/literature/{recid}" if recid else "",
            "abstract": (md.get("abstracts") or [{}])[0].get("value", ""),
        })
    return records


def parse_arxiv(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    records = []
    for entry in root.findall(f"{ATOM}entry"):
        abs_url = (entry.findtext(f"{ATOM}id") or "").strip()
        arxiv_id = abs_url.rsplit("/abs/", 1)[-1] if "/abs/" in abs_url else abs_url
        records.append({
            "source": "arxiv",
            "title": " ".join((entry.findtext(f"{ATOM}title") or "").split()),
            "authors": [a.findtext(f"{ATOM}name") or "" for a in entry.findall(f"{ATOM}author")],
            "year": (entry.findtext(f"{ATOM}published") or "")[:4],
            "arxiv": arxiv_id,
            "doi": entry.findtext(f"{ARXIV_NS}doi") or "",
            "journal": entry.findtext(f"{ARXIV_NS}journal_ref") or "",
            "citations": None,
            "url": abs_url,
            "abstract": entry.findtext(f"{ATOM}summary") or "",
            "category": (entry.find(f"{ARXIV_NS}primary_category").get("term")
                         if entry.find(f"{ARXIV_NS}primary_category") is not None else ""),
        })
    return records


def arxiv_query(text: str) -> str:
    """Plain words become an AND of all: terms; text with a field prefix passes through."""
    if ":" in text:
        return text
    terms = [t for t in text.replace('"', " ").split() if t]
    return " AND ".join(f"all:{t}" for t in terms)


def search_inspire(query: str, n: int, sort: str, timeout: float) -> list[dict]:
    params = {"q": query, "size": n, "sort": sort, "fields": INSPIRE_FIELDS}
    data = _get(f"{INSPIRE_URL}?{urllib.parse.urlencode(params)}", timeout)
    return parse_inspire(json.loads(data))


def search_arxiv(query: str, n: int, sort: str, timeout: float) -> list[dict]:
    sort_by = {"mostrecent": "submittedDate"}.get(sort, "relevance")
    params = {"search_query": arxiv_query(query), "start": 0, "max_results": n,
              "sortBy": sort_by, "sortOrder": "descending"}
    return parse_arxiv(_get(f"{ARXIV_URL}?{urllib.parse.urlencode(params)}", timeout))


def format_record(rec: dict, abstract_chars: int) -> str:
    authors = rec["authors"]
    who = (authors[0] + (" et al." if len(authors) > 1 else "")) if authors else "unknown authors"
    ids = []
    if rec.get("arxiv"):
        ids.append(f"arXiv:{rec['arxiv']}")
    if rec.get("doi"):
        ids.append(f"doi:{rec['doi']}")
    meta = [rec.get("year") or "n.d.", who]
    doc_type = rec.get("doc_type") or ""
    if rec.get("journal"):
        meta.append(rec["journal"])
    elif doc_type and doc_type != "article":
        meta.append(doc_type)  # book, book chapter, conference paper, thesis ...
    else:
        meta.append("preprint (no journal ref)")
    if rec.get("citations") is not None:
        meta.append(f"{rec['citations']} citations")
    lines = [f"- {rec['title']}", f"  {' | '.join(meta)}"]
    if ids:
        lines.append(f"  {' '.join(ids)}")
    if rec.get("url"):
        lines.append(f"  {rec['url']}")
    if abstract_chars and rec.get("abstract"):
        lines.append(f"  abstract: {_clip(rec['abstract'], abstract_chars)}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--source", choices=["both", "inspire", "arxiv"], default="both")
    ap.add_argument("--max", type=int, default=8, help="results per source (default 8)")
    ap.add_argument("--sort", choices=["mostrecent", "mostcited", "relevance"], default="mostcited",
                    help="INSPIRE supports mostcited/mostrecent; arXiv uses relevance/submittedDate")
    ap.add_argument("--abstract-chars", type=int, default=400)
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--json", action="store_true", help="print records as JSON")
    args = ap.parse_args(argv)

    searches = []
    if args.source in ("both", "inspire"):
        inspire_sort = args.sort if args.sort in ("mostrecent", "mostcited") else "mostcited"
        searches.append(("INSPIRE-HEP", lambda: search_inspire(args.query, args.max, inspire_sort, args.timeout)))
    if args.source in ("both", "arxiv"):
        searches.append(("arXiv", lambda: search_arxiv(args.query, args.max, args.sort, args.timeout)))

    answered, all_records = 0, []
    for name, run in searches:
        try:
            records = run()
        except SourceUnavailable as exc:
            print(f"UNAVAILABLE: {name} ({exc}). Fall back to WebSearch and mark ACCESS=snippet.")
            continue
        except (ValueError, ET.ParseError) as exc:
            print(f"UNAVAILABLE: {name} returned an unreadable response ({exc}).")
            continue
        answered += 1
        all_records.extend(records)
        if not args.json:
            print(f"## {name}: {len(records)} result(s) for {args.query!r}")
            for rec in records:
                print(format_record(rec, args.abstract_chars))
    if args.json:
        print(json.dumps(all_records, indent=2, ensure_ascii=False))
    return 0 if answered else 3


if __name__ == "__main__":
    sys.exit(main())
