# Science

Tools for investigating hard physics and engineering questions with Claude Code. The main one is the `/conundrum` skill.

## `/conundrum` (v1)

A multi-agent pipeline for questions like:

> Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?

It frames the question with you, researches the literature in parallel, checks the sources, and has independent analysts attack the problem through different methods. It then builds a slate of competing answers, including "none is viable" and "the question's premise is wrong". It tries to refute each one with calculations and sources, and a neutral judge writes a calibrated report. An auditor then traces every claim in the report back to the evidence.

The design, and the review of the Gemini proposal it started from, are in [`docs/conundrum-skill-plan.md`](docs/conundrum-skill-plan.md).

### Quick start

1. **Requirements**
   - Claude Code with dynamic workflows. They're available on paid plans; on Pro, turn them on under Dynamic workflows in `/config`.
   - Python 3.10+ with `pip install sympy numpy`.
2. **Start a new Claude Code session in this repo.** Claude Code loads the skill, agents and workflows at session start.
3. **Run the skill:**
   ```
   /conundrum standard Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?
   ```
4. **Confirm the brief,** which is Claude's precise restatement of your question.
5. **Review the dossier** after the research stage, and add anything you know.
6. **Confirm the analysis stage,** then read `runs/<slug>/report.md`.

### Depth and cost

| Depth | What runs | Agent runs | Rough cost at API list prices |
|---|---|---|---|
| `quick` | 3 researchers, 3 lenses, 1 refuter per candidate, Opus judge | ~16 | ~$10–25 |
| `standard` | 4 researchers with source checks, 5 lenses, 1 refuter per candidate, Fable judge | ~23 | ~$20–40 |
| `deep` | 5 researchers with checks, 6–7 lenses, 3 refuters per candidate with different angles, rebuttal round, Fable judge at max effort | ~40–50 | ~$50–100 |

These costs are estimates, not measurements. On a subscription a run draws on your usage limits instead. `/workflows` shows live token counts, and you can stop a run there.

### What you get

Everything lands in `runs/<slug>/`:

| File | What it is |
|---|---|
| `brief.md` | The question made precise: definitions, admissible physics, premises to test |
| `research/*.md` | Sourced claims per facet, each with a verbatim quote and access level; `*.check.md` holds the source-check verdicts |
| `dossier.md` | The checked evidence base: established results, key numbers, contested points, constraints |
| `analyses/*.md` | One file per lens |
| `candidates.md` | The competing answers, each with its decisive test |
| `verdicts/*.md` | The refutation attempts, each grounded in a calculation, a quote or an inconsistency |
| `report.md` | The ranked answers with credences: in principle vs. in practice, orders-of-magnitude gaps, what would change the verdict |
| `audit.md` | Every claim in the report traced to the evidence |
| `calc/*.py` | Every calculation the agents ran, so you can rerun them |

### How it works

```
/conundrum ─ frame the brief with you
  └ workflow conundrum-research: researchers (Sonnet) → source checkers → dossier (Opus)
  ─ checkpoint: you review the dossier and approve the lenses
  └ workflow conundrum-analyze: lenses (Opus) → candidate slate → refuters → [rebuttals] → judge (Fable) → audit
```

**Lenses** are independent analysts, each with a different method:

| Lens | Method |
|---|---|
| Decomposer | assumption ledger |
| Constraints | energy conditions, quantum inequalities, causality, all computed |
| Examiner | is the question well posed? |
| Engineer | orders-of-magnitude gap to demonstrated tech, TRL |
| Mechanist | causal chains |
| Idealizer | toy model, solved |
| Empiricist | what was actually measured |
| Dialectician | resolves contradictions |

The philosopher labels in the agent files are mnemonics; the methods are the content.

**Physics tooling.** `gr_tensors.py` computes the stress-energy a metric requires, what observers measure, energy-condition scans and total energy on a slice. It is tested against Schwarzschild, FRW, Morris–Thorne and Alcubierre closed forms. `lit_search.py` queries INSPIRE-HEP and arXiv.

### Network access

- **Local runs** have full web access.
- **Claude Code on the web** may block literature sites under the environment's network policy. The preflight reports which sources are reachable. Blocked research falls back to search snippets, which the pipeline marks and weighs down.

**To open it up.** The Android app can't edit environments, so use claude.ai/code in a browser or the Desktop app.
1. Click the cloud button showing the environment name (e.g. **Default**) above the message box.
2. Hover over the environment and click its gear icon.
3. Set **Network access** to **Custom**, paste the list below, and tick **Also include default list of common package managers** (PyPI).
4. Add `pip install sympy numpy` to **Setup script**; it is cached for later sessions.

```
arxiv.org
*.arxiv.org
inspirehep.net
doi.org
dx.doi.org
www.osti.gov
ui.adsabs.harvard.edu
ntrs.nasa.gov
*.aps.org
iopscience.iop.org
link.springer.com
www.sciencedirect.com
www.nature.com
www.science.org
pubs.aip.org
academic.oup.com
royalsocietypublishing.org
onlinelibrary.wiley.com
www.cambridge.org
ieeexplore.ieee.org
www.mdpi.com
```

**What to expect after saving:**
- **Shell tools** (the preflight and `lit_search.py`) see the change immediately.
- **Claude's WebFetch tool** only sees it in a new session.
- **Paywalls and bot walls remain.** Many publishers answer automated clients with 403s or bot-check redirects, and nearly everything is on arXiv anyway.
- **arXiv's API rate-limits shared cloud addresses.** INSPIRE indexes the same papers with their arXiv IDs.

### Permissions

`.claude/settings.json` pre-approves only what the agents need to avoid a prompt storm:
- `WebSearch`;
- `WebFetch` on any domain;
- running Python scripts under the skill's `scripts/` and under `runs/`;
- creating and writing files under `runs/`.

Everything else prompts as usual. Each workflow launch also asks for approval; choose "don't ask again" for a workflow to skip it next time.

### Tests

```
python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests   # tools + definition consistency
node --test .claude/skills/conundrum/scripts/tests/workflows.test.mjs     # orchestration, with a mock runtime
python3 .claude/skills/conundrum/scripts/gr_tensors.py selftest           # GR toolkit vs. known results
```

### Layout

```
.claude/
  skills/conundrum/
    SKILL.md
    references/          lenses.md  schemas.md  rubric.md
    scripts/             gr_tensors.py  lit_search.py  check_env.py  tests/
  agents/                16 role definitions (model, effort, tools, method)
  workflows/             conundrum-research.js  conundrum-analyze.js
  settings.json          permission allow-list
docs/conundrum-skill-plan.md
runs/                    one directory per investigation
```

### Known limitations of v1

- **Never run end to end yet.** It is tested offline: the tools, a mock-runtime run of both workflows, definition consistency, and one lens smoke-tested live. Your first real run is the real test, so start with `standard`.
- **Not yet in v1:**
  - pairwise judging in deep mode;
  - the persona-vs-neutral evaluation from plan §5.8;
  - a non-Claude critic such as GPT-6 Astra.
- **Cost figures are estimates** until measured.
