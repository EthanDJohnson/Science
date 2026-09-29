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

    def test_json_output(self):
        with mock.patch.object(lit_search, "_get", return_value=json.dumps(INSPIRE_FIXTURE).encode()):
            code, out = self.run_main(["warp drive", "--source", "inspire", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), 2)


if __name__ == "__main__":
    unittest.main()
