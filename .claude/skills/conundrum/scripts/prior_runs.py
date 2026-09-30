#!/usr/bin/env python3
"""Earlier /conundrum runs: find the ones related to a new question, bring in what the user approves,
and keep each run's record so later runs remember how far to trust it.

From the project root:
    python3 .claude/skills/conundrum/scripts/prior_runs.py list "<question>"   # related runs, best match first
    python3 .claude/skills/conundrum/scripts/prior_runs.py list                # every run, newest first
    python3 .claude/skills/conundrum/scripts/prior_runs.py import <old> --into <new> --mode leads|update
    python3 .claude/skills/conundrum/scripts/prior_runs.py record <slug>       # when a run finishes
    python3 .claude/skills/conundrum/scripts/prior_runs.py mark <slug> --trust distrusted --note "<why>"

How a new run may treat an earlier one (chosen with the user at framing, SKILL.md step 1):
- ignore: agents never see it, and nothing is imported.
- leads: its research notes, source checks and dossier are copied in as pointers to sources only;
  nothing counts until a researcher finds and quotes it again.
- update: its calculation scripts come too, and a claim that re-verifies carries over with a
  PRIOR label naming the run and its date. Researchers then look for newer work.
Conclusions never carry over. Analyses, candidates, verdicts, cruxes, reports and audits stay
behind, so the new run's lenses and judge reason independently.

A run's record is runs/<slug>/run.json. It holds what the files say (date, question, status,
whether its sources were checked, bottom line) and what the user decided: trust ("ok" or
"distrusted"), dated notes, and the run that superseded it. Runs without one are described from
their files.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MODES = ("leads", "update")
# What each mode copies into runs/<new>/prior/<old>/. Conclusions are never on these lists.
COPY = {
    "leads": ["brief.md", "dossier.md", "research/*.md"],
    "update": ["brief.md", "dossier.md", "research/*.md", "calc/*.py"],
}
KEPT = ("trust", "notes", "superseded_by", "recorded")   # what run.json adds to what the files say
OLD_DAYS = 180
STOP = set("""
about above after again against also among another around because been before being below between both
could does doing down during each either even every from further have having here into itself just
made make many might more most much must need needs other over same should since some such than that
their them then there these they this those through under until upon very what when where which while
whom will with within without would your considering question questions answer""".split())


class Refused(Exception):
    pass


# ---------------------------------------------------------------- reading a run
def check_slug(slug: str) -> str:
    if not SLUG.match(slug or ""):
        raise Refused(f"not a run name: {slug!r}")
    return slug


def sections(text: str) -> dict[str, str]:
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            cur = m.group(1).lower()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def header(text: str) -> dict[str, str]:
    """The brief's `slug: ... | depth: ... | type: ... | date: ...` line."""
    for line in text.splitlines()[:8]:
        if "|" in line and ":" in line:
            fields = {}
            for part in line.split("|"):
                key, _, value = part.partition(":")
                fields[key.strip().lower()] = value.strip()
            if {"slug", "date"} & fields.keys():
                return fields
    return {}


def first_paragraph(text: str, limit: int) -> str:
    """The first paragraph, whitespace collapsed. A longer one is cut at its last full sentence
    within the limit, so a bottom line never stops mid-sentence before its credences."""
    para = re.split(r"\n\s*\n", text.strip(), maxsplit=1)[0] if text.strip() else ""
    para = " ".join(para.split())
    if len(para) <= limit:
        return para
    cut = para[: limit - 1]
    end = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    return cut[: end + 1] + " …" if end >= limit // 2 else cut.rstrip() + "…"


def parse_prior(brief_text: str) -> list[dict]:
    """The brief's `## Prior runs` lines: `- <run> (<date>): <mode>[, same question]. <reason>`."""
    out = []
    for line in sections(brief_text).get("prior runs", "").splitlines():
        m = re.match(r"^\s*-\s*`?([A-Za-z0-9][\w.-]*)`?\s*\((\d{4}-\d{2}-\d{2})\)\s*:\s*(ignore|leads|update)"
                     r"(\s*,\s*same question)?", line, re.I)
        if m:
            out.append({"slug": m.group(1), "date": m.group(2), "mode": m.group(3).lower(),
                        "same_question": bool(m.group(4))})
    return out


def describe(run: Path) -> dict:
    """What a run's files say, plus the user's decisions kept in its run.json."""
    brief = (run / "brief.md").read_text(errors="replace") if (run / "brief.md").is_file() else ""
    report = (run / "report.md").read_text(errors="replace") if (run / "report.md").is_file() else ""
    fields, parts = header(brief), sections(brief)
    title = re.match(r"^#\s*(?:Brief:\s*)?(.*)", brief).group(1).strip() if brief.startswith("#") else ""
    when = fields.get("date") or (run.name[:10] if re.match(r"\d{4}-\d{2}-\d{2}", run.name) else "")
    rec = {
        "slug": run.name,
        "date": when,
        "title": title,
        "question": first_paragraph(" ".join(line.strip().strip('"“”') for line in
                                             parts.get("question as asked", "").split("\n\n")[0].splitlines()), 300),
        "type": (fields.get("type") or "").split(" ")[0],
        "depth": (fields.get("depth") or "").split(" ")[0],
        "status": "complete" if report else "partial",
        "source_checked": any((run / "research").glob("*.check.md")),
        "bottom_line": first_paragraph(sections(report).get("bottom line", ""), 2000),
        "prior": parse_prior(brief),
        "trust": "ok",
        "notes": [],
        "superseded_by": None,
    }
    try:
        kept = json.loads((run / "run.json").read_text())
        rec.update({k: kept[k] for k in KEPT if k in kept})
    except (OSError, ValueError):
        pass
    rec["_text"] = " ".join([title, rec["question"], parts.get("question made precise", ""), rec["bottom_line"]])
    return rec


def save(run: Path, rec: dict) -> None:
    (run / "run.json").write_text(json.dumps({k: v for k, v in rec.items() if not k.startswith("_")},
                                             indent=2, ensure_ascii=False) + "\n")


def runs_in(runs: Path) -> list[dict]:
    if not runs.is_dir():
        return []
    return [describe(d) for d in sorted(runs.iterdir()) if d.is_dir() and SLUG.match(d.name)
            and ((d / "brief.md").is_file() or (d / "run.json").is_file())]


# ---------------------------------------------------------------- choosing
def keywords(text: str) -> set[str]:
    out = set()
    for word in re.findall(r"[a-z][a-z0-9-]+", text.lower()):
        for part in word.split("-"):
            if len(part) >= 4 and part not in STOP:
                out.add(part[:-1] if part.endswith("s") and len(part) > 4 else part)
    return out


def match(question: str, rec: dict) -> float:
    q = keywords(question)
    return len(q & keywords(rec["_text"])) / len(q) if q else 0.0


def days_old(rec: dict, today: date) -> int | None:
    try:
        return (today - date.fromisoformat(rec["date"])).days
    except (TypeError, ValueError):
        return None


def age_text(days: int | None) -> str:
    if days is None:
        return "undated"
    if days < 1:
        return "today"
    if days < 60:
        return f"{days} days ago"
    return f"{days // 30} months ago" if days < 730 else f"{days // 365} years ago"


def suggest(rec: dict, today: date) -> tuple[str, str]:
    """The default mode for an earlier run, with its reason."""
    if rec["trust"] == "distrusted":
        return "ignore", "you marked it distrusted"
    problems = []
    if rec["status"] != "complete":
        problems.append("never finished")
    if not rec["source_checked"]:
        problems.append("sources never checked")
    if problems:
        return "leads", "; ".join(problems)
    days = days_old(rec, today)
    if days is not None and days > OLD_DAYS:
        return "update", f"complete and source-checked, but {age_text(days)}: use leads if the field moves fast"
    return "update", "complete and source-checked"


def listing(runs: Path, question: str | None, today: date, limit: int = 10) -> str:
    recs = runs_in(runs)
    if not recs:
        return f"No earlier runs in {runs}/."
    shown, footer = [], []
    for rec in recs:
        if rec["trust"] == "distrusted":
            footer.append(f"{rec['slug']} (you marked it distrusted{': ' + rec['notes'][-1] if rec['notes'] else ''})")
        elif rec["superseded_by"]:
            footer.append(f"{rec['slug']} (superseded by {rec['superseded_by']})")
        else:
            shown.append(rec)
    if question:
        scored = sorted(((match(question, r), r) for r in shown), key=lambda x: (-x[0], x[1]["slug"]))
        unrelated = sum(1 for s, _ in scored if s == 0)
        shown_scored = [(s, r) for s, r in scored if s > 0][:limit]
        head = f'Earlier runs, best match first, for: "{question}"'
    else:
        shown_scored = [(None, r) for r in sorted(shown, key=lambda r: r["date"], reverse=True)[:limit]]
        unrelated, head = 0, "Earlier runs, newest first"
    lines = [head, ""]
    for i, (score, rec) in enumerate(shown_scored, 1):
        mode, why = suggest(rec, today)
        facts = [f"{rec['date'] or 'undated'} ({age_text(days_old(rec, today))})", rec["status"],
                 "sources checked" if rec["source_checked"] else "sources not checked"]
        if rec["depth"]:
            facts.append(f"depth {rec['depth']}")
        if score is not None:
            facts.append(f"match {score:.0%}")
        lines.append(f"{i}. {rec['slug']} · " + " · ".join(facts))
        lines.append(f"   Question: {rec['title'] or rec['question'] or '(no brief)'}")
        lines.append(f"   Bottom line: {rec['bottom_line'] or 'none (no report)'}")
        for note in rec["notes"]:
            lines.append(f"   Note: {note}")
        lines.append(f"   Suggested: {mode} ({why})")
    if not shown_scored:
        lines.append("None related." if question else "None.")
    if unrelated:
        lines.append(f"\n{unrelated} unrelated run(s) not shown.")
    if footer:
        lines.append("\nIgnored without asking: " + "; ".join(footer) + ".")
    return "\n".join(lines)


# ---------------------------------------------------------------- acting
MODE_RULES = {
    "leads": (
        "**Leads only.** Use these notes to find sources quickly: which papers carried weight, what each "
        "claimed, and where access failed. Carry nothing. A lead becomes a claim in this run only when you "
        "find and quote the source yourself, and then it is an ordinary claim with no PRIOR line. Never cite "
        "a file in this folder."),
    "update": (
        "**Update.** A claim from these notes may carry into this run once you re-verify it against its "
        "source with `fetch_text.py` or `lit_search.py`. Write it with this run's claim ID and a line "
        "`PRIOR: {slug} ({date}), was <old ID>; re-verified`. If the source can't be reopened, you may keep "
        "the claim as `ACCESS: search-summary` with `PRIOR: ... ; not re-verified`. Then search for work "
        "published after {date}, and record any newer result that contradicts or supersedes a carried claim. "
        "The calculation scripts under `calc/` may be read for method, but any number cited in this run must "
        "come from a script in this run's own `calc/` folder. Never cite a file in this folder."),
}


def import_run(runs: Path, old: str, new: str, mode: str, today: date) -> list[Path]:
    check_slug(old), check_slug(new)
    if mode not in MODES:
        raise Refused("mode must be leads or update (ignore imports nothing)")
    if old == new:
        raise Refused("a run can't import itself")
    src, into = runs / old, runs / new
    if not src.is_dir():
        raise Refused(f"no run folder {src}")
    if not into.is_dir():
        raise Refused(f"no run folder {into}; create it first")
    rec = describe(src)
    if rec["trust"] == "distrusted":
        why = f": {rec['notes'][-1]}" if rec["notes"] else ""
        raise Refused(f"{old} is marked distrusted{why}. If the user now trusts it, run "
                      f"`prior_runs.py mark {old} --trust ok` first")
    dst = into / "prior" / old
    if dst.exists():
        shutil.rmtree(dst)   # a re-import replaces the earlier copy
    base, copied = src.resolve(), []
    for pattern in COPY[mode]:
        for f in sorted(src.glob(pattern)):
            if f.is_symlink() or not f.is_file() or base not in f.resolve().parents:
                continue
            rel = f.relative_to(src)
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst / rel)
            copied.append(rel)
    notes = "\n".join(f"- {n}" for n in rec["notes"]) or "- none"
    (dst / "PROVENANCE.md").write_text(
        f"# Material from an earlier run: {old}\n\n"
        f"- Run date: {rec['date'] or 'unknown'} ({age_text(days_old(rec, today))})\n"
        f"- Question then: {rec['title'] or rec['question'] or 'unknown'}\n"
        f"- Status then: {rec['status']}; sources {'checked' if rec['source_checked'] else 'not checked'}\n"
        f"- Imported on {today.isoformat()} as: {mode}\n\n"
        f"Notes on this run:\n{notes}\n\n"
        + MODE_RULES[mode].format(slug=old, date=rec["date"] or "its run date") + "\n\n"
        "Nothing here is a conclusion. The earlier run's analyses, candidates, verdicts, report and audit "
        "were left behind on purpose, so this run reaches its own.\n")
    return copied


def mark(runs: Path, slug: str, today: date, trust: str | None = None, note: str | None = None,
         superseded_by: str | None = None) -> dict:
    run = runs / check_slug(slug)
    if not run.is_dir():
        raise Refused(f"no run folder {run}")
    rec = describe(run)
    if trust:
        rec["trust"] = trust
    if note:
        rec["notes"] = rec["notes"] + [f"{today.isoformat()}: {' '.join(note.split())}"]
    if superseded_by:
        rec["superseded_by"] = check_slug(superseded_by)
    save(run, rec)
    return rec


def record(runs: Path, slug: str, today: date) -> dict:
    """Write a finished run's run.json, and mark earlier runs of the same question superseded."""
    run = runs / check_slug(slug)
    if not run.is_dir():
        raise Refused(f"no run folder {run}")
    rec = describe(run)
    rec["recorded"] = today.isoformat()
    save(run, rec)
    for p in rec["prior"]:
        if p["same_question"] and p["slug"] != slug and (runs / p["slug"]).is_dir():
            mark(runs, p["slug"], today, superseded_by=slug)
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=Path, default=Path("runs"), help="the runs folder (default: runs)")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("list", help="earlier runs, best match first")
    p.add_argument("question", nargs="?")
    p = sub.add_parser("import", help="copy an approved earlier run into a new one")
    p.add_argument("old")
    p.add_argument("--into", required=True)
    p.add_argument("--mode", required=True, choices=MODES)
    p = sub.add_parser("record", help="write a finished run's run.json")
    p.add_argument("slug")
    p = sub.add_parser("mark", help="record the user's view of a run")
    p.add_argument("slug")
    p.add_argument("--trust", choices=("ok", "distrusted"))
    p.add_argument("--note")
    p.add_argument("--superseded-by")
    args = ap.parse_args(argv)
    today = date.today()
    try:
        if args.command == "list":
            print(listing(args.runs, args.question, today))
        elif args.command == "import":
            copied = import_run(args.runs, args.old, args.into, args.mode, today)
            print(f"imported {len(copied)} file(s) from {args.old} as {args.mode} into "
                  f"{args.runs / args.into / 'prior' / args.old}/ (see PROVENANCE.md there)")
        elif args.command == "record":
            rec = record(args.runs, args.slug, today)
            print(f"recorded {args.slug}: {rec['status']}, sources {'checked' if rec['source_checked'] else 'not checked'}")
        else:
            if not (args.trust or args.note or args.superseded_by):
                ap.error("mark needs --trust, --note or --superseded-by")
            rec = mark(args.runs, args.slug, today, args.trust, args.note, args.superseded_by)
            print(f"{args.slug}: trust {rec['trust']}, {len(rec['notes'])} note(s)"
                  + (f", superseded by {rec['superseded_by']}" if rec["superseded_by"] else ""))
    except Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
