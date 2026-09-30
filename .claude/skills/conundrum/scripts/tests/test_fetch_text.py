"""Offline tests for fetch_text.py. A fake urlopen serves a hand-built PDF and HTML page.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import builtins
import contextlib
import importlib.util
import io
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import fetch_text  # noqa: E402

HAVE_PYPDF = importlib.util.find_spec("pypdf") is not None


def minimal_pdf(*page_texts: str) -> bytes:
    """A small valid PDF with one line of Helvetica text per page."""
    n = len(page_texts)
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n))
    objs = {1: b"<< /Type /Catalog /Pages 2 0 R >>",
            2: f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode()}
    font = 3 + 2 * n
    for i, text in enumerate(page_texts):
        page, content = 3 + 2 * i, 4 + 2 * i
        objs[page] = (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 500 144] /Contents {content} 0 R "
                      f"/Resources << /Font << /F1 {font} 0 R >> >> >>").encode()
        stream = b"BT /F1 12 Tf 20 100 Td (" + text.encode() + b") Tj ET"
        objs[content] = b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
    objs[font] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    out, offsets = io.BytesIO(), {}
    out.write(b"%PDF-1.4\n")
    for num in sorted(objs):
        offsets[num] = out.tell()
        out.write(f"{num} 0 obj\n".encode() + objs[num] + b"\nendobj\n")
    xref = out.tell()
    out.write(f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode())
    for num in sorted(objs):
        out.write(f"{offsets[num]:010d} 00000 n \n".encode())
    out.write(f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return out.getvalue()


class FakeResponse:
    def __init__(self, body, content_type, url="https://example.org/paper"):
        self.body, self.url = body, url
        self.headers = {"Content-Type": content_type}

    def read(self, n=-1):
        return self.body if n < 0 else self.body[:n]

    def geturl(self):
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def run(argv, response=None, error=None):
    buf = io.StringIO()
    side = error if error is not None else (lambda *a, **k: response)
    with mock.patch.object(fetch_text.urllib.request, "urlopen", side_effect=side), contextlib.redirect_stdout(buf):
        code = fetch_text.main(argv)
    return code, buf.getvalue()


PDF = minimal_pdf("The bubble wall thickness is a few hundred Planck lengths.",
                  "Page two talks about horizons.")
HTML = (b"<html><head><style>p {color: red}</style><script>var hidden = 'do not print';</script></head>"
        b"<body><h1>Title</h1><p>Energy &amp; momentum are   conserved.</p></body></html>")


@unittest.skipUnless(HAVE_PYPDF, "pypdf not installed")
class Pdf(unittest.TestCase):
    def test_grep_finds_phrase_with_page_label(self):
        code, out = run(["https://x/p.pdf", "--grep", "few hundred Planck", "--context", "10"],
                        FakeResponse(PDF, "application/pdf"))
        self.assertEqual(code, 0)
        self.assertIn("PDF, 2 pages", out)
        self.assertIn("[p. 1] ...", out)
        self.assertIn("few hundred Planck", out)

    def test_grep_ignores_stray_spaces_inside_words(self):
        spaced = minimal_pdf("the bub ble wall thickness")
        code, out = run(["https://x/p.pdf", "--grep", "bubble wall"], FakeResponse(spaced, "application/pdf"))
        self.assertEqual(code, 0)
        self.assertIn("bub ble wall", out)

    def test_no_match_exits_2_and_pages_select(self):
        code, _ = run(["https://x/p.pdf", "--grep", "wormhole"], FakeResponse(PDF, "application/pdf"))
        self.assertEqual(code, 2)
        code, out = run(["https://x/p.pdf", "--pages", "2"], FakeResponse(PDF, "application/octet-stream"))
        self.assertEqual(code, 0)
        self.assertIn("[p. 2] Page two talks about horizons.", out)
        self.assertNotIn("Planck", out)

    def test_missing_or_broken_pypdf_exits_4(self):
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "pypdf":
                raise ImportError("no pypdf")
            return real_import(name, *args, **kwargs)
        with mock.patch.object(builtins, "__import__", side_effect=fake_import):
            code, out = run(["https://x/p.pdf"], FakeResponse(PDF, "application/pdf"))
        self.assertEqual(code, 4)
        self.assertIn("pip install pypdf cffi", out)


class HtmlAndErrors(unittest.TestCase):
    def test_html_is_stripped_and_unescaped(self):
        code, out = run(["https://x/page"], FakeResponse(HTML, "text/html; charset=utf-8"))
        self.assertEqual(code, 0)
        self.assertIn("Title Energy & momentum are conserved.", out)
        self.assertNotIn("do not print", out)
        self.assertNotIn("color: red", out)

    def test_regex_and_clipping(self):
        code, out = run(["https://x/page", "--regex", r"momentum\s+are", "--context", "5"],
                        FakeResponse(HTML, "text/html"))
        self.assertEqual(code, 0)
        self.assertIn("momentum are", out)
        code, out = run(["https://x/page", "--max-chars", "10"], FakeResponse(HTML, "text/html"))
        self.assertIn("(clipped:", out)

    def test_blocked_host_exits_3_with_hint(self):
        err = fetch_text.urllib.error.URLError("Tunnel connection failed: 403 Forbidden")
        code, out = run(["https://api.semanticscholar.org/x"], error=err)
        self.assertEqual(code, 3)
        self.assertIn("may not allow api.semanticscholar.org", out)
        self.assertIn("search-summary", out)

    def test_page_spec_parsing(self):
        self.assertEqual(fetch_text.parse_pages("1-3,5,3,99", 6), [1, 2, 3, 5])


class BotChecks(unittest.TestCase):
    CHALLENGE = (b"<html><body><h1>Client Challenge</h1><p>JavaScript is disabled in your browser. "
                 b"A required part of this site couldn't load.</p></body></html>")

    def test_a_bot_check_page_is_blocked_not_quoted(self):
        code, out = run(["https://doi.org/10.1140/epja/x", "--grep", "pressure"],
                        FakeResponse(self.CHALLENGE, "text/html", url="https://link.springer.com/article/x"))
        self.assertEqual(code, 3)
        self.assertIn("BLOCKED: link.springer.com served a bot-check page", out)
        self.assertIn("never contradicted", out)
        self.assertNotIn("NO MATCH", out)

    def test_a_long_article_that_mentions_captcha_is_not_blocked(self):
        page = b"<html><body><p>" + b"Neutron lifetime measurements with a captcha-free apparatus. " * 200 + b"</p></body></html>"
        code, out = run(["https://x/article", "--grep", "apparatus"], FakeResponse(page, "text/html"))
        self.assertEqual(code, 0)

    def test_no_match_on_a_short_page_says_it_may_be_a_stub(self):
        code, out = run(["https://x/page", "--grep", "lifetime"], FakeResponse(HTML, "text/html"))
        self.assertEqual(code, 2)
        self.assertIn("may be a stub or a landing page", out)


class BotChecksSparePages(unittest.TestCase):
    def test_an_abstract_sized_page_that_mentions_access_denied_is_not_blocked(self):
        text = b"We report a measurement of the neutron lifetime; access denied to the trap region was tested. "
        page = b"<html><body><p>" + text * 45 + b"</p></body></html>"    # about 4,400 characters, like an arXiv abstract page
        code, out = run(["https://arxiv.org/abs/2412.19519", "--grep", "neutron lifetime"], FakeResponse(page, "text/html"))
        self.assertEqual(code, 0)
        self.assertNotIn("BLOCKED", out)



if __name__ == "__main__":
    unittest.main()
