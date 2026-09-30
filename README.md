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
   - Python 3.10+ with `pip install sympy numpy scipy pypdf cffi`. `pypdf` lets agents quote PDFs verbatim. `cffi` is there because some system Python packages (a broken `cryptography`) otherwise make `pypdf` crash on import; the preflight reports this.
2. **Start a new Claude Code session in this repo.** Claude Code loads the skill, agents and workflows at session start.
3. **Run the skill:**
   ```
   /conundrum standard Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?
   ```
4. **Confirm the brief,** which is Claude's precise restatement of your question.
5. **Review the dossier** after the research stage, and add anything you know.
6. **Confirm the analysis stage,** then read `runs/<slug>/report.md`.

### Depth and cost

| Depth | What runs | Agent runs | Rough time | Cost at API list prices |
|---|---|---|---|---|
| `quick` | 3 researchers, 3 lenses, 1 refuter per candidate, Opus judge | ~18 | 1–2 hours | ~$25–40 (measured once: $29) |
| `standard` | 4 researchers with source checks, 5 lenses with math checks, 1 refuter per candidate, Fable judge | ~30 | ~2.5 hours | ~$35–50 (measured once: $39) |
| `deep` | 5 researchers with checks, 6–7 lenses with math checks, 3 refuters per candidate with different angles, rebuttal round, Fable judge at max effort | ~45–62 | 4–5 hours | ~$55–90 |

Times include the two checkpoints where the pipeline waits for you. The measured standard run took about 2.5 hours in a cloud session running only 2 agents at once; see [Where to run it](#where-to-run-it).

**Measured runs**, both in cloud sessions on 2026-09-29:

| | Quick: Alcubierre drives | Standard: the problem of time |
|---|---|---|
| Total at list prices | $28.72 | $38.64 |
| Agents / main session | $21.92 / $6.79 | $33.23 / $5.41 |
| Spent re-running agents after interruptions | ~$3.40 (a usage-limit stop and a container restart) | ~$1.80 (a container restart) |

Per agent in the standard run:
- researchers ~$0.45–0.85, source checkers ~$0.10–0.20, the dossier ~$0.95;
- lenses ~$1.05–2.55, math checks ~$0.60–1.55;
- a calculator built on demand ~$1.80;
- the slate ~$2.35, refuters ~$0.65–1.05, the Fable judge ~$2.70, the audit ~$0.15.

The deep figures are extrapolated from these runs. `python3 dev/run_costs.py` measures a run from Claude Code's transcripts, per agent.

**What the fixes bought.** Before the toolkit fixes and the no-polling rule, a smoke test of the constraints lens cost ~$12.70 over 64 turns (see [`examples/`](examples/smoke-test-constraints-lens/)). Most of that went on waiting for slow calculations and on re-reading a context that grew to 394k tokens. In the measured run, the same lens cost ~$2.50.

Cache reads count against plan usage at the cached rate, so the API list price is a rough proxy for how much of your window a run uses. `/workflows` shows live token counts and lets you stop a run. Afterwards `/usage` attributes usage to subagents and flags cache misses, and `dev/run_costs.py` prices each agent at API list prices.

### Where to run it

A workflow runs at most min(16, CPUs − 2) agents at once. The preflight prints the number for your machine.

| | Local terminal on your computer | Cloud session (claude.ai/code, or started from the app) |
|---|---|---|
| Agents at once | Typically 6–14 on an 8–16-core machine | 2, as the container has 4 CPUs. The measured standard run still took about 2.5 hours; a deep run, with about twice the agents, will feel the limit more |
| Hitting your usage limit | The run waits for the reset and continues by itself, up to twice per run (interactive session, v2.1.271 or later) | Probably fails the agents that hit it: the docs exclude SDK and background sessions from the pause. Relaunch after the reset |
| Run files | Stay on your disk | Lost if not pushed before the container is reclaimed; the skill offers to push after each stage |
| Literature access | Full web access | Allowlisted hosts only; WebFetch sees changes only in a new session |
| Your computer | Must stay awake for the whole run | Can be off; start and follow it from your phone |

Token cost is the same either way. Local is the more robust choice when a computer can stay on for a few hours. `claude remote-control`, run in the project folder, lets you follow a local session from the Claude app. The docs list Remote Control sessions among those that don't pause at the usage limit, though, so a long run is safest in a plain terminal session.

The stages hand over through files, so they can also change machines. For example, frame and research in the cloud, push, pull, then run the analysis locally.

### Your first local run

1. **Get the code and a current Claude Code.** Clone the repo, or `git pull` in your copy, and stay on `main`. Run `claude update`: a workflow waits out a usage limit only from version 2.1.271.
2. **Install and check the Python side:**
   ```
   pip install sympy numpy scipy pypdf cffi
   python3 .claude/skills/conundrum/scripts/check_env.py
   ```
   The preflight should show every package working, the literature sources reachable, and at least 5 agents at once.
3. **Turn on the sandbox (recommended).** Agents write Python scripts and run them, and `.claude/settings.json` pre-approves that, so on your computer those scripts run as you. In the sandbox, shell commands:
   - can write only inside the project and temp folders, and never into `.claude/skills`, `agents`, `hooks` or `workflows`, the settings files or `.git` hooks;
   - reach only allowed hosts. A command that needs a new host asks you first; in auto mode, Claude names the hosts on the command instead;
   - can still read the rest of your disk, `~/.ssh` included, so the host list is what keeps data from leaving. `sandbox.filesystem.denyRead` can hide folders.

   WebSearch and WebFetch run inside Claude Code, outside the sandbox, under their usual permission rules. The sandbox runs on macOS, Linux and WSL2; on Windows, run Claude Code inside WSL2.

   Turn it on with `/sandbox`, choosing the mode that runs sandboxed commands without asking. Then pre-allow the literature hosts in `.claude/settings.local.json`, which stays out of git; create the file or add to it:
   ```json
   {
     "sandbox": {
       "enabled": true,
       "network": {
         "allowedDomains": ["arxiv.org", "*.arxiv.org", "inspirehep.net", "doi.org", "dx.doi.org",
           "api.crossref.org", "api.semanticscholar.org", "www.semanticscholar.org", "www.osti.gov",
           "ui.adsabs.harvard.edu", "ntrs.nasa.gov", "*.aps.org", "iopscience.iop.org", "link.springer.com",
           "www.sciencedirect.com", "www.nature.com", "www.science.org", "pubs.aip.org", "academic.oup.com",
           "royalsocietypublishing.org", "onlinelibrary.wiley.com", "www.cambridge.org", "ieeexplore.ieee.org",
           "www.mdpi.com"]
       }
     }
   }
   ```
4. **Start a fresh session in a plain terminal.** Run `claude` in the project folder, not `claude remote-control`: the docs exclude Remote Control sessions from the usage-limit wait. A fresh session keeps the run's transcript separate, which step 7 reads. Start early in a usage window, and keep the computer awake: on macOS, `caffeinate -i claude`; on Linux, `systemd-inhibit claude`.
5. **Start small.** Run `/conundrum quick <your question>` first: about 16 agents and 1–2 hours. Move to `standard` once it has run cleanly.
6. **Watch it.** `/workflows` shows each agent's progress. Note any permission prompt and any agent that reports a `[pipeline guard]` refusal; each one points at a rule to fix.
7. **Measure it.** When it's done, run `python3 dev/run_costs.py` in the project folder, or type `! python3 dev/run_costs.py` in the session. It prints each agent's turns, tokens and cost at list prices: the numbers the estimates above still lack.

### If a run is cut off

| Cut | What is lost | What survives |
|---|---|---|
| An agent reaches its turn limit | Whatever it hadn't written to its file. Its reasoning isn't stored in a usable form, so the file is its only memory | Its file, and every completed agent's saved result |
| Your usage limit, in a local interactive subscription session | Nothing: waiting agents continue after the reset, up to two waits per run | Everything |
| Your usage limit, in a background or cloud session | The in-flight work of the agents that hit it | Their files and every completed agent's result. Relaunch after the reset |
| A cloud container reclaimed after inactivity | Every file you didn't push | The workflow's saved results, so a relaunch trusts agents whose files are gone. Push `runs/<slug>/` after each stage |

Agents append findings to their files as they go, in the same step as their next tool call, so a cut costs a few turns of work and a checkpoint costs output tokens, not an extra turn. A relaunched agent that finds its file continues from it. A relaunch replays saved results only up to the first agent that didn't finish, in the order the agents were started, and reruns everything after it. So the workflows start agents in a fixed order, whichever finishes first, with the calculation-heavy lenses last.

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
| `math/*.md` | Standard and deep runs: an independent check of each lens's mathematics, with the check scripts and their logs in `math/<lens>/` |
| `candidates.md` | The competing answers, each with its decisive test |
| `verdicts/*.md` | The refutation attempts, each grounded in a calculation, a quote or an inconsistency |
| `report.md` | The ranked answers with credences: in principle vs. in practice, orders-of-magnitude gaps, what would change the verdict |
| `audit.md` | Every claim in the report traced to the evidence |
| `calc/*.py` | Every calculation the agents ran, so you can rerun them |
| `prior/<run>/` | Evidence copied from earlier runs you approved, with a `PROVENANCE.md` saying how it may be used |
| `run.json` | The run's record for later runs: date, question, status, bottom line, and your notes on how far to trust it |

### Building on earlier runs

At framing, Claude looks for earlier runs related to your question and proposes how to treat each one:

| Mode | What the new run gets | Default for |
|---|---|---|
| **ignore** | Nothing; agents never see it | Runs you marked distrusted, and independent re-checks |
| **leads** | Its research notes and dossier, as pointers to sources. Nothing counts until a researcher finds and quotes it again | Runs that never finished or were never source-checked, and older runs in fast-moving fields |
| **update** | Also its calculation scripts. Claims that re-verify carry over, labelled with the run and its date, and researchers look for newer work | Complete, source-checked runs |

Overrule it in plain words: "I don't trust that research, get it fresh", or "that's six months old in a fast-moving field, discount it".

**Conclusions never carry over.** An earlier run's analyses, candidates, verdicts, report and audit stay behind, so the lenses and the judge reason from the new evidence alone. After the new report is written, Claude compares the two and adds a "What changed since <run>" section.

**The pipeline remembers what you decide:**
- Each finished run gets a `run.json` record.
- Say you don't trust a run, and it is marked distrusted; later runs ignore it without asking. By hand: `python3 .claude/skills/conundrum/scripts/prior_runs.py mark <run> --trust distrusted --note "<why>"`, and `--trust ok` undoes it.
- Caveats about a run, such as "the plot values were read by eye", are kept as notes and shown to the researchers who use it.
- A newer run of the same question marks the older one superseded, so framing offers the latest.

### How it works

```
/conundrum ─ frame the brief with you
  └ workflow conundrum-research: researchers (Sonnet) → source checkers → dossier (Opus)
  ─ checkpoint: you review the dossier and approve the lenses
  └ workflow conundrum-analyze: lenses (Opus) → [math checks] → candidate slate → refuters → [rebuttals] → judge (Fable) → audit
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

**Question types.** Framing classifies the question as feasibility, design, mechanism, anomaly or foundations, which sets the default lenses.
- Foundations questions, such as the problem of time or the interpretations of quantum mechanics, get positions instead of options.
- Positions are judged on internal consistency, on what each gives up, and on whether any observation could tell them apart.
- Where positions are empirically equivalent, the judge ranks them by what they give up and says so, instead of inventing probabilities.
- Anomaly questions get candidates that each name the dominant cause of a discrepancy: a systematic in one method, a kind of new physics, or the null (a fluctuation, or uncertainties underestimated across experiments). The slate adds a prediction matrix of what each candidate predicts for every independent class of measurement. Deep refuters attack each candidate's magnitude, its evidence and the independent bounds it must meet. The judge must check each explanation's size and sign against the gap, keep an explicit "unidentified" share within a method, and name the deciding measurement with who and when.

**Math checks.** In standard and deep runs, each lens's analysis goes straight to a math checker, an Opus agent that re-derives the analysis's load-bearing mathematics from scratch. It never reuses the lens's scripts.
- Each claim is checked with SymPy, then numerically at 50 points to 30 digits, including the domain's ends, plus a limit and the units.
- Each claim is marked verified, refuted (with a counterexample) or unverified in `math/<lens>.md`, with a log for every verdict.
- Refuted math can't support a candidate. The refuters can cite it, and the judge and auditor weigh it.

Formal proofs in Lean are planned, not built; [`docs/formal-math-plan.md`](docs/formal-math-plan.md) explains why they come second.

**Physics tooling.** `gr_tensors.py` computes the stress-energy a metric requires and what every observer measures. It also covers:
- energy-condition scans with Hawking–Ellis classification;
- total, negative and positive energy on a slice;
- curvature radii;
- Ford–Roman quantum-inequality bounds and Lorentzian averaging;
- horizon finding and Hawking temperatures;
- high-precision rechecks of surprising signs.

It is tested against Schwarzschild, FRW, Morris–Thorne, Painlevé–Gullstrand and Alcubierre closed forms. The other calculators:
- `stats_tools.py` gives the statistics lens tested significance, look-elsewhere, counting-experiment and Bayes-factor calculations, plus the tools for disagreeing methods: tension with asymmetric errors, chi-squared within and between methods, and the data or precision a decisive test needs when systematics set a floor;
- `unit_tools.py` parses, converts and dimension-checks quantities such as `"0.5 * 1 t * (3 km/s)^2"`;
- `rocket_tools.py` covers classical and relativistic rocket equations and constant-acceleration trips.

Each checks itself against independent reference values, and `references/tools.md` catalogs them all.

`lit_search.py` prints abstracts the agents can quote, from four sources:
- INSPIRE-HEP and arXiv, the default for physics;
- Crossref and Semantic Scholar (`--source general`) for engineering, materials, chemistry, statistics and other fields.

Results come best match first; `--since <year>` restricts every source to recent work, and `"refersto:arxiv:<id>"` lists the papers citing a result, which is how re-analyses and rebuttals turn up. Semantic Scholar also lists open-access PDF links. `fetch_text.py` prints a source's own words from a PDF or web page, around a phrase given with `--grep`, so agents quote the text itself: WebFetch passes pages through a model, whose answer can paraphrase. Two optional environment variables speed these up; nothing identifying is sent unless you set them:
- `SEMANTIC_SCHOLAR_API_KEY` raises Semantic Scholar's shared rate limit;
- `CROSSREF_MAILTO` gives Crossref an email address for its faster pool.

**Calculators on demand.** At framing, Claude checks the calculations a question needs against the catalog. If several agents would need one that's missing and easy to get wrong, Claude proposes it with the brief. On your OK:
1. A toolsmith agent builds it during the research stage, with a self-test against at least four independent reference values.
2. At the dossier checkpoint, Claude re-runs the self-test and checks the references.
3. Claude then promotes it into the shared toolkit, so future runs have it too.

Agents never write straight into the toolkit; promotion is a step you see.

### Network access

- **Local runs** have full web access. In the sandbox, shell commands reach only the hosts you allow; see [Your first local run](#your-first-local-run).
- **Claude Code on the web** may block literature sites under the environment's network policy. The preflight reports which sources are reachable. Blocked research falls back to INSPIRE abstracts and WebSearch summaries. Summaries are written by a model, not the source, so the pipeline labels them `search-summary` and weighs them down.

**To open it up.** The Android app can't edit environments, so use claude.ai/code in a browser or the Desktop app.
1. Click the cloud button showing the environment name (e.g. **Default**) above the message box.
2. Hover over the environment and click its gear icon.
3. Set **Network access** to **Custom**, paste the list below, and tick **Also include default list of common package managers** (PyPI).
4. Add `pip install sympy numpy scipy pypdf cffi` to **Setup script**; new sessions run it.

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

It also registers two hooks: the turn-budget hook above, and the pipeline guard.

**The pipeline guard.** Agents read arbitrary web pages and PDFs, so a hostile page could try to talk one into editing the toolkit, the agent definitions or the hooks. `.claude/hooks/guard_pipeline.py` stops the pipeline's own agents from changing the pipeline:
- They may write only under `runs/` and temp files.
- Their shell commands can't write into `.claude/`, `.git/`, `CLAUDE.md` or `~/.claude/`.
- They can run git only read-only.

The main conversation isn't affected; that's how calculators get promoted. The shell checks are best-effort, since code that builds a path at run time can slip past them. So each checkpoint also runs `git status` on those paths, and stops if anything changed that the main session didn't change.

Everything else prompts as usual. Each workflow launch also asks for approval; choose "don't ask again" for a workflow to skip it next time.

### Tests

```
python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests   # tools, hooks, dev scripts, definition consistency
node --test .claude/skills/conundrum/scripts/tests/workflows.test.mjs     # orchestration, with a mock runtime
python3 .claude/skills/conundrum/scripts/gr_tensors.py selftest           # GR toolkit vs. known results
python3 .claude/skills/conundrum/scripts/stats_tools.py selftest          # statistics toolkit vs. reference values
python3 .claude/skills/conundrum/scripts/unit_tools.py selftest           # units vs. exact SI and IAU definitions
python3 .claude/skills/conundrum/scripts/rocket_tools.py selftest         # rocket equations vs. closed forms and the 1 g table
python3 .claude/skills/conundrum/scripts/math_checks.py selftest          # math checks vs. known identities, limits and expansions
```

### Layout

```
.claude/
  skills/conundrum/
    SKILL.md
    references/          lenses.md  schemas.md  rubric.md  tools.md (calculator catalog)
    scripts/             gr_tensors.py  stats_tools.py  unit_tools.py  rocket_tools.py
                         math_checks.py  math_run.py
                         lit_search.py  fetch_text.py  check_env.py  prior_runs.py  tests/
  agents/                19 role definitions (model, effort, tools, method)
  workflows/             conundrum-research.js  conundrum-analyze.js
  hooks/                 turn_budget.py (counts each agent's turns and tool calls)
                         guard_pipeline.py (keeps pipeline agents from editing the pipeline)
  settings.json          permission allow-list and hook registration
dev/                     agent_rules.py (the single source of every agent's ground rules: edit there, then run it)
                         run_costs.py (a run's turns, tokens and cost per agent, from the transcripts)
docs/                    conundrum-skill-plan.md (the design)  formal-math-plan.md (math checks and Lean)
examples/                smoke-test output of one lens, with provenance notes
runs/                    one directory per investigation
```

### Known limitations of v1

- **Two runs so far.** A quick run on the Alcubierre question completed end to end on 2026-09-29.
  - It exposed one blocker, now fixed. Claude Code refused the judge's write to `report.md`, because it blocks subagents from writing files named `report*.md`. The judge now returns the report as text, and the main session saves it.
  - A standard run on the problem of time followed. It exercised the math checks, the foundations type, a calculator built on demand, and the returned report, with no refusals.
- **What the smoke test fixed.** The constraints lens produced a sound, calculation-backed analysis (see [`examples/`](examples/smoke-test-constraints-lens/)). It also exposed problems, now fixed:
  - a toolkit bug that passed the weak energy condition where it fails;
  - quoting search summaries as if they were source text;
  - an agent that could run out of turns before writing its file;
  - an agent that killed its own shell with `pkill -f`.
- **Deep runs are unmeasured.** Their cost and time are extrapolated from one quick and one standard run.
- **A turn-capped workflow agent's return value is undocumented.** The scripts treat a missing or `ok: false` result as a failure. Check `/workflows` on the first real run, and read the run's `journal.jsonl` if a result looks empty.
- **Agents are told, not forced, to stay in their own run's folder.** Material from earlier runs reaches them through `prior/`, but no hook stops an agent from opening another run's files. The dossier's source notes count the claims carried from earlier runs, and the auditor traces every report claim to this run's evidence.
- **Search summaries are weak evidence.** Where WebFetch can't reach papers, claims rest on INSPIRE abstracts and search summaries. The auditor flags report claims that rest only on summaries.
- **Not yet in v1:**
  - pairwise judging in deep mode;
  - the persona-vs-neutral evaluation from plan §5.8;
  - a non-Claude critic such as GPT-6 Astra.
