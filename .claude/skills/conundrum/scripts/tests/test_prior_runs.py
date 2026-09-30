"""Tests for prior_runs.py on a synthetic runs/ folder.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prior_runs as pr  # noqa: E402

TODAY = date(2026, 10, 1)
WARP = "Considering Alcubierre drives, what are viable engineering options for the negative energy required?"


def make_run(runs: Path, slug: str, question: str, report: str | None = None, checked: bool = False,
             prior_lines: str = "") -> Path:
    d = runs / slug
    for sub in ("research", "calc", "analyses", "verdicts", "cruxes"):
        (d / sub).mkdir(parents=True)
    (d / "brief.md").write_text(
        f"# Brief: {question[:40]}\nslug: {slug} | depth: standard | type: feasibility | date: {slug[:10]}\n\n"
        f'## Question as asked\n"{question}"\n\n## Question made precise\n- terms defined here\n\n'
        f"## Prior runs\n{prior_lines or 'None.'}\n")
    (d / "research" / "theory.md").write_text("# Research: theory\n- [RT-01] CLAIM: a claim\n")
    if checked:
        (d / "research" / "theory.check.md").write_text("| RT-01 | verified | quote found |\n")
    (d / "dossier.md").write_text("# Dossier\n")
    (d / "calc" / "lens_energy.py").write_text("print('1 J')\n")
    (d / "analyses" / "constraints.md").write_text("# Analysis: constraints\n")
    (d / "verdicts" / "C1-0.md").write_text("verdict: refuted\n")
    (d / "cruxes" / "C2.md").write_text("# Crux\n")
    (d / "candidates.md").write_text("# Candidate answers\n")
    if report:
        (d / "report.md").write_text(f"# Report\n\n## Bottom line\n{report}\n\nMore detail.\n\n## Ranked answers\n")
        (d / "audit.md").write_text("# Audit\n")
    return d


class PriorRuns(unittest.TestCase):
    def setUp(self):
        self.box = tempfile.TemporaryDirectory()
        self.runs = Path(self.box.name) / "runs"
        self.runs.mkdir()
        self.done = make_run(self.runs, "2026-03-01-alcubierre-energy", "What negative energy does an Alcubierre drive need?",
                             report="No viable option within known physics.", checked=True)
        self.notes = make_run(self.runs, "2026-09-29-warp-bubble-shapes", "Which warp-bubble shapes need less energy?")
        self.other = make_run(self.runs, "2026-05-01-battery-anomaly", "Is the battery capacity fade anomaly real?",
                              report="Artifact.", checked=True)
        self.new = self.runs / "2026-10-01-alcubierre-options"
        self.new.mkdir()

    def tearDown(self):
        self.box.cleanup()

    def test_describe_reads_the_files(self):
        rec = pr.describe(self.done)
        self.assertEqual((rec["date"], rec["status"], rec["depth"], rec["type"]),
                         ("2026-03-01", "complete", "standard", "feasibility"))
        self.assertTrue(rec["source_checked"])
        self.assertEqual(rec["bottom_line"], "No viable option within known physics.")
        self.assertEqual(rec["question"], "What negative energy does an Alcubierre drive need?")
        partial = pr.describe(self.notes)
        self.assertEqual((partial["status"], partial["source_checked"], partial["bottom_line"]), ("partial", False, ""))

    def test_suggested_modes(self):
        self.assertEqual(pr.suggest(pr.describe(self.done), TODAY)[0], "update")
        self.assertIn("months ago", pr.suggest(pr.describe(self.done), TODAY)[1])   # 7 months old
        self.assertEqual(pr.suggest(pr.describe(self.done), date(2026, 3, 20)),
                         ("update", "complete and source-checked"))
        self.assertEqual(pr.suggest(pr.describe(self.notes), TODAY),
                         ("leads", "never finished; sources never checked"))
        pr.mark(self.runs, self.done.name, TODAY, trust="distrusted", note="used a retracted paper")
        self.assertEqual(pr.suggest(pr.describe(self.done), TODAY)[0], "ignore")

    def test_listing_ranks_related_runs_and_hides_the_rest(self):
        text = pr.listing(self.runs, WARP, TODAY)
        self.assertLess(text.index("alcubierre-energy"), text.index("warp-bubble-shapes"))
        self.assertNotIn("battery", text)
        self.assertIn("1 unrelated run(s) not shown", text)
        self.assertIn("Suggested: leads (never finished; sources never checked)", text)
        self.assertNotIn("alcubierre-options", text)            # the new run has no brief yet
        everything = pr.listing(self.runs, None, TODAY)
        self.assertIn("battery", everything)

    def test_distrusted_and_superseded_runs_are_ignored_without_asking(self):
        pr.mark(self.runs, self.done.name, TODAY, trust="distrusted", note="I don't trust that research")
        pr.mark(self.runs, self.notes.name, TODAY, superseded_by="2026-09-30-newer")
        text = pr.listing(self.runs, WARP, TODAY)
        footer = text.split("Ignored without asking:")[1]
        self.assertIn("2026-03-01-alcubierre-energy (you marked it distrusted: 2026-10-01: I don't trust that research)", footer)
        self.assertIn("2026-09-29-warp-bubble-shapes (superseded by 2026-09-30-newer)", footer)
        self.assertIn("None related.", text)

    def test_leads_copies_evidence_but_never_conclusions(self):
        copied = pr.import_run(self.runs, self.done.name, self.new.name, "leads", TODAY)
        dst = self.new / "prior" / self.done.name
        self.assertEqual(sorted(map(str, copied)),
                         ["brief.md", "dossier.md", "research/theory.check.md", "research/theory.md"])
        for gone in ("report.md", "audit.md", "candidates.md", "analyses", "verdicts", "cruxes", "calc"):
            self.assertFalse((dst / gone).exists(), gone)
        provenance = (dst / "PROVENANCE.md").read_text()
        self.assertIn("**Leads only.**", provenance)
        self.assertIn("Run date: 2026-03-01 (7 months ago)", provenance)
        self.assertIn("Nothing here is a conclusion", provenance)

    def test_update_also_brings_calculation_scripts_and_the_carry_rule(self):
        pr.mark(self.runs, self.done.name, TODAY, note="White's plot values were read by eye")
        copied = pr.import_run(self.runs, self.done.name, self.new.name, "update", TODAY)
        self.assertIn(Path("calc/lens_energy.py"), copied)
        provenance = (self.new / "prior" / self.done.name / "PROVENANCE.md").read_text()
        self.assertIn("PRIOR: 2026-03-01-alcubierre-energy (2026-03-01), was <old ID>; re-verified", provenance)
        self.assertIn("published after 2026-03-01", provenance)
        self.assertIn("White's plot values were read by eye", provenance)

    def test_reimport_replaces_the_earlier_copy(self):
        pr.import_run(self.runs, self.done.name, self.new.name, "update", TODAY)
        pr.import_run(self.runs, self.done.name, self.new.name, "leads", TODAY)
        self.assertFalse((self.new / "prior" / self.done.name / "calc").exists())

    def test_import_refusals(self):
        pr.mark(self.runs, self.notes.name, TODAY, trust="distrusted")
        cases = [(self.notes.name, self.new.name, "leads", "distrusted"),
                 (self.done.name, self.new.name, "ignore", "mode must be"),
                 (self.done.name, self.done.name, "leads", "itself"),
                 (self.done.name, "2026-10-02-missing", "leads", "create it first"),
                 ("../outside", self.new.name, "leads", "not a run name"),
                 ("2025-01-01-nothing", self.new.name, "leads", "no run folder")]
        for old, new, mode, why in cases:
            with self.subTest(old=old, new=new, mode=mode):
                with self.assertRaisesRegex(pr.Refused, why):
                    pr.import_run(self.runs, old, new, mode, TODAY)

    def test_symlinks_are_not_followed_out_of_a_run(self):
        secret = Path(self.box.name) / "secret.md"
        secret.write_text("private")
        (self.done / "research" / "leak.md").symlink_to(secret)
        copied = pr.import_run(self.runs, self.done.name, self.new.name, "leads", TODAY)
        self.assertNotIn(Path("research/leak.md"), copied)

    def test_record_writes_the_run_and_supersedes_the_same_question(self):
        pr.mark(self.runs, self.done.name, TODAY, note="kept note")
        finished = make_run(self.runs, "2026-10-02-alcubierre-rerun", "What negative energy does an Alcubierre drive need?",
                            report="Still no viable option.", checked=True, prior_lines=(
                                "- `2026-03-01-alcubierre-energy` (2026-03-01): update, same question. Complete and checked.\n"
                                "- 2026-09-29-warp-bubble-shapes (2026-09-29): leads. Never source-checked."))
        rec = pr.record(self.runs, finished.name, TODAY)
        saved = json.loads((finished / "run.json").read_text())
        self.assertEqual((saved["status"], saved["bottom_line"], saved["recorded"]),
                         ("complete", "Still no viable option.", "2026-10-01"))
        self.assertEqual([p["mode"] for p in rec["prior"]], ["update", "leads"])
        self.assertNotIn("_text", saved)
        old = pr.describe(self.done)
        self.assertEqual(old["superseded_by"], finished.name)
        self.assertEqual(old["notes"], ["2026-10-01: kept note"])        # decisions survive
        self.assertIsNone(pr.describe(self.notes)["superseded_by"])      # a different question

    def test_command_line(self):
        runs = str(self.runs)
        quiet = contextlib.ExitStack()
        quiet.enter_context(contextlib.redirect_stdout(io.StringIO()))
        quiet.enter_context(contextlib.redirect_stderr(io.StringIO()))
        self.addCleanup(quiet.close)
        self.assertEqual(pr.main(["--runs", runs, "import", self.done.name, "--into", self.new.name, "--mode", "update"]), 0)
        self.assertEqual(pr.main(["--runs", runs, "mark", self.notes.name, "--trust", "distrusted", "--note", "stale"]), 0)
        self.assertEqual(pr.main(["--runs", runs, "import", self.notes.name, "--into", self.new.name, "--mode", "leads"]), 2)
        self.assertEqual(pr.main(["--runs", runs, "record", self.done.name]), 0)
        with self.assertRaises(SystemExit):
            pr.main(["--runs", runs, "mark", self.done.name])              # nothing to mark


if __name__ == "__main__":
    unittest.main()


class BottomLines(unittest.TestCase):
    def test_a_long_bottom_line_is_cut_at_a_sentence_not_mid_word(self):
        text = ("On a fixed classical spacetime there is no conflict. " * 12
                + "The weak null stands at about 0.85 and the relational answer at 0.15.")
        cut = pr.first_paragraph(text, 500)
        self.assertLessEqual(len(cut), 500)
        self.assertTrue(cut.endswith("conflict. …"), cut[-40:])
        self.assertEqual(pr.first_paragraph("Short. Two.", 500), "Short. Two.")
        self.assertEqual(pr.first_paragraph("x" * 20, 10), "x" * 9 + "…")   # no sentence to cut at

    def test_the_record_keeps_a_bottom_line_of_up_to_about_1200_characters(self):
        para = "One sentence of the bottom line, with its credence of 0.85. " * 15
        self.assertEqual(len(pr.first_paragraph(para, 1200)), len(para.strip()))
