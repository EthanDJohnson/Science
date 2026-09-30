#!/usr/bin/env python3
"""Find a free, legal full text of a paper from its DOI or arXiv ID, and search it.

Publisher pages are often paywalled or behind a bot check. Most physics papers also exist as a
free copy: the arXiv preprint, an accepted manuscript in a lab or university repository (US
national-lab work is in OSTI), or an open-access copy in PubMed Central. This asks free indexes
for them and lists what it finds, best first:

    INSPIRE-HEP       the arXiv ID of a physics paper
    OpenAlex          open-access copies of any paper, with their version
    OSTI              manuscripts of US Department of Energy work (DOE PAGES)
    Europe PMC        open-access full text from PubMed Central
    Unpaywall         like OpenAlex; used only when UNPAYWALL_EMAIL is set, since it requires an address
    Semantic Scholar  open-access PDF links; asked only when nothing else found a copy

With --grep (or --regex) it opens the best copy it can reach and prints the passages around the
phrase. It moves on to the next copy when one is blocked, unreachable or lacks the phrase. With
--text it prints the text instead.

Versions matter. A preprint (the submitted version) can differ from the published paper, and
numbers sometimes change. So the best copy is the published version where one is free, then the
accepted manuscript, then the preprint. arXiv's latest version is often the accepted one, but
not always. Say in SOURCE which version you quoted, and check a number taken from a preprint
against the published abstract, which lit_search.py prints.

It never contacts authors or anyone else: it only reads public indexes and free copies. When no
free copy exists and the answer may turn on the paper, it says how to flag the paper for the
user, who can request it from its authors.

Usage (from the project root):
    python3 .claude/skills/conundrum/scripts/find_fulltext.py 10.1103/PhysRevLett.111.222501
    python3 .claude/skills/conundrum/scripts/find_fulltext.py https://doi.org/10.1103/nr3b-3dtl --grep "charge exchange"
    python3 .claude/skills/conundrum/scripts/find_fulltext.py arXiv:2412.19519 --grep "systematic" --max-matches 5
    python3 .claude/skills/conundrum/scripts/find_fulltext.py 10.1103/PhysRevLett.127.162501 --text --pages 1-2

Optional environment variables (nothing identifying is sent unless you set them):
    UNPAYWALL_EMAIL           turns on Unpaywall, which requires a contact address
    OPENALEX_MAILTO           an address for OpenAlex's polite pool (CROSSREF_MAILTO is used if set)
    SEMANTIC_SCHOLAR_API_KEY  raises Semantic Scholar's shared rate limit

Exit status: 0 on success; 1 if the identifier can't be read; 2 if --grep found nothing in any
copy it opened; 3 if no free copy was found or none could be opened; 4 if a PDF needs pypdf.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse

import fetch_text
import lit_search

OPENALEX_URL = "https://api.openalex.org/works/doi:{doi}"
OSTI_URL = "https://www.osti.gov/api/v1/records"
EUROPEPMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EUROPEPMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
UNPAYWALL_URL = "https://api.unpaywall.org/v2/{doi}"
S2_URL = "https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"

# Best first. arXiv's latest version is labelled submitted: it is often, not always, the accepted one.
VERSION_RANK = {"published": 0, "accepted": 1, "submitted": 2, "unknown": 3}
VERSION_LABEL = {
    "published": "published version",
    "accepted": "accepted manuscript",
    "submitted": "preprint (submitted version)",
    "unknown": "version not stated",
}
MAX_TRIES = 4

NEW_ARXIV = r"\d{4}\.\d{4,5}"
OLD_ARXIV = r"[a-z][a-z\-]*(?:\.[A-Z]{2})?/\d{7}"
ARXIV_ID = re.compile(rf"^(?:arxiv:)?({NEW_ARXIV}|{OLD_ARXIV})(v\d+)?$", re.I)
ARXIV_URL = re.compile(rf"arxiv\.org/(?:abs|pdf)/({NEW_ARXIV}|{OLD_ARXIV})(v\d+)?(?:\.pdf)?(?:[?#]|$)", re.I)
ARXIV_DOI = re.compile(rf"^10\.48550/arxiv\.({NEW_ARXIV}|{OLD_ARXIV})$", re.I)
DOI = re.compile(r"10\.\d{4,9}/[^\s\"<>]+")


class BadIdentifier(ValueError):
    pass


def _balanced(text: str) -> str:
    """Drop trailing punctuation that belongs to the surrounding text, keeping a DOI's own parentheses."""
    text = text.rstrip(".,;:'\"]")
    while text.endswith(")") and text.count(")") > text.count("("):
        text = text[:-1].rstrip(".,;:")
    return text


def parse_identifier(text: str) -> tuple[str | None, str | None]:
    """(doi, arxiv_id) from a DOI, an arXiv ID, or a URL containing either. The arXiv ID keeps no version."""
    raw = urllib.parse.unquote(text.strip())
    m = ARXIV_ID.match(raw) or ARXIV_URL.search(raw)
    if m:
        return None, m.group(1)
    m = DOI.search(raw)
    if m:
        doi = _balanced(m.group(0))
        arx = ARXIV_DOI.match(doi)
        return (None, arx.group(1)) if arx else (doi, None)
    raise BadIdentifier(f"no DOI or arXiv ID in {text!r}: give a DOI (10.xxxx/...), an arXiv ID, or a URL "
                        "containing one (lit_search.py prints the DOI)")


def arxiv_pdf(arxiv_id: str) -> str:
    return f"https://arxiv.org/pdf/{arxiv_id}"


def arxiv_in(url: str) -> str | None:
    """The arXiv ID an arXiv URL or arXiv DOI points to, if it is one."""
    m = ARXIV_URL.search(url or "")
    if m:
        return m.group(1)
    m = re.search(rf"10\.48550/arxiv\.({NEW_ARXIV}|{OLD_ARXIV})", url or "", re.I)
    return m.group(1) if m else None


def _version(value: str | None) -> str:
    v = (value or "").lower()
    for key in ("published", "accepted", "submitted"):
        if v.startswith(key):
            return key
    return "unknown"


class Finder:
    """Collects free copies from the indexes, merging duplicates."""

    def __init__(self, timeout: float):
        self.timeout = timeout
        self.copies: dict[str, dict] = {}
        self.checked: dict[str, str] = {}
        self.paper: dict = {}

    # ------------------------------------------------------------ bookkeeping
    def add(self, url: str, version: str, host: str, found_by: str, kind: str = "pdf", license: str | None = None):
        if not url:
            return
        arx = arxiv_in(url)
        if arx:
            url, version, host, kind = arxiv_pdf(arx), "submitted", "arXiv (latest version)", "pdf"
            self.paper.setdefault("arxiv", arx)
        key = url.rstrip("/").lower()
        copy = self.copies.get(key)
        if copy is None:
            self.copies[key] = {"url": url, "version": version, "host": host, "kind": kind,
                                "license": license, "found_by": [found_by]}
            return
        if found_by not in copy["found_by"]:
            copy["found_by"].append(found_by)
        if VERSION_RANK[version] < VERSION_RANK[copy["version"]]:
            copy["version"] = version
        copy["license"] = copy["license"] or license

    def ranked(self) -> list[dict]:
        kind_rank = {"pdf": 0, "xml": 0, "page": 1}
        return sorted(self.copies.values(), key=lambda c: (kind_rank[c["kind"]], VERSION_RANK[c["version"]]))

    def _json(self, url: str, headers: dict | None = None):
        return json.loads(lit_search._get(url, self.timeout, headers=headers))

    def _ask(self, name: str, fn) -> None:
        try:
            note = fn()
            self.checked[name] = note or "ok"
        except lit_search.SourceUnavailable as exc:
            self.checked[name] = "no record" if "HTTP 404" in str(exc) else f"unavailable ({exc})"
        except (ValueError, KeyError, TypeError) as exc:
            self.checked[name] = f"unreadable answer ({type(exc).__name__})"

    # ------------------------------------------------------------ the indexes
    def inspire(self, doi: str | None, arxiv_id: str | None) -> str | None:
        query = f"doi:{doi}" if doi else f"arxiv:{arxiv_id}"
        hits = lit_search.search_inspire(query, 1, "relevance", self.timeout)
        if not hits:
            return "no record"
        rec = hits[0]
        for key in ("title", "year", "journal"):
            if rec.get(key):
                self.paper.setdefault(key, rec[key])
        if rec.get("doi"):
            self.paper.setdefault("doi", rec["doi"])
        if rec.get("arxiv"):
            self.add(arxiv_pdf(rec["arxiv"]), "submitted", "arXiv", "INSPIRE")
        return None

    def openalex(self, doi: str) -> str | None:
        mailto = os.environ.get("OPENALEX_MAILTO") or os.environ.get("CROSSREF_MAILTO")
        url = OPENALEX_URL.format(doi=urllib.parse.quote(doi, safe="/()"))
        work = self._json(url + (f"?{urllib.parse.urlencode({'mailto': mailto})}" if mailto else ""))
        self.paper.setdefault("title", work.get("title"))
        self.paper.setdefault("year", str(work.get("publication_year") or ""))
        found = 0
        for loc in work.get("locations") or []:
            if not loc.get("is_oa"):
                continue
            source = (loc.get("source") or {}).get("display_name") or "unnamed source"
            pdf, page = loc.get("pdf_url"), loc.get("landing_page_url")
            self.add(pdf or page, _version(loc.get("version")), source, "OpenAlex",
                     kind="pdf" if pdf else "page", license=loc.get("license"))
            found += 1
        return None if found else f"no free copy ({(work.get('open_access') or {}).get('oa_status', 'closed')})"

    def osti(self, doi: str) -> str | None:
        records = self._json(f"{OSTI_URL}?{urllib.parse.urlencode({'doi': doi})}")
        for rec in records if isinstance(records, list) else []:
            if (rec.get("doi") or "").lower() != doi.lower():
                continue
            for link in rec.get("links") or []:
                if link.get("rel") == "fulltext":
                    # DOE PAGES holds the accepted manuscript, or the published article when it is open.
                    self.add(link.get("href"), "accepted", "OSTI (DOE PAGES)", "OSTI")
                    return None
        return "no record"

    def europepmc(self, doi: str) -> str | None:
        params = {"query": f'DOI:"{doi}"', "format": "json", "resultType": "lite", "pageSize": 3}
        results = self._json(f"{EUROPEPMC_URL}?{urllib.parse.urlencode(params)}").get("resultList", {}).get("result", [])
        for rec in results:
            if (rec.get("doi") or "").lower() == doi.lower() and rec.get("pmcid") and rec.get("isOpenAccess") == "Y":
                # The XML full text is served for the open-access subset; the PDF links refuse scripts.
                self.add(EUROPEPMC_FULLTEXT.format(pmcid=rec["pmcid"]), "published", "Europe PMC (PubMed Central)",
                         "Europe PMC", kind="xml")
                return None
        return "no open-access copy"

    def unpaywall(self, doi: str, email: str) -> str | None:
        url = UNPAYWALL_URL.format(doi=urllib.parse.quote(doi, safe="/()"))
        data = self._json(f"{url}?{urllib.parse.urlencode({'email': email})}")
        locs = data.get("oa_locations") or []
        for loc in locs:
            host = loc.get("repository_institution") or ("publisher" if loc.get("host_type") == "publisher" else "repository")
            pdf = loc.get("url_for_pdf")
            self.add(pdf or loc.get("url"), _version(loc.get("version")), host, "Unpaywall",
                     kind="pdf" if pdf else "page", license=loc.get("license"))
        return None if locs else "no free copy"

    def semantic_scholar(self, doi: str) -> str | None:
        key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        url = S2_URL.format(doi=urllib.parse.quote(doi, safe="/()")) + "?fields=title,year,openAccessPdf,externalIds"
        data = self._json(url, headers={"x-api-key": key} if key else None)
        self.paper.setdefault("title", data.get("title"))
        if (data.get("externalIds") or {}).get("ArXiv"):
            self.add(arxiv_pdf(data["externalIds"]["ArXiv"]), "submitted", "arXiv", "Semantic Scholar")
        oa = data.get("openAccessPdf") or {}
        if oa.get("url"):
            status = (oa.get("status") or "").upper()
            version = "published" if status in ("GOLD", "HYBRID", "BRONZE") else "unknown"
            self.add(oa["url"], version, "open-access PDF", "Semantic Scholar", license=oa.get("license"))
        return None if (oa.get("url") or (data.get("externalIds") or {}).get("ArXiv")) else "no free copy"

    def run(self, doi: str | None, arxiv_id: str | None) -> None:
        if arxiv_id:
            self.paper["arxiv"] = arxiv_id
            self.add(arxiv_pdf(arxiv_id), "submitted", "arXiv", "the identifier")
        self._ask("INSPIRE", lambda: self.inspire(doi, arxiv_id))
        doi = doi or self.paper.get("doi")
        if doi:
            self.paper["doi"] = doi
        if not doi:
            for name in ("OpenAlex", "OSTI", "Europe PMC", "Unpaywall", "Semantic Scholar"):
                self.checked[name] = "skipped (no DOI)"
            return
        self._ask("OpenAlex", lambda: self.openalex(doi))
        self._ask("OSTI", lambda: self.osti(doi))
        self._ask("Europe PMC", lambda: self.europepmc(doi))
        email = os.environ.get("UNPAYWALL_EMAIL")
        if email:
            self._ask("Unpaywall", lambda: self.unpaywall(doi, email))
        else:
            self.checked["Unpaywall"] = "off (set UNPAYWALL_EMAIL to use it)"
        if self.copies:
            self.checked["Semantic Scholar"] = "skipped (a copy was already found)"
        else:
            self._ask("Semantic Scholar", lambda: self.semantic_scholar(doi))


# ---------------------------------------------------------------- output
def paper_line(paper: dict) -> str:
    parts = [paper.get("title") or "title unknown"]
    parts += [p for p in (paper.get("year"), paper.get("journal")) if p]
    if paper.get("doi"):
        parts.append(f"doi:{paper['doi']}")
    if paper.get("arxiv"):
        parts.append(f"arXiv:{paper['arxiv']}")
    return "PAPER: " + " | ".join(str(p) for p in parts)


def describe(copy: dict) -> str:
    label = VERSION_LABEL[copy["version"]]
    if copy["host"].startswith("arXiv"):
        label = "preprint, latest arXiv version (often the accepted manuscript; not always)"
    kind = " (landing page; may not hold the full text)" if copy["kind"] == "page" else ""
    lic = f", {copy['license']}" if copy.get("license") else ""
    return f"{label}, {copy['host']}{lic}{kind}"


def identity(paper: dict) -> str:
    return f"doi:{paper['doi']}" if paper.get("doi") else f"arXiv:{paper.get('arxiv')}"


def request_advice(paper: dict) -> str:
    return ("Quote the abstract lit_search.py prints (ACCESS: abstract). If the answer may turn on this paper's full "
            "text, list it under Gaps in your notes as "
            f"'PAPER TO REQUEST: {identity(paper)} | <title> | <what it would settle>'. The user sees these at the "
            "checkpoint and can ask the authors for a copy. Never contact anyone yourself.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("identifier", help="a DOI, an arXiv ID, or a URL containing one")
    fetch_text.add_text_options(ap)
    ap.add_argument("--text", action="store_true", help="print the best copy's text (capped by --max-chars)")
    ap.add_argument("--json", action="store_true", help="print the paper and its free copies as JSON")
    args = ap.parse_args(argv)
    try:
        doi, arxiv_id = parse_identifier(args.identifier)
    except BadIdentifier as exc:
        print(f"ERROR: {exc}.")
        return 1

    finder = Finder(args.timeout)
    finder.run(doi, arxiv_id)
    copies = finder.ranked()
    if args.json:
        print(json.dumps({"paper": finder.paper, "copies": copies, "checked": finder.checked}, indent=2))
        return 0 if copies else 3

    print(paper_line(finder.paper))
    checked = "; ".join(f"{name} {note}" for name, note in finder.checked.items())
    if not copies:
        print(f"Checked: {checked}.")
        print(f"NO FREE COPY FOUND for {identity(finder.paper)}. {request_advice(finder.paper)}")
        return 3
    if not (args.grep or args.regex or args.text):
        print("FREE COPIES, best first:")
        for i, copy in enumerate(copies, 1):
            print(f"  {i}. {describe(copy)}\n     {copy['url']}   [found by {', '.join(copy['found_by'])}]")
        print(f"Checked: {checked}.")
        print('Next: add --grep "<phrase>" to search the best copy you can open, or --text to print it.')
        return 0

    opened, needs_pypdf = 0, None
    trying = copies[:MAX_TRIES]
    for copy in trying:
        try:
            chunks, kind, final_url = fetch_text.load(copy["url"], args.timeout, args.pages)
        except fetch_text.Blocked as exc:
            print(f"SKIPPED: {copy['url']} ({exc} served a bot-check page)")
            continue
        except fetch_text.Unavailable as exc:
            print(f"SKIPPED: {copy['url']} ({exc})")
            continue
        except fetch_text.NeedsPypdf as exc:
            needs_pypdf = str(exc)
            print(f"SKIPPED: {copy['url']} (a PDF, and {exc})")
            continue
        opened += 1
        total = sum(len(t) for _, t in chunks)
        print(f"SOURCE: {final_url} | {kind} | {total:,} characters | VERSION: {describe(copy)} | "
              f"OF: {identity(finder.paper)}")
        if args.text:
            fetch_text.print_text(chunks, args.max_chars)
            return 0
        found = fetch_text.matches(chunks, args)
        if found:
            for passage in found:
                print(passage)
            return 0
        print(fetch_text.no_match_note(args, total) + (" Trying the next copy." if copy is not trying[-1] else ""))
    if opened:
        print(f"NO MATCH for {(args.regex or args.grep)!r} in the {opened} free cop{'y' if opened == 1 else 'ies'} opened.")
        return 2
    if needs_pypdf:
        print(f"CANNOT READ PDF: {needs_pypdf}.")
        return 4
    print(f"Checked: {checked}.")
    print(f"NO FREE COPY COULD BE OPENED for {identity(finder.paper)}. {request_advice(finder.paper)}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
