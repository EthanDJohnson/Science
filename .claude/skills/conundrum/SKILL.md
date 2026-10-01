---
name: conundrum
description: Multi-agent investigation of a hard physics or engineering question (feasibility, design, mechanism or anomaly). Partitioned literature research, a source-checked dossier, independent method lenses, competing candidate answers, calculation-grounded falsification, and a neutral adjudicated report. Expensive (roughly 15 to 60 agent runs over 1 to 5 hours); runs only when invoked as /conundrum.
argument-hint: "[quick|standard|deep] <question>"
disable-model-invocation: true
---

# /conundrum

You coordinate a multi-agent investigation. Two saved workflows do the heavy lifting. Your job is framing, two checkpoints with the user, and presenting the result. Never skip a checkpoint, and never start a workflow before the user has confirmed.

Arguments: $ARGUMENTS
- If the first word is `quick`, `standard` or `deep`, that is the depth and the rest is the question. The default depth is `standard`.
- If the rest is the path of an existing `runs/<slug>/brief.md`, resume that run instead of framing a new one.

Reference files, all in `.claude/skills/conundrum/references/`:
- `schemas.md`: file formats;
- `lenses.md`: lens catalog and selection rules;
- `rubric.md`: how the judge weighs evidence;
- `tools.md`: the tested calculators in the shared toolkit.

## 0. Preflight

Run `python3 .claude/skills/conundrum/scripts/check_env.py`.
- **Few agents at once:** if it notes that only a few agents run at once, mention it. The time estimates below assume 2 at once, as in the measured runs; a machine with more CPUs runs faster.
- **Required package missing:** ask whether to install it (`pip install sympy numpy scipy`) before continuing. The physics calculations depend on it, and agents' scripts often use scipy.
- **Literature sources blocked:** tell the user in one line that research will lean on search summaries and INSPIRE abstracts, which the pipeline marks and weighs down. Continue unless they want to fix network access first.

Then check that WebFetch itself can read papers: WebFetch `https://arxiv.org/abs/gr-qc/0009013` and ask for the title.
- **WebFetch fails with EGRESS_BLOCKED while `check_env.py` shows arxiv.org reachable:** the environment's network settings changed after this session started. WebFetch picks them up only in a new session. Tell the user so. They can continue, with research leaning on `lit_search` abstracts and search summaries, or start a new session first.

## 1. Frame the question with the user

1. **Create the run directory.** Build a slug from today's date (`date +%F`) plus a 3–6 word kebab-case summary, for example `2026-09-29-alcubierre-negative-energy`. Create `runs/<slug>/`.
2. **Classify the question** as `feasibility`, `design`, `mechanism`, `anomaly` or `foundations`, using `lenses.md`. Foundations questions are about consistency and interpretation, such as the problem of time or the interpretations of quantum mechanics.
3. **Look for earlier runs.** Run `python3 .claude/skills/conundrum/scripts/prior_runs.py list "<question>"`. It lists earlier runs that share the question's key terms, best match first. For each it gives the age, whether its sources were checked, the user's notes and a suggested mode. For each run that bears on this question, settle on one mode:
   - **ignore:** agents never see it. Use it for an independent re-check.
   - **leads:** its notes only point researchers at sources; nothing counts until it is found and quoted again. The default for a run that never finished or was never source-checked, and for an older run in a fast-moving field.
   - **update:** claims that re-verify carry over, labelled with the run and its date, and researchers look for newer work. The default for a complete, source-checked run.

   Runs the user marked distrusted, and runs a newer one superseded, are ignored without asking; name them in one line. No mode ever passes an earlier run's analyses, verdicts or report to the agents. If an earlier run asked the same question, start the brief from its definitions, and tell the user what you changed.
4. **Draft `runs/<slug>/brief.md`** in the brief format. Do the thinking the user would want done up front:
   - **Define every loaded term.** For example, "superluminal effective speed" relative to which observers; "negative energy" meaning which energy density, measured by whom.
   - **State the admissible physics.** The default is established GR plus QFT, including semiclassical gravity. Speculative extensions are allowed only when labelled.
   - **State the horizon for "viable":** in principle, and in practice within a stated time.
   - **List the hidden premises worth testing.**
   - **Say what a useful answer looks like.**
   - **Scope the research facets** under `## Research facets`, for the facets this depth runs (quick: theory, quantitative, critiques; standard adds engineering; deep adds frontier): one line per facet saying what it owns for this question and what it leaves to the others, so each experiment, effect or topic has one owner and the researchers don't chase the same papers. For an anomaly, `engineering` covers the measurements themselves: each experiment's method and systematic error budget, statistical and systematic uncertainties kept apart, results that supersede others, and the experiments planned or running (who, target precision, when). `quantitative` covers the related quantities and Standard Model inputs, `critiques` the proposed explanations and the searches and bounds against them, and `frontier` the last few years' results, talks and proposals, newest first. At quick depth, which has no engineering facet, give the error budgets to `quantitative`.
   - **Name the owner of each worked calculation** the question needs, under `## Worked calculations`: for example, the statistician combines the measurements and computes the tension. The owner must do it, and its result is the reference the slate builder, the refuters and the judge use. Lenses run at the same time and can't read each other, so another lens that needs the number computes its own and says so.
   - **List the earlier runs** under `## Prior runs`, with the mode you propose for each and why.
5. **Check for calculator gaps.** List the calculations the question will need, for example relativistic travel times, Casimir energies, heat rejection, orbital transfers, or a relation between measured constants that several agents will use (a lifetime from couplings with radiative corrections, say). Compare them with `tools.md`.
   - **Propose a new calculator only for a calculation several agents will need and that is easy to get subtly wrong.** One-off arithmetic doesn't qualify; agents write that in their own scripts.
   - **For each one, give a snake_case name not already in the toolkit,** and a one-line purpose saying what it must cover.
   - **Often there are none.** Say so and move on.
6. **Get the brief confirmed.** Show the user:
   - the question made precise;
   - the premises to test;
   - what counts as an answer;
   - the depth with its expected size;
   - any proposed calculators. Each costs roughly 2 US dollars at API prices and is built alongside the research;
   - the earlier runs, with the mode you propose for each and its reason.

   Ask them to confirm or correct it, and apply any corrections to `brief.md`. The user may overrule a mode in plain words, such as "I don't trust that research, get it fresh" (ignore) or "that's six months old in a fast-moving field, discount it" (leads).

   | depth | what runs | agent runs | rough time | rough cost at API list prices (US dollars) |
   |---|---|---|---|---|
   | quick | 3 researchers, no source checks, 3 lenses, 1 refuter per candidate, Opus judge | ~18 | 1–2 hours | ~25–40 |
   | standard | 4 researchers + checks, 5 lenses + math checks, 1 refuter per candidate, Fable judge | ~30 | ~2.5 hours | ~35–50 |
   | deep | 5 researchers + checks, 6–7 lenses + math checks, 3 refuters per candidate, crux round, Fable judge at max | ~45–62 | 4–5 hours | ~55–90 |

   Say that each depth has been measured once at list prices: quick 29 US dollars and standard 39 (both including reruns after interruptions), and deep 84 (61 agent runs with a full 8-candidate slate, no reruns). Times include the checkpoints; in a cloud session running 2 agents at once, the measured standard run took about 2.5 hours and the deep run about 4. On a subscription the run draws on usage limits instead. `/workflows` shows live token counts, and `/usage` afterwards attributes usage to subagents and flags cache misses.

   **A deep run in a cloud session on a subscription will probably cross a usage limit partway.** There, agents that hit the limit fail instead of waiting for the reset. Suggest launching the analyze stage at the start of a fresh usage window, or running it locally, where waiting agents continue after the reset; the stages hand over through files, so research can run in one place and analysis in another.

   Once the brief is confirmed, act on the earlier runs:
   - **Record what the user said about a run,** so later runs remember it. For distrust, run `prior_runs.py mark <run> --trust distrusted --note "<their reason>"`, and later runs ignore it without asking. A caveat, such as "the plot values were read by eye", goes in with `--note` alone.
   - **Copy in each leads or update run** with `prior_runs.py import <run> --into <slug> --mode <mode>`. It copies evidence, never conclusions, into `runs/<slug>/prior/<run>/`, with a `PROVENANCE.md` telling researchers how they may use it.

## 2. Research

Call the Workflow tool with `name: "conundrum-research"` and `args: {slug, depth, type, tools, prior}`. `type` is the question type from step 1; `tools` holds the confirmed calculators as `[{name, purpose}]`, and `prior` the brief's leads and update runs as `[{slug, mode}]`; leave either out if it is empty. Append `research <runId>` to `runs/<slug>/workflow-runs.txt` as soon as the launch returns: a relaunch needs the run ID (see "If something fails"). Every launch gets its own line, relaunches included, with the run ID that launch returned; resuming always uses the last line for its stage. The workflow runs in the background, so wait for its completion notification. If the result lists `missing` or `unchecked` facets, mention them at the checkpoint.

**In a cloud session, offer to commit and push `runs/<slug>/` now,** and again after step 4. The container is reclaimed after inactivity and unpushed files are lost, while a workflow's saved results survive, so a later relaunch would trust agents whose files no longer exist.

## 3. Checkpoint with the user

Read `runs/<slug>/dossier.md` and summarize it in 12 lines or fewer:
- the three facts the question depends on most;
- the key numbers;
- contested points;
- binding constraints;
- the share of claims resting only on search summaries;
- anything the source checks dropped or corrected;
- the papers flagged to request: no free copy was found, and the answer may turn on them. The user may be able to get them, for example by asking the authors. Never contact anyone yourself.

**Check that the pipeline itself is untouched.** Run `git status --short -- .claude CLAUDE.md .mcp.json`. Pipeline agents can't write there, because the pipeline guard hook blocks it. Any change you didn't make yourself means something got past the guard: stop, show the user `git diff` for those paths, and don't promote anything or continue until they decide.

**Promote the calculators that were built.** For each entry in the workflow result's `tools` with `ok: true`:
1. **Re-run its self-test yourself** with `python3 runs/<slug>/tools/<name>.py selftest`; don't rely on the toolsmith's report.
2. **Read its reference values.** Each must come from an independent source cited in a comment (a closed form, a definition, a published table), not from the code itself. At least one must be a limit where the model reduces to a simpler known law.
3. **If both hold, promote it.**
   - Copy it to `.claude/skills/conundrum/scripts/<name>.py` with `cp -n`; a sandboxed shell can't write into `.claude/skills/`, so there use the Write tool. Never overwrite an existing file; if the name is taken, ask the user.
   - In the copy, change each `runs/<slug>/tools` path (the docstring's usage examples) to `.claude/skills/conundrum/scripts`, so later agents run the toolkit copy, not a file in this run's folder. Then `diff` the run copy against the promoted one: only those lines, and any note you add, may differ.
   - Add its row to `tools.md`, noting "built in run <slug>".
   - Run `python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests`.
   - Tell the user what was added, and where to find its reference values. The lenses can use it in the analysis stage, and future runs find it in the toolkit.
4. **If anything fails,** leave it in the run folder, say what failed, and let the lenses do without it.

Then:
- **Ask for corrections or unpublished data,** and for any flagged paper the user can supply. Append them to the dossier under `## User-supplied`, marking each `[user]`. Save a supplied paper in `runs/<slug>/user/` and list its path there: agents read it with `fetch_text.py runs/<slug>/user/<file>`.
- **Choose lenses** with `lenses.md`, from type × depth. Show each one with a line on why. A deep run takes 6–7: the type's five plus the ones `lenses.md` adds at deep.
- **Offer a stop after the slate** when this project has never run this depth or question type before (check the `depth` and `type` in `runs/*/run.json`). The analyze stage then returns once the lenses, math checks and candidate slate are done, about half its cost in a deep run (two-thirds in a standard one), so the user can look at the candidates before the refuters and the judge run on them.
- **Confirm the user wants to continue.** This is the expensive half.

## 4. Analyze

Call the Workflow tool with `name: "conundrum-analyze"` and `args: {slug, depth, type, lenses}`, adding `stopAfter: "slate"` if the user took that offer, and wait for completion. Append `analyze <runId>` to `runs/<slug>/workflow-runs.txt` as soon as the launch returns.

**If the result says `stoppedAfter: "slate"`,** show the user `runs/<slug>/candidates.md`: its exclusivity line, each candidate's claim and decisive test, and for an anomaly its prediction matrix. Ask whether to continue. Then relaunch with the same args without `stopAfter`, plus `resumeFromRunId` from the last `analyze` line, and append the relaunch's own run ID as a new `analyze` line: if this relaunch is interrupted too, resuming from the earlier ID would rerun everything after the slate. The lenses, math checks and slate come back from saved results. If the user wants the slate changed, also pass their request as `slateNote`: the lenses and math checks are replayed, and only the slate is rebuilt. Resuming works only in this session.

**If any agents failed,** that is, if `lensesFailed`, `mathFailed`, `refutersFailed`, `cruxFailed` or `unexamined` is non-empty, or `audit` is null, tell the user which, before presenting anything, and offer a relaunch with `resumeFromRunId`. It reruns the first failed agent and every agent after it, and an agent whose file is marked `status: final` returns it unchanged. If `audit` is null, don't present audit flags: `audit.md` may be missing, unfinished, or the audit of an earlier report.

**Save the report first.** The result's `report` field holds the judge's report as text; write it verbatim to `reportPath` (`runs/<slug>/report.md`). The judge can't save it itself, because Claude Code blocks subagents from writing files named `report*.md`. If `reportIncomplete` is true, tell the user the judge didn't mark the report complete.

Then offer to commit and push `runs/<slug>/` again (see step 2).

## 5. Report

First check that the pipeline is still untouched, as at step 3: `git status --short -- .claude CLAUDE.md .mcp.json` should show only changes you made.

Read `runs/<slug>/report.md`, and `runs/<slug>/audit.md` if the workflow result's `audit` is not null.

**Compare with earlier runs.** For each run in the brief's `## Prior runs` that has a report and isn't marked distrusted, compare its ranked answers with this run's. Append `## What changed since <run>` to `report.md`, in 15 lines or fewer:
- answers that rose, fell, appeared or dropped out, with their credences;
- the new evidence behind each change, by dossier ID;
- anything the earlier run relied on that this run found superseded.

The judge never saw the earlier report, so this is the first comparison.

Present:
- the bottom line;
- the ranked-answers table;
- what changed since earlier runs, if you compared any;
- the top three decisive tests or calculations;
- every audit flag marked `unsupported` or `contradicted`, plus the count marked `weak`;
- the papers the report says the answer may turn on but no free copy exists for, so the user can decide whether to request them;
- the paths to `report.md`, `dossier.md` and `calc/`.

Don't restate the whole report; it is in the file.

**Record the run** with `python3 .claude/skills/conundrum/scripts/prior_runs.py record <slug>`. It writes `runs/<slug>/run.json`, which later runs read at framing, and marks any earlier run of the same question as superseded. If the user says how far to trust this run, add it with `prior_runs.py mark`.

## If something fails

- **A workflow stopped partway:** if it still shows as running, stop it first (TaskStop). Relaunch it with the same name and args, plus `resumeFromRunId` set to the run ID on the last line for that stage in `runs/<slug>/workflow-runs.txt`, and append the relaunch's own ID. Every agent before the first failed or unfinished one returns its saved result; that agent and every one after it run again, and a rerun agent whose file is marked `status: final` returns it unchanged. Resuming works only in the session that launched the workflow; in a new session everything reruns.
- **A workflow hit the usage limit:** in a local interactive session, waiting agents continue by themselves after the reset (up to two waits per run). In a background or cloud session the affected agents fail instead. After the reset, relaunch as above; a cut-off agent continues from what it had appended to its file. In a cloud session, once you can act again, offer to push `runs/<slug>/` before anything else.
- **The container was reclaimed:** before relaunching, list `analyses/`, `math/`, `verdicts/` and `cruxes/`. If a file is missing for an agent the relaunch would replay, tell the user: a resume would trust a result whose file is gone. Offer a fresh analyze run instead.
- **An agent's tool call was refused with `[pipeline guard]`:** it tried to write outside `runs/`. That's expected to be rare. If it shows up in a run, mention it, and check that the agent's output doesn't depend on the refused write.
- **A workflow returned `ok: false`:** tell the user what failed (the result says why), and offer to rerun that stage. If the analyze stage failed at the judge, a relaunch with `resumeFromRunId` returns the saved result of every agent before the first failure and runs everything from there: just the judge and the audit if nothing failed earlier.
- **Research came back thin because sources were blocked:** say so plainly, and offer to rerun where the network allows arXiv, INSPIRE and journal sites.
- **The workflow approval prompt:** in manual permission mode each run asks for approval. The user can pick "Yes, and don't ask again" for these two workflows.
