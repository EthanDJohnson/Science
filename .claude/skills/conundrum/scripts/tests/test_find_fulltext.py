"""Tests for find_fulltext.py with synthetic index responses shaped like the real APIs.

The fixture values are illustrative: the tests check identifier parsing, merging and ranking of
copies, what is sent to whom, and the fallback when a copy can't be opened. No network access.
"""
import contextlib
import io
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import fetch_text  # noqa: E402
import find_fulltext as ff  # noqa: E402

DOI = "10.1103/PhysRevLett.111.222501"


def inspire_hit(arxiv="1309.2623", doi=DOI):
    return {"hits": {"total": 1, "hits": [{"id": "1", "metadata": {
        "control_number": 1, "titles": [{"title": "Improved Determination of the Neutron Lifetime"}],
        "arxiv_eprints": [{"value": arxiv}] if arxiv else [], "dois": [{"value": doi}] if doi else [],
        "publication_info": [{"journal_title": "Phys.Rev.Lett.", "journal_volume": "111", "artid": "222501",
                              "year": 2013}]}}]}}


OPENALEX = {"title": "Improved Determination of the Neutron Lifetime", "publication_year": 2013,
            "open_access": {"is_oa": True, "oa_status": "green"},
            "locations": [
                {"is_oa": False, "version": "publishedVersion", "pdf_url": None,
                 "landing_page_url": f"https://doi.org/{DOI}", "source": {"display_name": "Physical Review Letters"}},
                {"is_oa": True, "version": "submittedVersion", "pdf_url": "https://arxiv.org/pdf/1309.2623",
                 "landing_page_url": "https://arxiv.org/abs/1309.2623", "source": {"display_name": "arXiv"}},
                {"is_oa": True, "version": None, "pdf_url": None,
                 "landing_page_url": "https://doi.org/10.48550/arxiv.1309.2623", "source": {"display_name": "arXiv"}},
                {"is_oa": True, "version": "acceptedVersion", "pdf_url": "https://repo.example.edu/1234.pdf",
                 "landing_page_url": "https://repo.example.edu/1234", "source": {"display_name": "A repository"},
                 "license": "cc-by"},
            ]}
OSTI = [{"doi": DOI.lower(), "links": [{"rel": "citation", "href": "https://www.osti.gov/biblio/42"},
                                       {"rel": "fulltext", "href": "https://www.osti.gov/servlets/purl/42"}]}]
EUROPEPMC_NONE = {"resultList": {"result": []}}
EUROPEPMC_OA = {"resultList": {"result": [{"doi": DOI.lower(), "pmcid": "PMC99", "isOpenAccess": "Y"}]}}
S2 = {"title": "t", "externalIds": {"ArXiv": "1309.2623"},
      "openAccessPdf": {"url": "https://arxiv.org/pdf/1309.2623", "status": "GREEN"}}


class Responder:
    """Answers each index by host, and records every URL and header sent."""

    def __init__(self, **answers):
        self.answers = {"inspire": inspire_hit(), "openalex": OPENALEX, "osti": OSTI, "ebi": EUROPEPMC_NONE,
                        "semanticscholar": S2, "unpaywall": {"oa_locations": []}}
        self.answers.update(answers)
        self.calls = []

    def __call__(self, url, timeout, retries=2, headers=None):
        self.calls.append((url, headers))
        for key, answer in self.answers.items():
            if key in url:
                if isinstance(answer, Exception):
                    raise answer
                return json.dumps(answer).encode()
        raise AssertionError(f"unexpected URL {url}")

    def hosts(self):
        return [url.split("/")[2] for url, _ in self.calls]


def run(argv, responder, load=None, env=None):
    out = io.StringIO()
    clean = {k: v for k, v in os.environ.items()
             if k not in ("UNPAYWALL_EMAIL", "OPENALEX_MAILTO", "CROSSREF_MAILTO", "SEMANTIC_SCHOLAR_API_KEY")}
    clean.update(env or {})
    patches = [mock.patch.dict(os.environ, clean, clear=True),
               mock.patch.object(ff.lit_search, "_get", side_effect=responder)]
    if load is not None:
        patches.append(mock.patch.object(ff.fetch_text, "load", side_effect=load))
    with contextlib.ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
        with contextlib.redirect_stdout(out):
            code = ff.main(argv)
    return code, out.getvalue()


class Identifiers(unittest.TestCase):
    def test_dois_arxiv_ids_and_urls(self):
        cases = {
            "10.1103/PhysRevLett.111.222501": (DOI, None),
            "doi:10.1103/PhysRevLett.111.222501.": (DOI, None),
            "https://doi.org/10.1103/nr3b-3dtl": ("10.1103/nr3b-3dtl", None),
            "https://link.springer.com/article/10.1140/epja/s10050-026-01929-x": ("10.1140/epja/s10050-026-01929-x", None),
            "https://journals.aps.org/prc/abstract/10.1103/PhysRevC.71.055502": ("10.1103/PhysRevC.71.055502", None),
            "(see 10.1016/0146-6410(81)90041-7)": ("10.1016/0146-6410(81)90041-7", None),
            "https://doi.org/10.1103%2FPhysRevLett.111.222501": (DOI, None),
            "arXiv:2412.19519v1": (None, "2412.19519"),
            "2412.19519": (None, "2412.19519"),
            "https://arxiv.org/abs/2506.01682v2": (None, "2506.01682"),
            "https://arxiv.org/pdf/nucl-ex/0411041": (None, "nucl-ex/0411041"),
            "nucl-ex/0411041v2": (None, "nucl-ex/0411041"),
            "https://doi.org/10.48550/arXiv.2412.19519": (None, "2412.19519"),
        }
        for text, want in cases.items():
            self.assertEqual(ff.parse_identifier(text), want, text)

    def test_a_malformed_identifier_exits_1(self):
        with self.assertRaises(ff.BadIdentifier):
            ff.parse_identifier("https://www.sciencedirect.com/science/article/pii/S0370269318306075")
        code, out = run(["not a paper"], Responder())
        self.assertEqual(code, 1)
        self.assertIn("give a DOI", out)


class Finding(unittest.TestCase):
    def test_copies_are_merged_and_ranked(self):
        code, out = run([DOI, "--json"], Responder())
        self.assertEqual(code, 0)
        data = json.loads(out)
        urls = [c["url"] for c in data["copies"]]
        # The arXiv copy found three ways is one entry; the paywalled publisher page is not a copy.
        self.assertEqual(urls.count("https://arxiv.org/pdf/1309.2623"), 1)
        self.assertNotIn(f"https://doi.org/{DOI}", urls)
        arxiv = next(c for c in data["copies"] if "arxiv" in c["url"])
        self.assertEqual(arxiv["found_by"], ["INSPIRE", "OpenAlex"])
        # Accepted manuscripts come before the preprint.
        self.assertEqual(urls, ["https://repo.example.edu/1234.pdf", "https://www.osti.gov/servlets/purl/42",
                                "https://arxiv.org/pdf/1309.2623"])
        self.assertEqual(data["paper"]["arxiv"], "1309.2623")

    def test_a_published_open_copy_comes_first(self):
        code, out = run([DOI, "--json"], Responder(ebi=EUROPEPMC_OA))
        first = json.loads(out)["copies"][0]
        self.assertEqual(first["url"], "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC99/fullTextXML")
        self.assertEqual(first["version"], "published")

    def test_nothing_identifying_is_sent_unless_configured(self):
        responder = Responder()
        run([DOI], responder)
        self.assertNotIn("api.unpaywall.org", responder.hosts())
        self.assertFalse(any("mailto" in url or "email" in url for url, _ in responder.calls))
        self.assertTrue(all(headers is None for _, headers in responder.calls))
        responder = Responder()
        run([DOI], responder, env={"UNPAYWALL_EMAIL": "me@example.org", "OPENALEX_MAILTO": "me@example.org"})
        unpaywall = [url for url, _ in responder.calls if "unpaywall" in url]
        self.assertEqual(len(unpaywall), 1)
        self.assertIn("email=me%40example.org", unpaywall[0])
        self.assertTrue(any("openalex" in url and "mailto=me%40example.org" in url for url, _ in responder.calls))

    def test_semantic_scholar_is_asked_only_when_nothing_else_found_a_copy(self):
        responder = Responder()
        run([DOI], responder)
        self.assertNotIn("api.semanticscholar.org", responder.hosts())
        closed = {"title": "t", "open_access": {"oa_status": "closed"}, "locations": []}
        responder = Responder(inspire=inspire_hit(arxiv=None), openalex=closed, osti=[])
        code, out = run([DOI], responder)
        self.assertIn("api.semanticscholar.org", responder.hosts())
        self.assertEqual(code, 0)
        self.assertIn("https://arxiv.org/pdf/1309.2623", out)

    def test_an_index_that_fails_is_noted_not_fatal(self):
        down = ff.lit_search.SourceUnavailable("HTTP 503: rate-limited")
        missing = ff.lit_search.SourceUnavailable("HTTP 404: Not Found")
        code, out = run([DOI], Responder(osti=down, openalex=missing))
        self.assertEqual(code, 0)
        self.assertIn("OSTI unavailable (HTTP 503: rate-limited)", out)
        self.assertIn("OpenAlex no record", out)

    def test_no_free_copy_says_how_to_flag_the_paper(self):
        closed = {"title": "t", "open_access": {"oa_status": "closed"}, "locations": []}
        s2_none = {"title": "t", "externalIds": {}, "openAccessPdf": None}
        code, out = run([DOI], Responder(inspire=inspire_hit(arxiv=None), openalex=closed, osti=[], semanticscholar=s2_none))
        self.assertEqual(code, 3)
        self.assertIn(f"NO FREE COPY FOUND for doi:{DOI}", out)
        self.assertIn(f"PAPER TO REQUEST: doi:{DOI}", out)
        self.assertIn("Never contact anyone yourself", out)

    def test_an_arxiv_id_without_a_doi_skips_the_doi_indexes(self):
        responder = Responder(inspire=inspire_hit(arxiv="2412.19519", doi=None))
        code, out = run(["arXiv:2412.19519"], responder)
        self.assertEqual(code, 0)
        self.assertEqual(responder.hosts(), ["inspirehep.net"])
        self.assertIn("https://arxiv.org/pdf/2412.19519", out)
        self.assertIn("OpenAlex skipped (no DOI)", out)


class Opening(unittest.TestCase):
    CHUNKS = [("[p. 1] ", "The lifetime is 887.7 s with a systematic uncertainty from the neutron flux.")]

    def test_grep_falls_back_past_blocked_and_unreachable_copies(self):
        attempts = []

        def load(url, timeout, pages=None):
            attempts.append(url)
            if "repo.example.edu" in url:
                raise fetch_text.Blocked("repo.example.edu")
            if "osti" in url:
                raise fetch_text.Unavailable("HTTP 403: Forbidden")
            return self.CHUNKS, "PDF, 1 page", url
        code, out = run([DOI, "--grep", "neutron flux"], Responder(), load=load)
        self.assertEqual(code, 0)
        self.assertEqual(len(attempts), 3)
        self.assertIn("SKIPPED: https://repo.example.edu/1234.pdf (repo.example.edu served a bot-check page)", out)
        self.assertIn("SOURCE: https://arxiv.org/pdf/1309.2623 | PDF, 1 page", out)
        self.assertIn("VERSION: preprint, latest arXiv version", out)
        self.assertIn(f"OF: doi:{DOI}", out)
        self.assertIn("neutron flux", out)

    def test_a_phrase_missing_from_every_copy_exits_2(self):
        load = lambda url, timeout, pages=None: (self.CHUNKS, "PDF, 1 page", url)  # noqa: E731
        code, out = run([DOI, "--grep", "dark matter"], Responder(), load=load)
        self.assertEqual(code, 2)
        self.assertIn("NO MATCH for 'dark matter' in the 3 free copies opened.", out)
        self.assertEqual(out.count("Trying the next copy."), 2)

    def test_no_copy_opened_exits_3_or_4(self):
        def unreachable(url, timeout, pages=None):
            raise fetch_text.Unavailable("HTTP 403: Forbidden")
        code, out = run([DOI, "--grep", "flux"], Responder(), load=unreachable)
        self.assertEqual(code, 3)
        self.assertIn("NO FREE COPY COULD BE OPENED", out)
        self.assertIn("PAPER TO REQUEST", out)

        def no_pypdf(url, timeout, pages=None):
            raise fetch_text.NeedsPypdf("pypdf is not installed: pip install pypdf cffi")
        code, out = run([DOI, "--grep", "flux"], Responder(), load=no_pypdf)
        self.assertEqual(code, 4)
        self.assertIn("pip install pypdf", out)

    def test_text_prints_the_best_copy(self):
        load = lambda url, timeout, pages=None: (self.CHUNKS, "PDF, 1 page", url)  # noqa: E731
        code, out = run([DOI, "--text", "--max-chars", "20"], Responder(), load=load)
        self.assertEqual(code, 0)
        self.assertIn("(clipped:", out)


if __name__ == "__main__":
    unittest.main()
