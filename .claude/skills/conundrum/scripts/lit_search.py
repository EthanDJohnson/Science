#!/usr/bin/env python3
"""Literature search for /conundrum researchers (standard library only).

Sources, chosen with --source (a comma-separated list or an alias):
    inspire   INSPIRE-HEP: citation counts and journal refs; best for gr-qc, hep-th, hep-ph.
    arxiv     the arXiv API: physics, maths and CS preprints.
    crossref  Crossref: every DOI-registered journal, conference and book, in all fields.
    s2        Semantic Scholar: all fields, with abstracts, citation counts and open-access PDF links.
    physics   inspire,arxiv (the default; "both" is an alias)
    general   crossref,s2 (engineering, materials, chemistry, statistics, anything outside physics)
    all       all four

It prints compact records a researcher can cite. The abstracts are the papers' own text, so
they can be quoted as ACCESS: abstract. When a source is unreachable (for example under a
restrictive network policy) it says so plainly, so the researcher can fall back to WebSearch
and mark evidence as ACCESS: search-summary.

Results come best match first (--sort relevance, the default). Sorting a plain query by
citations or date brings back famous or merely recent papers that share a word with it, so
use --sort mostcited or mostrecent only with a narrow query, such as an INSPIRE title search.
Crossref and Semantic Scholar rank by relevance only; for them, --sort mostcited or mostrecent
re-sorts a relevance-ranked pool of up to 100 results.

--since YEAR keeps work from that year on, translated for each source: INSPIRE "de>=YEAR"
(earliest date, so a 2024 preprint published in 2025 still counts), arXiv submittedDate,
Crossref from-pub-date, Semantic Scholar year. Prefer it to writing a date into the query.

INSPIRE also takes its own search syntax (t "title words", a author, refersto:arxiv:<id> or
refersto:doi:<doi> for the papers citing one; this script looks up the record INSPIRE needs for
that). The other sources can't read it, so a query that uses it goes to INSPIRE only.

Optional environment variables (nothing identifying is sent unless you set them):
    SEMANTIC_SCHOLAR_API_KEY   sent as the x-api-key header; raises the shared rate limit.
    CROSSREF_MAILTO            an email address for Crossref's faster "polite" pool.

Usage (from the project root):
    python3 .claude/skills/conundrum/scripts/lit_search.py "alcubierre negative energy"
    python3 .claude/skills/conundrum/scripts/lit_search.py "neutron lifetime beam" --since 2024
    python3 .claude/skills/conundrum/scripts/lit_search.py 't "warp drive"' --source inspire --sort mostcited
    python3 .claude/skills/conundrum/scripts/lit_search.py "refersto:arxiv:2412.19519" --source inspire --sort mostrecent
    python3 .claude/skills/conundrum/scripts/lit_search.py "casimir energy density" --source arxiv --max 5 --json
    python3 .claude/skills/conundrum/scripts/lit_search.py "look-elsewhere effect trials factor" --source general

Exit status: 0 if at least one source answered, 3 if every source was unreachable.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

INSPIRE_URL = "https://inspirehep.net/api/literature"
ARXIV_URL = "https://export.arxiv.org/api/query"
CROSSREF_URL = "https://api.crossref.org/works"
S2_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
CROSSREF_SELECT = ",".join([
    "DOI", "title", "author", "issued", "container-title", "type", "is-referenced-by-count",
    "abstract", "URL", "volume", "page",
])
S2_FIELDS = ",".join([
    "title", "authors", "year", "abstract", "externalIds", "journal", "citationCount", "url",
    "publicationTypes", "openAccessPdf",
])
POOL_MAX = 100  # relevance-ranked results fetched before a local re-sort
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


def _get(url: str, timeout: float, retries: int = 2, headers: dict | None = None) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
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
            reason = str(getattr(exc, "reason", exc))
            if "403" in reason or "Tunnel" in reason:
                host = urllib.parse.urlsplit(url).hostname
                reason += f"; the network policy may not allow {host} (see README, Network access)"
            raise SourceUnavailable(reason) from exc
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


CROSSREF_TYPES = {
    "journal-article": "article", "posted-content": "preprint", "proceedings-article": "conference paper",
    "book-chapter": "book chapter", "book": "book", "monograph": "book", "edited-book": "book",
    "report": "report", "dissertation": "thesis", "dataset": "dataset", "standard": "standard",
}


def strip_markup(text: str) -> str:
    """Crossref abstracts are JATS XML; keep the words, drop the tags and a leading 'Abstract'."""
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text or "")).split())
    return re.sub(r"^(Abstract|ABSTRACT)[\s.:]+", "", text)


def parse_crossref(payload: dict) -> list[dict]:
    records = []
    for it in payload.get("message", {}).get("items", []):
        doi = it.get("DOI", "")
        parts = (it.get("issued") or {}).get("date-parts") or [[None]]
        year = str(parts[0][0]) if parts and parts[0] and parts[0][0] else ""
        kind = it.get("type", "")
        container = (it.get("container-title") or [""])[0]
        journal = "" if kind == "posted-content" else " ".join(
            str(p) for p in (container, it.get("volume"), it.get("page")) if p)
        authors = [" ".join(p for p in (a.get("given"), a.get("family")) if p) or a.get("name", "")
                   for a in it.get("author", [])]
        records.append({
            "source": "crossref",
            "title": " ".join(((it.get("title") or [""])[0]).split()),
            "authors": authors,
            "year": year,
            "arxiv": "",
            "doi": doi,
            "journal": journal,
            "doc_type": CROSSREF_TYPES.get(kind, kind.replace("-", " ")),
            "citations": it.get("is-referenced-by-count"),
            "url": f"https://doi.org/{doi}" if doi else it.get("URL", ""),
            "abstract": strip_markup(it.get("abstract", "")),
        })
    return records


def parse_s2(payload: dict) -> list[dict]:
    records = []
    for p in payload.get("data", []) or []:
        ext = p.get("externalIds") or {}
        j = p.get("journal") or {}
        name = (j.get("name") or "").strip()
        journal = "" if not name or "arxiv" in name.lower() else " ".join(
            str(x).strip() for x in (name, j.get("volume"), j.get("pages")) if x and str(x).strip())
        types = p.get("publicationTypes") or []
        doc_type = next((label for key, label in (("Review", "review"), ("Conference", "conference paper"),
                                                   ("Book", "book"), ("JournalArticle", "article"))
                          if key in types), "")
        records.append({
            "source": "s2",
            "title": " ".join((p.get("title") or "").split()),
            "authors": [a.get("name", "") for a in p.get("authors") or []],
            "year": str(p.get("year") or ""),
            "arxiv": ext.get("ArXiv", ""),
            "doi": ext.get("DOI", ""),
            "journal": journal,
            "doc_type": doc_type,
            "citations": p.get("citationCount"),
            "url": p.get("url") or "",
            "abstract": p.get("abstract") or "",
            "open_access_pdf": (p.get("openAccessPdf") or {}).get("url") or "",
        })
    return records


def rank(records: list[dict], sort: str, n: int) -> list[dict]:
    """Re-sort a relevance-ranked pool locally (stable, so ties keep relevance order)."""
    if sort == "mostcited":
        records = sorted(records, key=lambda r: -(r.get("citations") or 0))
    elif sort == "mostrecent":
        records = sorted(records, key=lambda r: -int(r["year"]) if r.get("year", "").isdigit() else 0)
    return records[:n]


def arxiv_query(text: str) -> str:
    """Plain words become an AND of all: terms; text with a field prefix passes through."""
    if ":" in text:
        return text
    terms = [t for t in text.replace('"', " ").split() if t]
    return " AND ".join(f"all:{t}" for t in terms)


# INSPIRE's own syntax that no other source can read: citation operators, date comparisons, and a
# leading field keyword followed by a quoted phrase (t "...", a "...").
INSPIRE_ONLY = re.compile(r'\b(refersto|citedby|exactauthor|collaboration|texkey|recid|cn)\s*:|\btopcite\s+\d|'
                          r'\b(date|de|du|year)\s*[<>]|(^|\b(and|or)\s+)(t|a|j|k|ti|au|title|author)\s+"', re.I)
# INSPIRE sorts: its relevance ranking is called bestmatch.
INSPIRE_SORT = {"relevance": "bestmatch", "mostcited": "mostcited", "mostrecent": "mostrecent"}


# INSPIRE answers refersto: only for a record ID; refersto:arxiv:<id> is silently ignored.
REFERSTO = re.compile(r"\brefersto:(arxiv|eprint|doi):(\S+)", re.I)


class NotFound(Exception):
    """An identifier INSPIRE has no record for: a wrong ID, not a source that is down."""


def resolve_refersto(query: str, timeout: float) -> str:
    """Rewrite refersto:arxiv:<id> or refersto:doi:<doi> as refersto:recid:<n>, the form INSPIRE answers.
    An arXiv version suffix (v2) and an arXiv: prefix are dropped, and a closing parenthesis that
    belongs to the query rather than the identifier is kept outside it."""
    def recid(match: re.Match) -> str:
        kind = "doi" if match.group(1).lower() == "doi" else "arxiv"
        ident, tail = match.group(2), ""
        while ident.endswith(")") and ident.count(")") > ident.count("("):
            ident, tail = ident[:-1], ")" + tail
        if kind == "arxiv":
            ident = re.sub(r"v\d+$", "", re.sub(r"(?i)^arxiv:", "", ident))
        params = {"q": f"{kind}:{ident}", "size": 1, "fields": "control_number"}
        hits = json.loads(_get(f"{INSPIRE_URL}?{urllib.parse.urlencode(params)}", timeout)).get("hits", {}).get("hits", [])
        if not hits:
            raise NotFound(f"INSPIRE has no record for {kind}:{ident}; check the identifier")
        return f"refersto:recid:{hits[0]['metadata']['control_number']}{tail}"
    return REFERSTO.sub(recid, query)


def search_inspire(query: str, n: int, sort: str, timeout: float, since: int | None = None) -> list[dict]:
    query = resolve_refersto(query, timeout) if REFERSTO.search(query) else query
    q = f"({query}) and de>={since}" if since else query   # parentheses keep an "or" inside the filter
    params = {"q": q, "size": n, "sort": INSPIRE_SORT.get(sort, sort), "fields": INSPIRE_FIELDS}
    data = _get(f"{INSPIRE_URL}?{urllib.parse.urlencode(params)}", timeout)
    return parse_inspire(json.loads(data))


def search_arxiv(query: str, n: int, sort: str, timeout: float, since: int | None = None) -> list[dict]:
    sort_by = {"mostrecent": "submittedDate"}.get(sort, "relevance")
    q = arxiv_query(query)
    if since:
        q = f"({q}) AND submittedDate:[{since}01010000 TO 209912312359]"
    params = {"search_query": q, "start": 0, "max_results": n,
              "sortBy": sort_by, "sortOrder": "descending"}
    return parse_arxiv(_get(f"{ARXIV_URL}?{urllib.parse.urlencode(params)}", timeout))


def search_crossref(query: str, n: int, sort: str, timeout: float, since: int | None = None) -> list[dict]:
    pool = n if sort == "relevance" else min(POOL_MAX, max(n, 5 * n))
    params = {"query": query, "rows": pool, "select": CROSSREF_SELECT}
    if since:
        params["filter"] = f"from-pub-date:{since}-01-01"
    if os.environ.get("CROSSREF_MAILTO"):
        params["mailto"] = os.environ["CROSSREF_MAILTO"]
    data = _get(f"{CROSSREF_URL}?{urllib.parse.urlencode(params)}", timeout)
    return rank(parse_crossref(json.loads(data)), sort, n)


def search_s2(query: str, n: int, sort: str, timeout: float, since: int | None = None) -> list[dict]:
    pool = n if sort == "relevance" else min(POOL_MAX, max(n, 5 * n))
    params = {"query": query, "limit": pool, "fields": S2_FIELDS}
    if since:
        params["year"] = f"{since}-"
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    data = _get(f"{S2_URL}?{urllib.parse.urlencode(params)}", timeout, headers={"x-api-key": key} if key else None)
    return rank(parse_s2(json.loads(data)), sort, n)


SOURCES = {
    "inspire": "INSPIRE-HEP",
    "arxiv": "arXiv",
    "crossref": "Crossref",
    "s2": "Semantic Scholar",
}
SOURCE_SETS = {
    "physics": ["inspire", "arxiv"],
    "both": ["inspire", "arxiv"],
    "general": ["crossref", "s2"],
    "all": ["inspire", "arxiv", "crossref", "s2"],
}


def parse_sources(text: str) -> list[str]:
    """'physics', 'all', 'general', or a comma-separated list such as 'inspire,s2'."""
    chosen = []
    for part in (p.strip().lower() for p in text.split(",") if p.strip()):
        for key in SOURCE_SETS.get(part, [part]):
            if key not in SOURCES:
                raise argparse.ArgumentTypeError(
                    f"unknown source {part!r}; choose from {', '.join([*SOURCES, *SOURCE_SETS])}")
            if key not in chosen:
                chosen.append(key)
    if not chosen:
        raise argparse.ArgumentTypeError("no source given")
    return chosen


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
    if rec.get("open_access_pdf"):
        lines.append(f"  open-access PDF: {rec['open_access_pdf']}")
    if abstract_chars and rec.get("abstract"):
        lines.append(f"  abstract: {_clip(rec['abstract'], abstract_chars)}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--source", type=parse_sources, default="physics",
                    help="physics (default: inspire,arxiv), general (crossref,s2), all, or a comma-separated list")
    ap.add_argument("--max", type=int, default=8, help="results per source (default 8)")
    ap.add_argument("--sort", choices=["relevance", "mostrecent", "mostcited"], default="relevance",
                    help="best match first (default); INSPIRE sorts server-side; arXiv by relevance or date; "
                         "Crossref and Semantic Scholar re-sort a relevance-ranked pool")
    ap.add_argument("--since", type=int, metavar="YEAR", help="only work from this year on, filtered by each source")
    ap.add_argument("--abstract-chars", type=int, default=400)
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--json", action="store_true", help="print records as JSON")
    args = ap.parse_args(argv)
    if args.since is not None and not 1900 <= args.since <= 2100:
        ap.error("--since takes a four-digit year")

    runners = {
        "inspire": lambda: search_inspire(args.query, args.max, args.sort, args.timeout, args.since),
        "arxiv": lambda: search_arxiv(args.query, args.max, args.sort, args.timeout, args.since),
        "crossref": lambda: search_crossref(args.query, args.max, args.sort, args.timeout, args.since),
        "s2": lambda: search_s2(args.query, args.max, args.sort, args.timeout, args.since),
    }
    sources = args.source if isinstance(args.source, list) else parse_sources(args.source)
    inspire_only = bool(INSPIRE_ONLY.search(args.query))
    searches = []
    for key in sources:
        if inspire_only and key != "inspire":
            print(f"SKIPPED: {SOURCES[key]} can't read INSPIRE search syntax; ask it in plain words "
                  "(use --since for dates).")
            continue
        searches.append((SOURCES[key], runners[key]))
    since_note = f" (since {args.since})" if args.since else ""

    answered, all_records = 0, []
    for name, run in searches:
        try:
            records = run()
        except SourceUnavailable as exc:
            print(f"UNAVAILABLE: {name} ({exc}). Fall back to WebSearch and mark ACCESS: search-summary.")
            continue
        except NotFound as exc:
            answered += 1   # the source answered: the identifier was wrong
            print(f"NOT FOUND: {exc}.")
            continue
        except (ValueError, ET.ParseError) as exc:
            print(f"UNAVAILABLE: {name} returned an unreadable response ({exc}).")
            continue
        answered += 1
        all_records.extend(records)
        if not args.json:
            print(f"## {name}: {len(records)} result(s) for {args.query!r}{since_note}")
            for rec in records:
                print(format_record(rec, args.abstract_chars))
            if not records and name == SOURCES["inspire"]:
                print("  INSPIRE found nothing. It reads some leading words as search fields (a, t, j, k, d ...), "
                      "and hyphenated names need quotes (\"J-PARC\"): try fewer, distinctive words, or reorder them.")
    if args.json:
        print(json.dumps(all_records, indent=2, ensure_ascii=False))
    return 0 if answered else 3


if __name__ == "__main__":
    sys.exit(main())
