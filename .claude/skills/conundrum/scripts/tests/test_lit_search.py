"""Tests for lit_search.py using synthetic responses shaped like the real APIs.

The fixture values are illustrative; the tests check parsing, formatting and failure
handling, not bibliographic facts. No network access is needed.
"""
import contextlib
import io
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lit_search  # noqa: E402

INSPIRE_FIXTURE = {
    "hits": {
        "total": 2,
        "hits": [
            {"id": "111", "metadata": {
                "control_number": 111,
                "titles": [{"title": "A warp drive paper"}],
                "authors": [{"full_name": "Doe, Jane"}, {"full_name": "Roe, Rick"}],
                "abstracts": [{"value": "We show   that the energy\n conditions are violated."}],
                "arxiv_eprints": [{"value": "gr-qc/0000001"}],
                "dois": [{"value": "10.0000/example.1"}],
                "citation_count": 42,
                "publication_info": [{"journal_title": "Class.Quant.Grav.", "journal_volume": "11",
                                      "page_start": "L73", "year": 1994}],
                "earliest_date": "1994-05-01"}},
            {"id": "222", "metadata": {
                "control_number": 222,
                "titles": [{"title": "An unpublished preprint"}],
                "authors": [{"full_name": "Solo, Sam"}],
                "earliest_date": "2025-01-15"}},
        ],
    }
}

ARXIV_FIXTURE = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2101.00001v2</id>
    <published>2021-01-02T00:00:00Z</published>
    <title>Positive-energy
      warp shells</title>
    <summary>  A subluminal shell satisfying the weak energy condition.  </summary>
    <author><name>Ada Example</name></author>
    <author><name>Bo Example</name></author>
    <arxiv:doi>10.0000/example.2</arxiv:doi>
    <arxiv:journal_ref>Class. Quantum Grav. 38 105009 (2021)</arxiv:journal_ref>
    <arxiv:primary_category term="gr-qc" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
</feed>
"""

CROSSREF_FIXTURE = {
    "status": "ok",
    "message": {"items": [
        {"DOI": "10.0000/example.3", "title": ["A  journal   article"], "type": "journal-article",
         "author": [{"given": "Ada", "family": "Example"}, {"name": "The Collaboration"}],
         "issued": {"date-parts": [[2019, 4, 2]]}, "container-title": ["Phys. Rev. D"],
         "volume": "99", "page": "084001", "is-referenced-by-count": 12,
         "abstract": "<jats:title>Abstract</jats:title><jats:p>Energy &amp; momentum <jats:italic>are</jats:italic> conserved.</jats:p>"},
        {"DOI": "10.0000/example.4", "title": ["A posted preprint"], "type": "posted-content",
         "author": [{"family": "Solo"}], "issued": {"date-parts": [[2024]]},
         "container-title": ["Some Server"], "is-referenced-by-count": 3},
        {"DOI": "10.0000/example.5", "title": ["An old classic"], "type": "journal-article",
         "issued": {"date-parts": [[None]]}, "container-title": ["J. Old"], "is-referenced-by-count": 500},
    ]},
}

S2_FIXTURE = {
    "total": 3, "offset": 0,
    "data": [
        {"paperId": "p1", "title": "Relevant but young", "year": 2023, "citationCount": 4,
         "authors": [{"name": "A. Author"}], "externalIds": {"DOI": "10.0000/example.6", "ArXiv": "2301.00001"},
         "journal": {"name": "Class. Quantum Grav.", "volume": "40", "pages": " 105009 "},
         "publicationTypes": ["JournalArticle"], "url": "https://www.semanticscholar.org/paper/p1",
         "abstract": "A relevant abstract.", "openAccessPdf": {"url": "https://arxiv.org/pdf/2301.00001", "status": "GREEN"}},
        {"paperId": "p2", "title": "Highly cited review", "year": 2010, "citationCount": 900,
         "authors": [], "externalIds": {}, "journal": {"name": "Rev. Mod. Phys."},
         "publicationTypes": ["Review", "JournalArticle"], "url": "https://www.semanticscholar.org/paper/p2",
         "abstract": None, "openAccessPdf": {"url": "", "status": None}},
        {"paperId": "p3", "title": "An arXiv-only preprint", "year": 2025, "citationCount": None,
         "authors": [{"name": "B. Writer"}], "externalIds": {"ArXiv": "2501.00002"},
         "journal": {"name": "arXiv.org"}, "publicationTypes": None, "url": "", "abstract": "Short.",
         "openAccessPdf": None},
    ],
}


class Parsing(unittest.TestCase):
    def test_parse_inspire_full_record(self):
        rec = lit_search.parse_inspire(INSPIRE_FIXTURE)[0]
        self.assertEqual(rec["title"], "A warp drive paper")
        self.assertEqual(rec["authors"], ["Doe, Jane", "Roe, Rick"])
        self.assertEqual(rec["year"], "1994")
        self.assertEqual(rec["arxiv"], "gr-qc/0000001")
        self.assertEqual(rec["journal"], "Class.Quant.Grav. 11 L73")
        self.assertEqual(rec["citations"], 42)
        self.assertEqual(rec["url"], "https://inspirehep.net/literature/111")

    def test_parse_inspire_sparse_record(self):
        rec = lit_search.parse_inspire(INSPIRE_FIXTURE)[1]
        self.assertEqual(rec["year"], "2025")
        self.assertEqual(rec["journal"], "")
        self.assertEqual(rec["arxiv"], "")
        self.assertIsNone(rec["citations"])

    def test_parse_arxiv(self):
        rec = lit_search.parse_arxiv(ARXIV_FIXTURE)[0]
        self.assertEqual(rec["title"], "Positive-energy warp shells")
        self.assertEqual(rec["arxiv"], "2101.00001v2")
        self.assertEqual(rec["year"], "2021")
        self.assertEqual(rec["category"], "gr-qc")
        self.assertEqual(rec["journal"], "Class. Quantum Grav. 38 105009 (2021)")

    def test_arxiv_query_building(self):
        self.assertEqual(lit_search.arxiv_query("alcubierre negative energy"),
                         "all:alcubierre AND all:negative AND all:energy")
        self.assertEqual(lit_search.arxiv_query("ti:warp AND cat:gr-qc"), "ti:warp AND cat:gr-qc")


class GeneralSources(unittest.TestCase):
    def test_parse_crossref_article(self):
        rec = lit_search.parse_crossref(CROSSREF_FIXTURE)[0]
        self.assertEqual(rec["title"], "A journal article")
        self.assertEqual(rec["authors"], ["Ada Example", "The Collaboration"])
        self.assertEqual(rec["year"], "2019")
        self.assertEqual(rec["journal"], "Phys. Rev. D 99 084001")
        self.assertEqual(rec["doc_type"], "article")
        self.assertEqual(rec["citations"], 12)
        self.assertEqual(rec["url"], "https://doi.org/10.0000/example.3")
        self.assertEqual(rec["abstract"], "Energy & momentum are conserved.")

    def test_crossref_preprint_and_missing_year(self):
        pre, old = lit_search.parse_crossref(CROSSREF_FIXTURE)[1:]
        self.assertEqual(pre["journal"], "")
        self.assertEqual(pre["doc_type"], "preprint")
        self.assertIn("| preprint", lit_search.format_record(pre, 0))
        self.assertEqual(old["year"], "")

    def test_parse_s2(self):
        young, review, preprint = lit_search.parse_s2(S2_FIXTURE)
        self.assertEqual(young["journal"], "Class. Quantum Grav. 40 105009")
        self.assertEqual(young["arxiv"], "2301.00001")
        self.assertEqual(young["open_access_pdf"], "https://arxiv.org/pdf/2301.00001")
        self.assertIn("open-access PDF: https://arxiv.org/pdf/2301.00001", lit_search.format_record(young, 100))
        self.assertEqual(review["doc_type"], "review")
        self.assertEqual(review["abstract"], "")
        self.assertEqual(review["open_access_pdf"], "")
        self.assertEqual(preprint["journal"], "")
        self.assertIn("preprint (no journal ref)", lit_search.format_record(preprint, 0))

    def test_mostcited_re_sorts_a_relevance_pool(self):
        urls = []

        def fake_get(url, timeout, headers=None):
            urls.append(url)
            return json.dumps(S2_FIXTURE).encode()
        with mock.patch.object(lit_search, "_get", side_effect=fake_get):
            recs = lit_search.search_s2("warp", 2, "mostcited", 5)
        self.assertEqual([r["title"] for r in recs], ["Highly cited review", "Relevant but young"])
        self.assertIn("limit=10", urls[0])
        with mock.patch.object(lit_search, "_get", side_effect=fake_get):
            recs = lit_search.search_s2("warp", 2, "relevance", 5)
        self.assertEqual([r["title"] for r in recs], ["Relevant but young", "Highly cited review"])
        self.assertIn("limit=2", urls[-1])
        with mock.patch.object(lit_search, "_get", side_effect=fake_get):
            recs = lit_search.search_s2("warp", 3, "mostrecent", 5)
        self.assertEqual([r["year"] for r in recs], ["2025", "2023", "2010"])

    def test_nothing_identifying_is_sent_unless_configured(self):
        calls = []

        def fake_get(url, timeout, headers=None):
            calls.append((url, headers))
            return json.dumps(CROSSREF_FIXTURE if "crossref" in url else S2_FIXTURE).encode()
        clean = {k: v for k, v in os.environ.items() if k not in ("CROSSREF_MAILTO", "SEMANTIC_SCHOLAR_API_KEY")}
        with mock.patch.dict(os.environ, clean, clear=True), mock.patch.object(lit_search, "_get", side_effect=fake_get):
            lit_search.search_crossref("warp", 2, "mostcited", 5)
            lit_search.search_s2("warp", 2, "mostcited", 5)
        self.assertNotIn("mailto", calls[0][0])
        self.assertIsNone(calls[1][1])
        with mock.patch.dict(os.environ, {"CROSSREF_MAILTO": "me@example.org", "SEMANTIC_SCHOLAR_API_KEY": "k123"}), \
                mock.patch.object(lit_search, "_get", side_effect=fake_get):
            lit_search.search_crossref("warp", 2, "mostcited", 5)
            lit_search.search_s2("warp", 2, "mostcited", 5)
        self.assertIn("mailto=me%40example.org", calls[2][0])
        self.assertEqual(calls[3][1], {"x-api-key": "k123"})

    def test_source_aliases_and_lists(self):
        self.assertEqual(lit_search.parse_sources("both"), ["inspire", "arxiv"])
        self.assertEqual(lit_search.parse_sources("general"), ["crossref", "s2"])
        self.assertEqual(lit_search.parse_sources("all"), ["inspire", "arxiv", "crossref", "s2"])
        self.assertEqual(lit_search.parse_sources("s2, inspire,s2"), ["s2", "inspire"])
        with self.assertRaises(lit_search.argparse.ArgumentTypeError):
            lit_search.parse_sources("astrology")

    def test_blocked_host_is_named(self):
        err = lit_search.urllib.error.URLError("Tunnel connection failed: 403 Forbidden")
        with mock.patch.object(lit_search.urllib.request, "urlopen", side_effect=err):
            with self.assertRaises(lit_search.SourceUnavailable) as ctx:
                lit_search._get("https://api.crossref.org/works?query=x", 5)
        self.assertIn("may not allow api.crossref.org", str(ctx.exception))


class Formatting(unittest.TestCase):
    def test_published_record_shows_journal_and_citations(self):
        text = lit_search.format_record(lit_search.parse_inspire(INSPIRE_FIXTURE)[0], 200)
        self.assertIn("Doe, Jane et al.", text)
        self.assertIn("42 citations", text)
        self.assertIn("arXiv:gr-qc/0000001", text)
        self.assertIn("abstract: We show that the energy conditions are violated.", text)

    def test_preprint_is_labelled(self):
        text = lit_search.format_record(lit_search.parse_inspire(INSPIRE_FIXTURE)[1], 200)
        self.assertIn("preprint (no journal ref)", text)


class DocumentTypes(unittest.TestCase):
    def test_book_without_journal_is_not_called_a_preprint(self):
        payload = {"hits": {"hits": [{"id": "9", "metadata": {
            "control_number": 9, "titles": [{"title": "A monograph"}],
            "authors": [{"full_name": "Writer, Wanda"}], "document_type": ["book"],
            "dois": [{"value": "10.0000/book"}], "earliest_date": "2017-01-01"}}]}}
        text = lit_search.format_record(lit_search.parse_inspire(payload)[0], 0)
        self.assertIn("| book", text)
        self.assertNotIn("preprint", text)


class RateLimits(unittest.TestCase):
    @staticmethod
    def http_error(code):
        return lit_search.urllib.error.HTTPError("https://x", code, "Unknown Error", {}, None)

    def test_retries_a_429_then_succeeds(self):
        ok = mock.MagicMock()
        ok.__enter__.return_value.read.return_value = b"payload"
        with mock.patch.object(lit_search.urllib.request, "urlopen",
                               side_effect=[self.http_error(429), ok]) as urlopen, \
                mock.patch.object(lit_search.time, "sleep") as sleep:
            self.assertEqual(lit_search._get("https://x", 5), b"payload")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once()

    def test_persistent_429_says_rate_limited(self):
        with mock.patch.object(lit_search.urllib.request, "urlopen", side_effect=self.http_error(429)), \
                mock.patch.object(lit_search.time, "sleep"):
            with self.assertRaises(lit_search.SourceUnavailable) as ctx:
                lit_search._get("https://x", 5, retries=2)
        self.assertIn("rate-limited", str(ctx.exception))

    def test_other_http_errors_fail_fast(self):
        with mock.patch.object(lit_search.urllib.request, "urlopen", side_effect=self.http_error(500)) as urlopen, \
                mock.patch.object(lit_search.time, "sleep") as sleep:
            with self.assertRaises(lit_search.SourceUnavailable) as ctx:
                lit_search._get("https://x", 5)
        self.assertIn("HTTP 500", str(ctx.exception))
        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()


class Failures(unittest.TestCase):
    def run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = lit_search.main(argv)
        return code, buf.getvalue()

    def test_all_sources_unavailable_exits_3(self):
        with mock.patch.object(lit_search, "_get", side_effect=lit_search.SourceUnavailable("blocked")):
            code, out = self.run_main(["warp drive"])
        self.assertEqual(code, 3)
        self.assertIn("UNAVAILABLE: INSPIRE-HEP", out)
        self.assertIn("UNAVAILABLE: arXiv", out)

    def test_one_source_up_exits_0(self):
        def fake_get(url, timeout):
            if "inspirehep" in url:
                raise lit_search.SourceUnavailable("blocked")
            return ARXIV_FIXTURE
        with mock.patch.object(lit_search, "_get", side_effect=fake_get):
            code, out = self.run_main(["warp drive"])
        self.assertEqual(code, 0)
        self.assertIn("## arXiv: 1 result(s)", out)

    def test_all_sources_run_in_order(self):
        def fake_get(url, timeout, headers=None):
            if "inspirehep" in url:
                return json.dumps(INSPIRE_FIXTURE).encode()
            if "crossref" in url:
                return json.dumps(CROSSREF_FIXTURE).encode()
            if "semanticscholar" in url:
                return json.dumps(S2_FIXTURE).encode()
            raise lit_search.SourceUnavailable("rate-limited")
        with mock.patch.object(lit_search, "_get", side_effect=fake_get):
            code, out = self.run_main(["warp drive", "--source", "all", "--max", "2"])
        self.assertEqual(code, 0)
        order = [out.index(h) for h in ("## INSPIRE-HEP", "UNAVAILABLE: arXiv", "## Crossref", "## Semantic Scholar")]
        self.assertEqual(order, sorted(order))

    def test_json_output(self):
        with mock.patch.object(lit_search, "_get", return_value=json.dumps(INSPIRE_FIXTURE).encode()):
            code, out = self.run_main(["warp drive", "--source", "inspire", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), 2)


class RelevanceAndRecency(unittest.TestCase):
    """Best match first by default, a per-source --since filter, and INSPIRE-only syntax kept to INSPIRE."""

    def capture(self, argv, responder=None):
        urls = []

        def fake_get(url, timeout, headers=None):
            urls.append(url)
            if responder:
                return responder(url)
            if "inspirehep" in url:
                return json.dumps(INSPIRE_FIXTURE).encode()
            if "crossref" in url:
                return json.dumps(CROSSREF_FIXTURE).encode()
            if "semanticscholar" in url:
                return json.dumps(S2_FIXTURE).encode()
            return ARXIV_FIXTURE
        out = io.StringIO()
        with mock.patch.object(lit_search, "_get", side_effect=fake_get), contextlib.redirect_stdout(out):
            code = lit_search.main(argv)
        return code, out.getvalue(), urls

    def test_default_sort_is_inspire_bestmatch(self):
        _, _, urls = self.capture(["neutron lifetime", "--source", "inspire"])
        self.assertIn("sort=bestmatch", urls[0])
        _, _, urls = self.capture(["neutron lifetime", "--source", "inspire", "--sort", "mostcited"])
        self.assertIn("sort=mostcited", urls[0])

    def test_since_is_translated_for_each_source(self):
        code, out, urls = self.capture(["neutron lifetime", "--source", "all", "--since", "2024"])
        self.assertEqual(code, 0)
        inspire, arxiv, crossref, s2 = urls
        self.assertIn("de%3E%3D2024", inspire)
        self.assertIn("submittedDate%3A%5B202401010000+TO+209912312359%5D", arxiv)
        self.assertIn("filter=from-pub-date%3A2024-01-01", crossref)
        self.assertIn("year=2024-", s2)
        self.assertIn("(since 2024)", out)
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                lit_search.main(["x", "--since", "24"])

    def test_inspire_only_syntax_skips_the_other_sources(self):
        _, out, urls = self.capture(['t "neutron lifetime"'])
        self.assertTrue(all("inspirehep" in u for u in urls))
        self.assertIn("SKIPPED: arXiv can't read INSPIRE search syntax", out)
        _, out, urls = self.capture(["a neutron lifetime puzzle"])
        self.assertTrue(any("arxiv" in u for u in urls), "plain words starting with 'a' still go to arXiv")

    def test_refersto_arxiv_is_resolved_to_a_record_id(self):
        def responder(url):
            if "control_number" in url and "arxiv%3A2412.19519" in url:
                return json.dumps({"hits": {"hits": [{"metadata": {"control_number": 2863199}}]}}).encode()
            return json.dumps(INSPIRE_FIXTURE).encode()
        _, _, urls = self.capture(["refersto:arxiv:2412.19519", "--source", "inspire"], responder)
        self.assertEqual(len(urls), 2)
        self.assertIn("refersto%3Arecid%3A2863199", urls[1])

    def test_an_empty_inspire_answer_explains_its_syntax(self):
        empty = lambda url: json.dumps({"hits": {"total": 0, "hits": []}}).encode()  # noqa: E731
        _, out, _ = self.capture(["J-PARC neutron lifetime", "--source", "inspire"], empty)
        self.assertIn('hyphenated names need quotes ("J-PARC")', out)


class SinceAndCitations(RelevanceAndRecency):
    def test_since_keeps_an_or_query_inside_the_filter(self):
        _, _, urls = self.capture(['t "neutron lifetime" or t "UCNtau"', "--source", "inspire", "--since", "2025"])
        self.assertIn(lit_search.urllib.parse.quote_plus('(t "neutron lifetime" or t "UCNtau") and de>=2025'), urls[0])
        _, _, urls = self.capture(["ti:neutron OR abs:UCNtau", "--source", "arxiv", "--since", "2025"])
        self.assertIn(lit_search.urllib.parse.quote_plus("(ti:neutron OR abs:UCNtau) AND submittedDate"), urls[0])

    def test_refersto_accepts_the_ids_lit_search_prints(self):
        looked_up = []

        def responder(url):
            if url.endswith("fields=control_number"):
                looked_up.append(url)
                return json.dumps({"hits": {"hits": [{"metadata": {"control_number": 42}}]}}).encode()
            return json.dumps(INSPIRE_FIXTURE).encode()
        _, _, urls = self.capture(["refersto:arxiv:arXiv:2412.19519v1", "--source", "inspire"], responder)
        self.assertIn("arxiv%3A2412.19519&", looked_up[0])
        _, _, urls = self.capture(["(refersto:arxiv:2403.00914) and t neutron", "--source", "inspire"], responder)
        self.assertIn(lit_search.urllib.parse.quote_plus("(refersto:recid:42) and t neutron"), urls[-1])
        # A DOI with its own parentheses keeps them.
        self.capture(["refersto:doi:10.1016/0146-6410(81)90041-7", "--source", "inspire"], responder)
        self.assertIn(lit_search.urllib.parse.quote_plus("doi:10.1016/0146-6410(81)90041-7"), looked_up[-1])

    def test_an_unknown_identifier_is_not_found_not_unavailable(self):
        def responder(url):
            return json.dumps({"hits": {"hits": []}}).encode()
        code, out, _ = self.capture(["refersto:arxiv:9999.99999", "--source", "inspire"], responder)
        self.assertEqual(code, 0)
        self.assertIn("NOT FOUND: INSPIRE has no record for arxiv:9999.99999", out)
        self.assertNotIn("UNAVAILABLE", out)

    def test_more_inspire_syntax_stays_off_arxiv_but_plain_words_do_not(self):
        for q in ('a Wietfeldt and t "neutron lifetime"', "topcite 100+ and neutron", "collaboration:UCNtau",
                  "exactauthor:F.E.Wietfeldt.1"):
            self.assertTrue(lit_search.INSPIRE_ONLY.search(q), q)
        for q in ("a theory of neutron decay", "neutron and a proton", "a search for dark decays", "beam lifetime"):
            self.assertFalse(lit_search.INSPIRE_ONLY.search(q), q)



if __name__ == "__main__":
    unittest.main()
