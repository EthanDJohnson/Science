#!/usr/bin/env python3
"""Print a source's own text, from a PDF or a web page, so agents can quote it verbatim.

WebFetch passes a page through a model and returns its answer, so its wording can drift from
the source. This prints the text itself: PDF text extracted with pypdf, or HTML with the markup
removed. With --grep it prints only the passages around a phrase, which keeps a long paper out
of the agent's context (and its cost). --grep ignores case and whitespace, because PDF extraction
often inserts stray spaces inside words ("bub ble"); --regex takes a regular expression instead.

It also reads a local file under runs/, such as a paper the user supplied in runs/<slug>/user/.

Usage (from the project root):
    python3 .claude/skills/conundrum/scripts/fetch_text.py https://arxiv.org/pdf/gr-qc/9702026 --grep "Planck length"
    python3 .claude/skills/conundrum/scripts/fetch_text.py runs/<slug>/user/paper.pdf --grep "systematic"
    python3 .claude/skills/conundrum/scripts/fetch_text.py <pdf-url> --pages 1-3
    python3 .claude/skills/conundrum/scripts/fetch_text.py https://arxiv.org/abs/gr-qc/0009013 --max-chars 3000

Quote the text as printed and mark it ACCESS: full-text. Whitespace is collapsed to single
spaces; nothing else is changed. When quoting you may close stray spaces inside words, and
nothing else. PDF extraction can also garble equations, ligatures (fi, fl) and hyphenated line
breaks, so don't quote a passage that looks garbled.

Some publishers answer automated requests with a short bot-check page ("Client Challenge", "Just a
moment...") and a 200 status. That page is reported as BLOCKED, not printed as the source: the
paper's arXiv version (INSPIRE lists it) or its lit_search abstract is the way in.

Exit status: 0 on success, 2 if --grep found nothing, 3 if the source was unreachable or blocked,
4 if a PDF needs pypdf (pip install pypdf cffi).
"""
from __future__ import annotations

import argparse
import html
import io
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "conundrum-skill/1.0 (research assistant; low volume)"
MAX_BYTES = 50_000_000


class Unavailable(Exception):
    pass


class NeedsPypdf(Exception):
    pass


class Blocked(Exception):
    """A bot-check page served in place of the source; the message is the host."""


LOCAL_TYPES = {".pdf": "application/pdf", ".html": "text/html", ".htm": "text/html", ".xml": "application/xml"}


def read_local(path: str) -> tuple[bytes, str, str]:
    """A file under runs/ (for example a paper the user supplied): (body, content type, path)."""
    runs = (Path.cwd() / "runs").resolve()
    real = Path(path).resolve()
    if runs not in real.parents:
        raise Unavailable("local files are read only from runs/<slug>/")
    if not real.is_file():
        raise Unavailable("no such file")
    if real.stat().st_size > MAX_BYTES:
        raise Unavailable(f"larger than {MAX_BYTES // 1_000_000} MB")
    return real.read_bytes(), LOCAL_TYPES.get(real.suffix.lower(), "text/plain"), path


def fetch(url: str, timeout: float) -> tuple[bytes, str, str]:
    """Return (body, content type, final URL). A path without a scheme is read from runs/."""
    if "://" not in url:
        return read_local(url)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise Unavailable(f"larger than {MAX_BYTES // 1_000_000} MB")
            return body, resp.headers.get("Content-Type", "") or "", resp.geturl() or url
    except urllib.error.HTTPError as exc:
        raise Unavailable(f"HTTP {exc.code}: {exc.reason}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        reason = str(getattr(exc, "reason", exc))
        if "403" in reason or "Tunnel" in reason:
            reason += (f"; the network policy may not allow {urllib.parse.urlsplit(url).hostname} "
                       "(see README, Network access)")
        raise Unavailable(reason) from exc


def is_pdf(body: bytes, content_type: str) -> bool:
    return body[:5] == b"%PDF-" or "pdf" in content_type.lower()


def pdf_pages(body: bytes) -> list[str]:
    try:
        import logging
        logging.getLogger("pypdf").setLevel(logging.ERROR)
        import pypdf
    except ImportError as exc:
        raise NeedsPypdf("pypdf is not installed: pip install pypdf cffi") from exc
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # a broken cryptography package raises a pyo3 PanicException here
        raise NeedsPypdf(f"pypdf is installed but fails to import ({type(exc).__name__}): pip install cffi") from exc
    reader = pypdf.PdfReader(io.BytesIO(body))
    return [" ".join((page.extract_text() or "").split()) for page in reader.pages]


def html_text(body: bytes, content_type: str) -> str:
    charset = re.search(r"charset=([\w-]+)", content_type or "")
    text = body.decode(charset.group(1) if charset else "utf-8", errors="replace")
    text = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1\s*>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def parse_pages(spec: str, n: int) -> list[int]:
    """'1-3,5' -> [1, 2, 3, 5], 1-based and clipped to the document."""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        lo, _, hi = part.partition("-")
        start, end = int(lo), int(hi) if hi else int(lo)
        pages.extend(p for p in range(start, end + 1) if 1 <= p <= n and p not in pages)
    return pages


# A bot-check or access page: short, and saying so. Real pages are longer: an arXiv abstract page
# extracts to about 4,500 characters, a Springer challenge page to about 230.
CHALLENGE = re.compile(r"client challenge|just a moment|enable javascript|captcha|are you a robot|access denied|"
                       r"verify you are human|checking your browser|unusual traffic", re.I)
SHORT_PAGE = 1500
CHALLENGE_MAX_CHARS = SHORT_PAGE


def blocked(text: str) -> bool:
    """True for a bot-check page served in place of the source."""
    return len(text) < CHALLENGE_MAX_CHARS and bool(CHALLENGE.search(text))


def phrase_pattern(phrase: str) -> str:
    """Match a phrase ignoring case and whitespace, so 'bubble wall' also finds 'bub ble wall'."""
    return r"\s*".join(re.escape(c) for c in phrase if not c.isspace())


def passages(chunks: list[tuple[str, str]], pattern: str, context: int, limit: int) -> list[str]:
    rx = re.compile(pattern, re.I)
    out = []
    for label, text in chunks:
        for m in rx.finditer(text):
            a, b = max(0, m.start() - context), min(len(text), m.end() + context)
            out.append(f"{label}...{text[a:b]}...")
            if len(out) >= limit:
                return out
    return out


# ---------------------------------------------------------------- shared with find_fulltext.py
def load(url: str, timeout: float, pages: str | None = None) -> tuple[list[tuple[str, str]], str, str]:
    """Fetch a source and return (chunks, kind, final URL): chunks are (label, text) pairs, one per PDF page
    or one for a page. Raises Unavailable, Blocked (a bot-check page) or NeedsPypdf."""
    body, content_type, final_url = fetch(url, timeout)
    if is_pdf(body, content_type):
        texts = pdf_pages(body)
        chosen = parse_pages(pages, len(texts)) if pages else list(range(1, len(texts) + 1))
        return ([(f"[p. {p}] ", texts[p - 1]) for p in chosen],
                f"PDF, {len(texts)} page{'s' if len(texts) != 1 else ''}", final_url)
    text = html_text(body, content_type)
    if blocked(text):
        raise Blocked(urllib.parse.urlparse(final_url).netloc)
    return [("", text)], content_type.split(";")[0] or "text", final_url


def add_text_options(ap: argparse.ArgumentParser) -> None:
    ap.add_argument("--grep", help="phrase to find, ignoring case and whitespace; print only the passages around it")
    ap.add_argument("--regex", help="like --grep, but a case-insensitive regular expression")
    ap.add_argument("--context", type=int, default=300, help="characters of context on each side of a match")
    ap.add_argument("--max-matches", type=int, default=10)
    ap.add_argument("--pages", help="PDF pages to use, for example 1-3,5")
    ap.add_argument("--max-chars", type=int, default=20000, help="cap on printed text without --grep")
    ap.add_argument("--timeout", type=float, default=30.0)


def matches(chunks: list[tuple[str, str]], args) -> list[str]:
    """The passages around args.grep (or args.regex)."""
    return passages(chunks, args.regex or phrase_pattern(args.grep), args.context, args.max_matches)


def no_match_note(args, total: int) -> str:
    short = (f" The page is only {total:,} characters: it may be a stub or a landing page, not the paper."
             if total < SHORT_PAGE else "")
    return f"NO MATCH for {(args.regex or args.grep)!r}. Try fewer or different words.{short}"


def print_text(chunks: list[tuple[str, str]], max_chars: int) -> None:
    text = " ".join(label + t for label, t in chunks)
    print(text[:max_chars])
    if len(text) > max_chars:
        print(f"(clipped: {len(text) - max_chars:,} more characters; use --grep or --pages)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    add_text_options(ap)
    args = ap.parse_args(argv)

    try:
        chunks, kind, final_url = load(args.url, args.timeout, args.pages)
    except Blocked as exc:
        print(f"BLOCKED: {exc} served a bot-check page, not the source. For a paper, find_fulltext.py <doi> "
              "finds a free copy (arXiv, a repository manuscript or PubMed Central); otherwise quote the lit_search "
              "abstract. A blocked page makes a claim unverifiable, never contradicted.")
        return 3
    except Unavailable as exc:
        print(f"UNAVAILABLE: {args.url} ({exc}). For a paper, find_fulltext.py <doi> finds a free copy; otherwise "
              "quote an abstract from lit_search.py or mark ACCESS: search-summary.")
        return 3
    except NeedsPypdf as exc:
        print(f"CANNOT READ PDF: {exc}.")
        return 4

    total = sum(len(t) for _, t in chunks)
    print(f"SOURCE: {final_url} | {kind} | {total:,} characters")
    if args.grep or args.regex:
        found = matches(chunks, args)
        if not found:
            print(no_match_note(args, total))
            return 2
        for p in found:
            print(p)
        return 0
    print_text(chunks, args.max_chars)
    return 0


if __name__ == "__main__":
    sys.exit(main())
