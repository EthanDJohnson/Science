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
   - Python 3.10+ with `pip install sympy numpy pypdf cffi`. `pypdf` lets agents quote PDFs verbatim. `cffi` is there because some system Python packages (a broken `cryptography`) otherwise make `pypdf` crash on import; the preflight reports this.
2. **Start a new Claude Code session in this repo.** Claude Code loads the skill, agents and workflows at session start.
3. **Run the skill:**
   ```
   /conundrum standard Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?
   ```
4. **Confirm the brief,** which is Claude's precise restatement of your question.
5. **Review the dossier** after the research stage, and add anything you know.
6. **Confirm the analysis stage,** then read `runs/<slug>/report.md`.

### Depth and cost

| Depth | What runs | Agent runs | Rough time | Rough cost at API list prices |
|---|---|---|---|---|
| `quick` | 3 researchers, 3 lenses, 1 refuter per candidate, Opus judge | ~16 | 1–2 hours | ~$35–60 |
| `standard` | 4 researchers with source checks, 5 lenses, 1 refuter per candidate, Fable judge | ~23 | 1.5–3 hours | ~$45–90 |
| `deep` | 5 researchers with checks, 6–7 lenses, 3 refuters per candidate with different angles, rebuttal round, Fable judge at max effort | ~40–50 | 3–5 hours | ~$100–180 |

Times exclude the two checkpoints where the pipeline waits for you. They also assume at least 5 agents can run at once; see [Where to run it](#where-to-run-it). The costs are extrapolated from two measured agents, not from a full run:

| Measured agent | Turns | Cost at API list prices | Time |
|---|---|---|---|
| Constraints lens (Opus, before the fixes; see [`examples/`](examples/smoke-test-constraints-lens/)) | 64 | ~$12 | 73 min |
| Researcher (Sonnet), one narrow facet | 44 | ~$0.90 | 8 min |

Where the lens's money went:
- **31%** waiting on slow calculations, including two cache expiries that each cost about $1;
- **29%** on one long planning burst, the cache rewrite it triggered, and carrying it through every later turn;
- **43%** in its last 24 turns, because every turn re-reads the whole context, which grew from 145k to 394k tokens.

The toolkit fixes and the no-polling rules target the first item. The harness reported "409k tokens" for that agent, but that is its final context size. It processed about 15.8M tokens, 93% of them cache reads.

Cache reads count against plan usage at the cached rate, so the API list price is a rough proxy for how much of your window a run uses. `/workflows` shows live token counts and lets you stop a run. Afterwards `/usage` attributes usage to subagents and flags cache misses.

### Where to run it

A workflow runs at most min(16, CPUs − 2) agents at once. The preflight prints the number for your machine.

| | Local terminal on your computer | Cloud session (claude.ai/code, or started from the app) |
|---|---|---|
| Agents at once | Typically 6–14 on an 8–16-core machine | 2: the container has 4 CPUs, so a standard run takes about 2× as long and a deep run 3–4× |
| Hitting your usage limit | The run waits for the reset and continues by itself, up to twice per run (interactive session, v2.1.271 or later) | Probably fails the agents that hit it: the docs exclude SDK and background sessions from the pause. Relaunch after the reset |
| Run files | Stay on your disk | Lost if not pushed before the container is reclaimed; the skill offers to push after each stage |
| Literature access | Full web access | Allowlisted hosts only; WebFetch sees changes only in a new session |
| Your computer | Must stay awake for the whole run | Can be off; start and follow it from your phone |

Token cost is the same either way. Local is the more robust choice when a computer can stay on for a few hours. `claude remote-control`, run in the project folder, lets you follow a local session from the Claude app. The docs list Remote Control sessions among those that don't pause at the usage limit, though, so a long run is safest in a plain terminal session.

The stages hand over through files, so they can also change machines. For example, frame and research in the cloud, push, pull, then run the analysis locally.

### If a run is cut off

| Cut | What is lost | What survives |
|---|---|---|
| An agent reaches its turn limit | Whatever it hadn't written to its file. Its reasoning isn't stored in a usable form, so the file is its only memory | Its file, and every completed agent's saved result |
| Your usage limit, in a local interactive subscription session | Nothing: waiting agents continue after the reset, up to two waits per run | Everything |
| Your usage limit, in a background or cloud session | The in-flight work of the agents that hit it | Their files and every completed agent's result. Relaunch after the reset |
| A cloud container reclaimed after inactivity | Every file you didn't push | The workflow's saved results, so a relaunch trusts agents whose files are gone. Push `runs/<slug>/` after each stage |

Agents append findings to their files as they go, in the same step as their next tool call, so a cut costs a few turns of work and a checkpoint costs output tokens, not an extra turn. A relaunched agent that finds its file continues from it. A relaunch also reruns a failed agent and every agent that started after it, so the calculation-heavy lenses start last.

**Turn counting.** Agents can't count their own turns reliably, so a hook counts for them: `.claude/hooks/turn_budget.py`, registered in `.claude/settings.json`. It runs once per agent turn (`PostToolBatch`) and costs no tokens. Only when a threshold is crossed does it add a one-line `[turn budget]` reminder to that agent's context:
- every 10 tool calls, with a nudge to append settled findings;
- at the first-draft call, for agents that write one document;
- at the top of the call budget;
- on each of the last 5 turns before the cutoff.

It reads each agent's budget from its definition file and ignores the main conversation and every other agent.

### What you get

Everything lands in `runs/<slug>/`:

| File | What it is |
|---|---|
| `brief.md` | The question made precise: definitions, admissible physics, premises to test |
| `research/*.md` | Sourced claims per facet, each with a verbatim quote, or a labelled search summary when the source couldn't be opened; `*.check.md` holds the source-check verdicts |
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
| Statistician | is the signal real? significance, look-elsewhere effect, prior odds (anomaly questions) |

The philosopher labels in the agent files are mnemonics; the methods are the content.

**Physics tooling.** `gr_tensors.py` computes the stress-energy a metric requires and what every observer measures. It also covers:
- energy-condition scans with Hawking–Ellis classification;
- total, negative and positive energy on a slice;
- curvature radii;
- Ford–Roman quantum-inequality bounds and Lorentzian averaging;
- horizon finding and Hawking temperatures;
- high-precision rechecks of surprising signs.

It is tested against Schwarzschild, FRW, Morris–Thorne, Painlevé–Gullstrand and Alcubierre closed forms. `stats_tools.py` gives the statistics lens tested significance, look-elsewhere, counting-experiment and Bayes-factor calculations. `lit_search.py` prints abstracts the agents can quote, from four sources:
- INSPIRE-HEP and arXiv, the default for physics;
- Crossref and Semantic Scholar (`--source general`) for engineering, materials, chemistry, statistics and other fields.

Semantic Scholar also lists open-access PDF links. `fetch_text.py` prints a source's own words from a PDF or web page, around a phrase given with `--grep`, so agents quote the text itself: WebFetch passes pages through a model, whose answer can paraphrase. Two optional environment variables speed these up; nothing identifying is sent unless you set them:
- `SEMANTIC_SCHOLAR_API_KEY` raises Semantic Scholar's shared rate limit;
- `CROSSREF_MAILTO` gives Crossref an email address for its faster pool.

### Network access

- **Local runs** have full web access.
- **Claude Code on the web** may block literature sites under the environment's network policy. The preflight reports which sources are reachable. Blocked research falls back to INSPIRE abstracts and WebSearch summaries. Summaries are written by a model, not the source, so the pipeline labels them `search-summary` and weighs them down.

**To open it up.** The Android app can't edit environments, so use claude.ai/code in a browser or the Desktop app.
1. Click the cloud button showing the environment name (e.g. **Default**) above the message box.
2. Hover over the environment and click its gear icon.
3. Set **Network access** to **Custom**, paste the list below, and tick **Also include default list of common package managers** (PyPI).
4. Add `pip install sympy numpy pypdf cffi` to **Setup script**; new sessions run it.

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
api.crossref.org
api.semanticscholar.org
www.semanticscholar.org
```

**What to expect after saving:**
- **Shell tools** (the preflight and `lit_search.py`) see the change immediately.
- **Claude's WebFetch tool** only sees it in a new session.
- **Paywalls and bot walls remain.** Many publishers answer automated clients with 403s or bot-check redirects, and nearly everything is on arXiv anyway.
- **arXiv's API rate-limits shared cloud addresses.** INSPIRE indexes the same papers with their arXiv IDs.
- **Semantic Scholar rate-limits requests without an API key.** The tool retries with backoff. A free key (see above) avoids most of it.

### Permissions

`.claude/settings.json` pre-approves only what the agents need to avoid a prompt storm:
- `WebSearch`;
- `WebFetch` on any domain;
- running Python scripts under the skill's `scripts/` and under `runs/`;
- creating and writing files under `runs/`.

It also registers the turn-budget hook above. Everything else prompts as usual. Each workflow launch also asks for approval; choose "don't ask again" for a workflow to skip it next time.

### Tests

```
python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests   # tools + definition consistency
node --test .claude/skills/conundrum/scripts/tests/workflows.test.mjs     # orchestration, with a mock runtime
python3 .claude/skills/conundrum/scripts/gr_tensors.py selftest           # GR toolkit vs. known results
python3 .claude/skills/conundrum/scripts/stats_tools.py selftest          # statistics toolkit vs. reference values
```

### Layout

```
.claude/
  skills/conundrum/
    SKILL.md
    references/          lenses.md  schemas.md  rubric.md
    scripts/             gr_tensors.py  stats_tools.py  lit_search.py  fetch_text.py  check_env.py  tests/
  agents/                17 role definitions (model, effort, tools, method)
  workflows/             conundrum-research.js  conundrum-analyze.js
  hooks/                 turn_budget.py (counts each agent's turns and tool calls)
  settings.json          permission allow-list and hook registration
docs/conundrum-skill-plan.md
examples/                smoke-test output of one lens, with provenance notes
runs/                    one directory per investigation
```

### Known limitations of v1

- **Never run end to end yet.** It is tested offline: the tools, a mock-runtime run of both workflows, and definition consistency. One lens was also smoke-tested live. Your first real run is the real test, so start with `standard`.
- **What the smoke test fixed.** The constraints lens produced a sound, calculation-backed analysis (see [`examples/`](examples/smoke-test-constraints-lens/)). It also exposed problems, now fixed:
  - a toolkit bug that passed the weak energy condition where it fails;
  - quoting search summaries as if they were source text;
  - an agent that could run out of turns before writing its file;
  - an agent that killed its own shell with `pkill -f`.
- **Cost and time are extrapolated** from two measured agents until a full run is measured.
- **A turn-capped workflow agent's return value is undocumented.** The scripts treat a missing or `ok: false` result as a failure. Check `/workflows` on the first real run, and read the run's `journal.jsonl` if a result looks empty.
- **Search summaries are weak evidence.** Where WebFetch can't reach papers, claims rest on INSPIRE abstracts and search summaries. The auditor flags report claims that rest only on summaries.
- **Not yet in v1:**
  - pairwise judging in deep mode;
  - the persona-vs-neutral evaluation from plan §5.8;
  - a non-Claude critic such as GPT-6 Astra.
