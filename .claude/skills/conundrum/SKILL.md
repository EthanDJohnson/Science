---
name: conundrum
description: Multi-agent investigation of a hard physics or engineering question (feasibility, design, mechanism or anomaly). Partitioned literature research, a source-checked dossier, independent method lenses, competing candidate answers, calculation-grounded falsification, and a neutral adjudicated report. Expensive (roughly 15 to 50 agent runs over 1 to 5 hours); runs only when invoked as /conundrum.
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
- **Few agents at once:** if it notes that only a few agents run at once, mention that runs here will take longer than the table below. It's roughly 2× for standard and 3–4× for deep.
- **Required package missing:** ask whether to install it (`pip install sympy numpy`) before continuing. The physics calculations depend on it.
- **Literature sources blocked:** tell the user in one line that research will lean on search summaries and INSPIRE abstracts, which the pipeline marks and weighs down. Continue unless they want to fix network access first.

Then check that WebFetch itself can read papers: WebFetch `https://arxiv.org/abs/gr-qc/0009013` and ask for the title.
- **WebFetch fails with EGRESS_BLOCKED while `check_env.py` shows arxiv.org reachable:** the environment's network settings changed after this session started. WebFetch picks them up only in a new session. Tell the user so. They can continue, with research leaning on `lit_search` abstracts and search summaries, or start a new session first.

## 1. Frame the question with the user

1. **Create the run directory.** Build a slug from today's date (`date +%F`) plus a 3–6 word kebab-case summary, for example `2026-09-29-alcubierre-negative-energy`. Create `runs/<slug>/`.
2. **Classify the question** as `feasibility`, `design`, `mechanism` or `anomaly`, using `lenses.md`.
3. **Draft `runs/<slug>/brief.md`** in the brief format. Do the thinking the user would want done up front:
   - **Define every loaded term.** For example, "superluminal effective speed" relative to which observers; "negative energy" meaning which energy density, measured by whom.
   - **State the admissible physics.** The default is established GR plus QFT, including semiclassical gravity. Speculative extensions are allowed only when labelled.
   - **State the horizon for "viable":** in principle, and in practice within a stated time.
   - **List the hidden premises worth testing.**
   - **Say what a useful answer looks like.**
4. **Check for calculator gaps.** List the calculations the question will need, for example relativistic travel times, Casimir energies, heat rejection or orbital transfers. Compare them with `tools.md`.
   - **Propose a new calculator only for a calculation several agents will need and that is easy to get subtly wrong.** One-off arithmetic doesn't qualify; agents write that in their own scripts.
   - **For each one, give a snake_case name not already in the toolkit,** and a one-line purpose saying what it must cover.
   - **Usually there are none.** Say so and move on.
5. **Get the brief confirmed.** Show the user:
   - the question made precise;
   - the premises to test;
   - what counts as an answer;
   - the depth with its expected size;
   - any proposed calculators. Each costs roughly $2–5 at API prices and is built alongside the research.

   Ask them to confirm or correct it, and apply any corrections to `brief.md`.

   | depth | what runs | agent runs | rough time | rough cost at API list prices |
   |---|---|---|---|---|
   | quick | 3 researchers, no source checks, 3 lenses, 1 refuter per candidate, Opus judge | ~16 | 1–2 hours | ~$35–60 |
   | standard | 4 researchers + checks, 5 lenses, 1 refuter per candidate, Fable judge | ~23 | 1.5–3 hours | ~$45–90 |
   | deep | 5 researchers + checks, 6–7 lenses, 3 refuters per candidate, crux round, Fable judge at max | ~40–50 | 3–5 hours | ~$100–180 |

   Say that these are extrapolated from two measured agents, not a full run. Times exclude the checkpoints and assume at least 5 agents can run at once (see the preflight). On a subscription the run draws on usage limits instead. `/workflows` shows live token counts, and `/usage` afterwards attributes usage to subagents and flags cache misses.

## 2. Research

Call the Workflow tool with `name: "conundrum-research"` and `args: {slug, depth, tools}`. `tools` holds the confirmed calculators as `[{name, purpose}]`; leave it out if there are none. The workflow runs in the background, so wait for its completion notification. If the result lists `missing` or `unchecked` facets, mention them at the checkpoint.

**In a cloud session, offer to commit and push `runs/<slug>/` now,** and again after step 4. The container is reclaimed after inactivity and unpushed files are lost, while a workflow's saved results survive, so a later relaunch would trust agents whose files no longer exist.

## 3. Checkpoint with the user

Read `runs/<slug>/dossier.md` and summarize it in 12 lines or fewer:
- the three facts the question depends on most;
- the key numbers;
- contested points;
- binding constraints;
- the share of claims resting only on search summaries;
- anything the source checks dropped or corrected.

**Check that the pipeline itself is untouched.** Run `git status --short -- .claude CLAUDE.md .mcp.json`. Pipeline agents can't write there, because the pipeline guard hook blocks it. Any change you didn't make yourself means something got past the guard: stop, show the user `git diff` for those paths, and don't promote anything or continue until they decide.

**Promote the calculators that were built.** For each entry in the workflow result's `tools` with `ok: true`:
1. **Re-run its self-test yourself** with `python3 runs/<slug>/tools/<name>.py selftest`; don't rely on the toolsmith's report.
2. **Read its reference values.** Each must come from an independent source cited in a comment (a closed form, a definition, a published table), not from the code itself. At least one must be a limit where the model reduces to a simpler known law.
3. **If both hold, promote it.**
   - Copy it to `.claude/skills/conundrum/scripts/<name>.py`. Never overwrite an existing file; if the name is taken, ask the user.
   - Add its row to `tools.md`, noting "built in run <slug>".
   - Run `python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests`.
   - Tell the user what was added, and where to find its reference values. The lenses can use it in the analysis stage, and future runs find it in the toolkit.
4. **If anything fails,** leave it in the run folder, say what failed, and let the lenses do without it.

Then:
- **Ask for corrections or unpublished data.** Append them to the dossier under `## User-supplied`, marking each `[user]`.
- **Choose lenses** with `lenses.md`, from type × depth. Show each one with a line on why.
- **Confirm the user wants to continue.** This is the expensive half.

## 4. Analyze

Call the Workflow tool with `name: "conundrum-analyze"` and `args: {slug, depth, type, lenses}`, and wait for completion. Then offer to commit and push `runs/<slug>/` again (see step 2).

## 5. Report

First check that the pipeline is still untouched, as at step 3: `git status --short -- .claude CLAUDE.md .mcp.json` should show only changes you made.

Read `runs/<slug>/report.md` and `runs/<slug>/audit.md`. Present:
- the bottom line;
- the ranked-answers table;
- the top three decisive tests or calculations;
- every audit flag marked `unsupported` or `contradicted`, plus the count marked `weak`;
- the paths to `report.md`, `dossier.md` and `calc/`.

Don't restate the whole report; it is in the file.

## If something fails

- **A workflow stopped partway:** relaunch it with the same name and args. In the same session, completed agents return their saved results instead of running again.
- **A workflow hit the usage limit:** in a local interactive session, waiting agents continue by themselves after the reset (up to two waits per run). In a background or cloud session the affected agents fail instead. Relaunch the same workflow with the same args after the reset: completed agents return saved results, and a cut-off agent continues from what it had appended to its file.
- **An agent's tool call was refused with `[pipeline guard]`:** it tried to write outside `runs/`. That's expected to be rare. If it shows up in a run, mention it, and check that the agent's output doesn't depend on the refused write.
- **A workflow returned `ok: false`:** tell the user what failed (the result says why), and offer to rerun that stage.
- **Research came back thin because sources were blocked:** say so plainly, and offer to rerun where the network allows arXiv, INSPIRE and journal sites.
- **The workflow approval prompt:** in manual permission mode each run asks for approval. The user can pick "Yes, and don't ask again" for these two workflows.
