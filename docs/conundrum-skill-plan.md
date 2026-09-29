# `/conundrum`: review of Gemini's design, and a build plan

*Status: plan only, nothing implemented yet. Written 2026-09-29.*

A second opinion on a Gemini conversation about (1) Harb et al.'s "philosophy agents" chemistry paper, (2) whether philosophy-style system prompts help frontier models, and (3) how to build a multi-agent "scientific conundrum" skill in Claude Code. Sections 1–4 check Gemini's claims; section 5 is my plan.

## TL;DR

1. **The paper is real, but narrower than Gemini said.** *The ballad of LLM agents: philosophical reasoning for chemistry* (Harb et al., Argonne) is peer-reviewed in *Machine Learning: Science and Technology* (2026), not only on ChemRxiv as Gemini cited. It tested **only OpenAI models** (GPT-4o, GPT-5, GPT-5.1), on the **open-ended numerical-answer subset** of ChemBench. Gemini's headline numbers (an "average of 7 to 11 percentage points", and Hume's "highest aggregate accuracy (68.3%)") are **GPT-4o-only** results presented as study-wide ones.
2. **The paper can't tell you whether personas help Opus 5.5 or Fable 5.1.**
   - GPT-5.1's API default is *no reasoning*; GPT-5's is medium. The paper's baselines may not have been reasoning at all.
   - In physical chemistry, the newer GPT-5.1 started 40 points below GPT-5 (56.7% vs. 97.0%). Socrates brought it to 94.0%, roughly where GPT-5 started with no philosophy.
   - At the strict threshold, GPT-5 gained least (+4.5) and GPT-5.1 most (+21.8).
   - That pattern fits "any prompt that makes a non-reasoning run reason helps" as well as it fits anything Socratic.
   - I found no sign of a non-philosophical control prompt that could tell those apart.
   - Current Claude models always think in Claude Code, so that lever is already pulled.
3. **Keep the lenses, but make them methods rather than personas.** Several independent agents each hunting for a different kind of explanation or error is valuable for coverage. That value comes from the method instructions, not the philosopher's name. Define each lens by what it must produce, and let an eval decide whether the names add anything.
4. **Gemini's pipeline has the right skeleton but real flaws:**
   - It narrows to 1–2 hypotheses too early.
   - Its critic argues in prose instead of running calculations and searches.
   - The hypothesis never gets a second turn.
   - Nothing checks citations. That is the same failure its own paper summary showed.
5. **The evidence favors model diversity over persona diversity.**
   - Mixing model families is one of the few consistently helpful ingredients in multi-agent reasoning.
   - An outside critic, such as the "Astra 6" (OpenAI's GPT-6 Astra) you mentioned, is a better bet than another philosopher.
6. **Its Claude Code instructions are outdated or invented.** Build it as three layers:
   - A **skill** holds the entry point, the framing step and a human checkpoint.
   - The skill runs **saved dynamic workflows**, which are deterministic, parallel and resumable.
   - The workflows call **custom subagents**. Each lens's system prompt, model and effort live in `.claude/agents/*.md`.
   - The built-in `/deep-research` workflow already does most of the research stage.

---

## 1. Fact-check: the paper

| Gemini said | What I found | Verdict |
|---|---|---|
| Title, authors, Argonne | Correct: Harb, Sun, Unal, Chia, Yang, Ingram, Assary | ✅ |
| Source: ChemRxiv preprint (10.26434/chemrxiv.15001731/v1) | Also peer-reviewed: *Mach. Learn.: Sci. Technol.* (IOP) 2026, DOI 10.1088/2632-2153/ae792d, with an open-access copy on OSTI | ⚠️ incomplete. Your "journal paper" was right |
| Evaluated on "ChemBench tasks" | Only the **open-ended numerical-answer subset**, scored at relative-error thresholds (strict = 1%) | ⚠️ scope omitted |
| (implied) Applies to frontier models generally | Only GPT-4o, GPT-5 and GPT-5.1. No Claude, Gemini or open-weight models | ⚠️ |
| Seven philosopher prompts | The abstract names Socrates, Descartes, Kant and Hume. Results mention Aristotle, and an indexed excerpt describes Hegel and Plato prompts | ✅ probably |
| PAs "consistently outperformed the default base models… by an average of 7 to 11 percentage points" | That range is **GPT-4o only**, at the 1% threshold: "all philosophical agents outperformed the base model… by a range of 7–11 percentage points" | ❌ misattributed |
| Hume "achieved the highest aggregate accuracy (68.3%)", followed by Aristotle and Kant (66.7%) | Also **GPT-4o only**, at 1%. 68.3% and 66.7% are exactly 41/60 and 40/60. If that's the denominator, the "best philosopher" won by one question | ❌ misattributed |
| (not reported) | Headline gains at the strict threshold: GPT-4o + Hume **+11.5**, GPT-5 + Kant **+4.5**, GPT-5.1 + Socrates **+21.8** points. Another indexed version of the abstract gives +18.4 / +14.1 / +11.7, with **Descartes** as GPT-5.1's best. The "best philosopher" changes with version or threshold | ❗ key numbers missing |
| Socrates took GPT-5.1 from 56.7% to 94.0% (physical chemistry) | A search excerpt attributes it to GPT-5.1. I couldn't check it against the PDF | ✅ probably |
| Descartes took GPT-4o to 86.6% | Confirmed, on a subdomain | ✅ |
| GPT-5 near 97% on physical chemistry, with small gains | Confirmed: baseline 97.0%, and Descartes "slightly outperformed" it | ✅ |
| Analytical chemistry: Socrates and Plato lifted GPT-5.1 from 8% to 20% | Not found. The paper says analytical and organic chemistry were hardest for every model | ❓ unverified |
| "Cited by: 5" | Unverifiable and irrelevant | — |

**What the paper can't tell you (caveats Gemini skipped):**

- **Reasoning-mode confound.**
  - GPT-5.1's API defaults to `reasoning_effort: "none"`. GPT-5 defaults to `"medium"`.
  - If the baselines ran at defaults, the biggest win (+21.8 on GPT-5.1) may come from making a non-reasoning run reason at all. I couldn't open the methods section to check this.
  - The smallest win (+4.5) came on the model that already reasons.
  - The physical-chemistry excerpts fit the same story, if they're right:
    - The newer GPT-5.1 started at 56.7%, 40 points below GPT-5's 97.0% baseline.
    - Socrates brought GPT-5.1 to 94.0%, roughly where GPT-5 started with no philosophy.
  - You'd see this pattern whether or not the philosophy matters.
- **No visible neutral control.** Nothing I could reach mentions a matched-length, non-philosophical prompt such as "decompose, check units, verify". Without one, you can't separate "philosophy" from "structured instructions".
- **Small, noisy comparisons.** Cells appear to be tens of questions. The winner flips across models and thresholds. "Match the philosopher to the subfield" is a hypothesis, not a finding.
- **Closed-form answers aren't open research problems.** Getting a number within 1% says little about generating and eliminating explanations for an open anomaly.

## 2. Fact-check: "any benefit on frontier models?"

| Gemini's claim | Assessment |
|---|---|
| The benefit shifts on frontier models, and closed benchmarks hit a ceiling | ✅ Reasonable, and consistent with GPT-5's small gain |
| Frontier models "default to pattern matching" before rigorous deduction, so a lens acts as a reasoning filter | ⚠️ Unfalsifiable framing. Opus 5.5, Sonnet 5.5 and the Fable models always think in Claude Code. What controls depth is `effort`, not a persona |
| Lenses make "auditability and rationale trace change dramatically" | ❌ No evidence given. Stated reasoning isn't reliably faithful to what produced the answer (§4), so a differently styled trace isn't more auditable |
| "As Harb et al. demonstrated", failures come from the wrong epistemic stance | ❌ The paper measured accuracy differences. It reports model × prompt interactions, not failure causes |
| A Kantian or methodical-doubt prompt "directly counters sycophancy" | ❌ No evidence given |
| Contrasting postures extract "far deeper analysis" than one prompt | ⚠️ Plausible for coverage. The evidence on debate itself is mixed (§4) |
| Skip lenses for lookups and routine calculations; rigid prompts can over-hedge creative work | ✅ Sensible |

**My answer to your original question:** expect little or no accuracy gain from a persona alone on Opus 5.5 or Fable 5.1. The defensible benefit is diversity: independent agents, each forced to look for a different kind of error or explanation. That benefit lives in the method instructions. Write the lenses as methods, and keep the philosopher names as labels if you like them. An eval (§5.8) can then show whether the names add anything.

## 3. Fact-check: Gemini's architecture and Claude Code instructions

**Worth keeping**

- **Partitioned research mandates** (empirical, mechanistic, contrarian). Giving research subagents distinct, non-overlapping tasks is Anthropic's published lesson for exactly this setup.
- **A three-part dossier:** established facts, discrepancies and constraints.
- **Isolated lens analyses written to separate files.** Independence comes before any interaction.
- **A neutral adjudicator** that doesn't role-play, with a report that ends in falsifying experiments (Platt's "strong inference").

**Needs fixing**

1. **It contradicts its own summary of the paper.**
   - It drops Aristotle and Kant, tied for second by its own numbers.
   - It drops Plato, which it said helped analytical chemistry.
   - It cites the paper for a fixed Descartes/Hume/Socrates trio that the paper doesn't support.
2. **Premature convergence.**
   - The Theorist proposes one or two hypotheses, and everything downstream only tests those.
   - Hard conundrums need a slate of competing hypotheses carried in parallel (Chamberlin's "multiple working hypotheses").
   - That slate should include the boring ones: artifact, contamination, calibration or unit error.
3. **Critique by prose.**
   - The Inquisitor is asked to find conservation-law violations and mathematical impossibilities, but it has no tools.
   - Those checks should be computed (Python, dimensional analysis, order-of-magnitude estimates).
   - They should also be searched: look for disconfirming evidence directly.
   - Self-critique without external grounding is weak (§4).
4. **No second turn.** The hypothesis never answers its critique. Add one bounded rebuttal round on the specific cruxes, not an open debate.
5. **No provenance check.**
   - The compiler turns raw research into "Known Facts (High Confidence)", and nothing verifies claims against sources.
   - Gemini's own paper summary, with GPT-4o numbers presented as aggregates, is the error this pipeline would launder.
6. **"Tournament" in name only.** There's no bracket or ranking. Real tournament designs, like Google's AI co-scientist, rank many hypotheses by pairwise comparison.
7. **The Claude Code part is outdated or invented.**
   - **Outdated location.** `.claude/commands/*.md` still works, but commands have been merged into skills. `.claude/skills/<name>/SKILL.md` adds supporting files and control over who can invoke it.
   - **Not a real mechanism.** `Run task: … -> save to .temp/…` doesn't exist. A skill is instructions Claude interprets.
   - **Missing custom subagents** (`.claude/agents/*.md`). They are exactly how you "preload a philosophy system prompt":
     - The file's body replaces the default system prompt.
     - Frontmatter sets `model:` (`sonnet`, `opus` or `fable`) and `effort:` (`low` through `max`).
     - So your "Sonnet at high, Opus at max" plan is directly configurable.
   - **Missing dynamic workflows.** A workflow is a script that holds the control flow, fans agents out and validates their structured output. It can resume after an interruption, and you can save it as a `/command`.
   - **Missing the built-in `/deep-research` workflow.** It already fans out searches, cross-checks sources and votes on claims.
   - **Wrong about debate.** Gemini dismissed debate as "unbounded", which you never proposed. It also missed that Claude Code's experimental **agent teams** document your exact idea: "Spawn 5 agent teammates to investigate different hypotheses. Have them talk to each other to try to disprove each other's theories, like a scientific debate."
8. **Cost is asserted, not estimated.**
   - Gemini claims "token efficiency" for a design that still runs about ten top-tier agents.
   - Anthropic reports that multi-agent research uses about 15× the tokens of a chat.
   - Plan depth tiers for that (§5.7).

## 4. What the broader evidence says

Full texts were blocked here, so these come from abstracts and search excerpts. Figures come from the papers' own reporting.

**Persona prompts don't reliably improve accuracy.**

- **Zheng et al. (EMNLP Findings 2024).**
  - Tested 162 roles, 2,410 factual questions and 4 model families.
  - Personas gave no gain over no persona, and the effects were "largely random".
  - Choosing the best persona automatically did no better than random.
- **Wharton Prompting Science Report 4 (Dec 2025).**
  - Covered GPQA Diamond and MMLU-Pro across six models, including reasoning models.
  - No expert persona reliably helped, and low-knowledge personas hurt.
- **Araujo et al. (EMNLP 2025).** Expert personas were neutral to slightly positive. Irrelevant persona details cost up to about 30 points.
- **Kong et al. (NAACL 2024), the instructive exception.**
  - Large role-play gains on ChatGPT, which the authors attribute to role-play acting as an implicit chain-of-thought trigger.
  - That is the same confound as in §1. For models that already think, the trigger should add little.

**At equal compute, debate mostly isn't better than voting.**

- **Early wins weren't compute-matched** (Du et al., ICML 2024).
- **With matched budgets, debate lost or tied:**
  - Self-consistency beat debate (Huang et al., ICLR 2024).
  - Debate didn't reliably beat ensembling (Smit et al., ICML 2024).
  - Majority voting explains most of debate's gains (Choi et al., NeurIPS 2025).
  - At equal thinking-token budgets, single agents matched or beat multi-agent designs on multi-hop QA (Tran & Kiela, 2026).
- **Where debate does help:**
  - Mixing different models (Zhang et al. 2025; ReConcile, ACL 2024).
  - Checkable evidence, such as debaters' quotes verified against the source (Khan et al., ICML 2024).
  - Voting rather than consensus, with few rounds. More rounds before the vote hurt (Kaesberg et al., ACL Findings 2025).
- **Agents conform and flip:**
  - They follow the majority (BenchForm, ICLR 2025).
  - They abandon correct answers under peer reasoning (Wynn et al. 2025).
  - They reach premature consensus through sycophancy (Yao et al. 2025).

**Critique works when it's grounded.**

- **Without external feedback, self-correction doesn't help and can hurt** (Huang et al., ICLR 2024; Kamoi et al., TACL 2024 survey).
  - Reasoning models' reflections mostly confirm their first answer (Kang et al. 2025).
- **With tools and verifiers, it works:**
  - CRITIC (search plus a code interpreter).
  - Self-Debug (execution feedback).
  - Sound external verifiers (Stechly et al., ICLR 2025).
- **Models struggle to find their own errors, but fix them once told where** (Tyen et al., ACL Findings 2024).

**Judges are biased, and reasoning traces aren't transcripts.**

- **LLM judges show position, verbosity and self-preference bias** (Zheng et al., NeurIPS 2023; Wang et al., ACL 2024). The better a model recognizes its own outputs, the more it favors them (Panickssery et al., NeurIPS 2024).
- **Stated reasoning often omits what actually drove the answer** (Turpin et al., NeurIPS 2023). In Anthropic's 2025 study, Claude 3.7 Sonnet mentioned a hint it had used about 25% of the time.

**Prior systems that worked lean on tools, diversity and external checks.**

- **Google's AI co-scientist** (Nature 2026).
  - Stages: generation, literature-grounded reflection, an Elo tournament of pairwise debates, similarity-based deduplication, evolution, and meta-review.
  - The authors warn that Elo is self-evaluated, and checked it against external correctness.
- **Stanford's Virtual Lab** (Nature 2025).
  - A PI agent works with specialist agents and a Scientific Critic, which caught concrete errors.
  - Parallel meetings are merged into one.
  - Tools and wet-lab tests carried the result.
- **Anthropic's multi-agent research system** (2025).
  - It beat single-agent Opus 4 by 90.2% on an internal eval.
  - Token usage explained 80% of variance on BrowseComp, and runs used about 15× chat tokens.
  - Subagents write outputs to the filesystem, and a separate agent handles citations.
  - Effort is scaled to how complex the query is.
- **The classics:** Chamberlin (1890) on multiple working hypotheses; Platt (1964) on strong inference.

**What this means for the design**

| Evidence | Design choice (§5) |
|---|---|
| Persona effects on objective tasks are close to noise | Lenses defined by method; persona vs. neutral wording becomes an eval arm |
| Voting beats debate at equal compute, and agents conform | Independent refuters with a majority vote; at most one crux round; advocates never see each other's drafts |
| Grounded critique works; intrinsic critique doesn't | Every verdict must state its basis: a calculation, a quoted source, or an inconsistency |
| Mixing model families helps | An optional non-Claude critic is the best-supported upgrade (§5.9) |
| Judges favor position, length and their own outputs | Judge on a different model than the refuters; an evidence-over-eloquence rubric; pairwise comparisons in both orders in deep mode |
| Single agents can match multi-agent systems at equal budget | Eval arm A: a single Opus at `max` with the same dossier |
| Token spend drives research quality, at ~15× chat | Depth tiers, with research on Sonnet |

---

## 5. The plan

### 5.1 Design principles

1. **Independence before interaction.** Every lens agent and every refuter works alone from files. Aggregation happens only afterwards.
2. **Many hypotheses, eliminated by evidence.** Always carry 4–8 competing explanations, including mundane ones, until tests kill them.
3. **Ground every critique.** A refutation is a calculation, a citation with a quote, or a documented inconsistency. "This seems unlikely" doesn't count.
4. **Provenance or it didn't happen.**
   - Every factual claim carries a source URL, a verbatim quote and an access level: full text, abstract or search snippet.
   - A checker verifies claims against sources.
   - The judge discounts snippet-only evidence.
5. **Spend effort where it pays.** Use Sonnet at `high` for search and Opus at `high` for analysis. Save `xhigh` and `max` for synthesis and judging.
6. **Put human checkpoints where your knowledge beats the model's:** after framing, and after the dossier.
7. **Measure before believing.** Personas, debate rounds and `max` effort each stay only if an ablation shows they help.

### 5.2 Architecture

```
/conundrum <question>                                    skill, main session
 0  FRAME     interactive brief: observations, numbers, what counts as an answer
              → you confirm
 ┌─ workflow: conundrum-research ────────────────────────────────────────────
 │ 1  RESEARCH  3–4 Sonnet researchers, one facet each (parallel)
 │ 1b CHECK     source checker per facet (pipelined behind each researcher)
 │ 1c DOSSIER   Opus compiler → dossier.md
 └──────────────────────────────────────────────────────────────────────────
 0' CHECKPOINT  you correct the dossier and add unpublished data
 ┌─ workflow: conundrum-analyze ─────────────────────────────────────────────
 │ 2  LENSES    4–5 lens agents, isolated (parallel) → analyses/<lens>.md
 │ 3  SLATE     4–8 competing hypotheses, each with distinguishing predictions
 │ 4  FALSIFY   refuter(s) per hypothesis, with Python + targeted search
 │ 5  CRUX      only if ≥2 survive: one written rebuttal per survivor
 │ 6  JUDGE     neutral adjudicator → report.md (probabilities + decisive tests)
 │ 7  AUDIT     every claim in the report traced to the dossier or a calculation
 └──────────────────────────────────────────────────────────────────────────
```

Why three layers:

- **Workflows for stages 1–7.**
  - Stages run in a fixed order, and agents truly run in parallel.
  - Outputs are validated against a schema.
  - A run resumes after interruption, so a failed judge doesn't re-buy the research.
  - Intermediate results stay out of your main context.
- **A skill as the entry point.**
  - Workflows can't take input mid-run, so framing and the dossier checkpoint live in the skill, between two workflow runs.
  - The skill also carries the lens catalog, schemas and rubric.
  - `disable-model-invocation: true` stops the expensive pipeline from triggering on its own.
  - A skill whose instructions call the Workflow tool counts as your opt-in to running workflows.
- **Custom subagents for every role.** Each role's system prompt, tools, model and effort are version-controlled. Workflows use them through `agent(prompt, { agentType })`.

### 5.3 Stages, models, effort

| # | Stage | Agents (standard) | Model / effort | Output |
|---|---|---|---|---|
| 0 | Frame | main session | your session | `brief.md` |
| 1 | Research. Facets: empirical data · mechanisms/theory · anomalies and failed replications · adjacent-field analogues | 3 (deep: 4) | Sonnet 5.5 / `high` | `research/<facet>.md` |
| 1b | Source check | 1 per facet | Sonnet 5.5 / `medium` | each claim marked verified, unverifiable or contradicted |
| 1c | Dossier | 1 | Opus 5.5 / `high` | `dossier.md` |
| 2 | Lenses | 5 | Opus 5.5 / `high` (Constraints lens: `xhigh`) | `analyses/<lens>.md` |
| 3 | Slate | 1 | Opus 5.5 / `xhigh` | `hypotheses.md` |
| 4 | Falsify | 1 per hypothesis (deep: 3, majority vote) | Opus 5.5 / `high` | `verdicts/<id>-<n>.md` |
| 5 | Crux (conditional) | 1 per survivor | Opus 5.5 / `high` | `cruxes/<id>.md` |
| 6 | Judge | 1 | **Fable 5.1 / `high`** (or Opus 5.5 / `max`) | `report.md` |
| 7 | Audit | 1 | Sonnet 5.5 / `medium` | flags on `report.md` |

How this compares with your model and effort plan:

- **Research on Sonnet 5.5 at `high`:** agreed.
- **Compiler on Opus at `max`:** I'd use `high`. Compiling is mostly synthesis and formatting. Spend the top effort on the judge.
- **Fable 5.1 as judge.**
  - Fable 5.1 is Anthropic's most capable model, at $10/$50 per million tokens against Opus 5.5's $4/$20.
  - One call at the end is where it has the most leverage.
  - Anthropic's guidance is that newer models at lower effort often match older ones at higher effort.
  - Raise effort to `max` only when a measurement shows headroom.
- **Set `effort` explicitly on every agent.** Opus 5.5's API default is `medium`. Subagents without an `effort` setting inherit your session's.
- **Haiku 4.5 doesn't take an effort setting.** Keep it out of stages that need depth.

### 5.4 Lens catalog (the philosopher is a label; the method is the content)

| Lens | Label | Must produce | Default? |
|---|---|---|---|
| Decomposer | Descartes | Sub-question tree, plus an **assumption ledger** (measured / derived / assumed / unknown) naming the one assumption whose failure would dissolve the conundrum | yes |
| Mechanist | Aristotle | A causal chain for each candidate mechanism, and what kind of phenomenon this is (kinetic vs. thermodynamic, transport, interfacial…) | yes |
| Empiricist | Hume | What was observed vs. inferred; base rates ("how often do anomalies like this turn out to be artifacts?"); analogous cases in adjacent systems | yes |
| Constraint auditor | Kant | Conservation, thermodynamic and rate limits, dimensional analysis and order-of-magnitude estimates, **computed in Python**, plus the validity domain of every model used | yes |
| Examiner | Socrates | A challenge to the framing (is the anomaly real, well-defined, reproducible?), plus the 5–10 hardest questions no current explanation answers | yes |
| Dialectician | Hegel | For two well-supported but conflicting bodies of evidence: the regime or condition under which both hold | when the dossier has a direct contradiction |
| Idealizer | Plato | The simplest idealized model that reproduces the phenomenon, and exactly where reality departs from it | theory-heavy problems |

Every lens must give at least three candidate explanations. Each needs a prediction that would tell it apart from the others. These feed the slate.

### 5.5 File layout

```
.claude/
  skills/conundrum/
    SKILL.md                  entry point + protocol
    references/lenses.md      catalog above + selection rules
    references/schemas.md     formats: research note, dossier, analysis, hypothesis, verdict, report
    references/rubric.md      adjudication rubric + calibration rules
  agents/
    researcher.md  source-checker.md  dossier-compiler.md
    lens-decomposer.md  lens-mechanist.md  lens-empiricist.md  lens-constraints.md
    lens-examiner.md  lens-dialectician.md  lens-idealizer.md
    hypothesis-builder.md  falsifier.md  crux-advocate.md  adjudicator.md  report-auditor.md
  workflows/
    conundrum-research.js
    conundrum-analyze.js
runs/<slug>/                  brief.md  research/  dossier.md  analyses/  hypotheses.md
                              verdicts/  cruxes/  report.md
```

Research notes use one line per claim:
`CLAIM … | SOURCE <url> | QUOTE "…" | ACCESS full-text/abstract/snippet | CONFIDENCE high/med/low`.

Keep the skill in the repo's `.claude/skills/`, where Claude Code accepts every frontmatter field used below. Uploading it to claude.ai as a personal skill instead limits frontmatter to six spec fields, and `argument-hint` or `disable-model-invocation` would then fail validation.

### 5.6 Sketches

These are illustrative starting points, not tested code.

**`.claude/skills/conundrum/SKILL.md`**

```markdown
---
name: conundrum
description: Multi-agent investigation of a hard scientific question or unexplained observation — partitioned literature research, independent method lenses, competing hypotheses, tool-grounded falsification, and a neutral adjudicated report. Expensive; runs only when invoked.
argument-hint: "[quick|standard|deep] <question, or path to a brief>"
disable-model-invocation: true
---

You coordinate; the workflows do the work. Never skip a checkpoint.

1. Frame. From $ARGUMENTS, draft runs/<slug>/brief.md: the conflicting observations
   (numbers, conditions, sources), what would count as an answer, known constraints,
   prior attempts, and any data the user holds that isn't public. Ask the user to
   confirm or correct it. Depth defaults to standard.
2. Research. Call the Workflow tool with name "conundrum-research", args {slug, depth}.
3. Checkpoint. Summarize dossier.md: established facts, open discrepancies,
   snippet-only sources. Ask for corrections or unpublished data; add them marked [user].
4. Analyze. Call the Workflow tool with name "conundrum-analyze", args {slug, depth, lenses}
   (choose lenses with references/lenses.md).
5. Report. Present report.md: ranked hypotheses with probabilities, the cheapest
   decisive experiment for each, and anything the auditor flagged.
```

**`.claude/agents/lens-constraints.md`**

```markdown
---
name: lens-constraints
description: Conundrum pipeline lens. Audits candidate explanations against hard physical constraints with explicit calculations. Use only when the conundrum workflow asks for it.
tools: Read, Write, Bash, WebSearch
model: opus
effort: xhigh
maxTurns: 40
---

You audit the conditions any valid explanation must satisfy. You are one of several
independent analysts; you will not see their work.

1. List every constraint that applies: conservation of mass, energy, charge and
   momentum; the second law; detailed balance; symmetry; transport and rate limits.
2. For each candidate explanation in the brief and dossier, and any you add, run the
   numbers in Python: magnitudes, units, limits. Print inputs and where they came from.
3. Classify each explanation as violates / strained / consistent, citing the calculation.
4. For every model the dossier relies on, state its domain of validity and whether the
   conundrum's conditions fall outside it.
5. Give at least three explanations that survive your audit, each with an observable
   prediction that would distinguish it from the others.

Write the file you were asked for in the "analysis" format from
.claude/skills/conundrum/references/schemas.md. Do not rank explanations or give a
final answer.
```

**`.claude/agents/adjudicator.md`**

```markdown
---
name: adjudicator
description: Neutral final judge for the conundrum pipeline. Ranks competing hypotheses after falsification. No persona.
tools: Read, Write
model: fable
effort: high
---

You are the scientific editor making the final call. You wrote none of the inputs.

- Judge evidence, not eloquence: a verdict counts for what its calculation or quoted
  source shows, not for its confidence or length.
- Evidence marked snippet-only or unverified counts for less; say where it changed
  your ranking.
- Give a probability for each surviving hypothesis plus an explicit "none of these"
  remainder, summing to 1.
- For each hypothesis still standing: the strongest evidence for and against, and the
  cheapest experiment or calculation that would decide it.
- List the assumptions every surviving hypothesis shares.
- Say which single result would most change your ranking.

Write report.md in the format in .claude/skills/conundrum/references/rubric.md.
```

**`.claude/workflows/conundrum-research.js`**

```js
export const meta = {
  name: 'conundrum-research',
  description: 'Conundrum stage 1: partitioned research, source check, dossier',
  whenToUse: 'Called by the /conundrum skill after the brief is confirmed',
  phases: [{ title: 'Research' }, { title: 'Check' }, { title: 'Dossier' }],
}

const { slug, depth = 'standard' } = args
const dir = `runs/${slug}`
const FACETS = {
  empirical: 'measurements, datasets and experimental conditions bearing on the question',
  mechanisms: 'governing theory, mechanisms and quantitative models, with their validity limits',
  anomalies: 'contradicting results, failed replications, known artifacts and published critiques',
  analogues: 'similar puzzles in adjacent systems or fields, and how they were resolved',
}
const facets = depth === 'quick' ? ['empirical', 'mechanisms']
  : depth === 'deep' ? Object.keys(FACETS)
  : ['empirical', 'mechanisms', 'anomalies']

// Each facet's check starts as soon as its own research finishes (no barrier).
await pipeline(facets,
  f => agent(`Question: ${dir}/brief.md. Research only: ${FACETS[f]}. Write ${dir}/research/${f}.md.`,
    { agentType: 'researcher', label: f, phase: 'Research' }),
  (_, f) => depth === 'quick' ? null
    : agent(`Check every load-bearing claim in ${dir}/research/${f}.md against its source.`,
        { agentType: 'source-checker', label: `check:${f}`, phase: 'Check' }))

phase('Dossier')
await agent(`Compile ${dir}/research/ into ${dir}/dossier.md.`, { agentType: 'dossier-compiler' })
return { dossier: `${dir}/dossier.md` }
```

**`.claude/workflows/conundrum-analyze.js`**

```js
export const meta = {
  name: 'conundrum-analyze',
  description: 'Conundrum stage 2: lenses, hypothesis slate, falsification, crux, judgment, audit',
  whenToUse: 'Called by the /conundrum skill after the dossier checkpoint',
  phases: [{ title: 'Lenses' }, { title: 'Slate' }, { title: 'Falsify' },
           { title: 'Crux' }, { title: 'Judge' }, { title: 'Audit' }],
}

const { slug, depth = 'standard',
        lenses = ['decomposer', 'mechanist', 'empiricist', 'constraints', 'examiner'] } = args
const dir = `runs/${slug}`
const refuters = depth === 'deep' ? 3 : 1

const SLATE = { type: 'object', required: ['hypotheses'], properties: { hypotheses: {
  type: 'array', items: { type: 'object', required: ['id', 'claim'],
    properties: { id: { type: 'string' }, claim: { type: 'string' } } } } } }
const VERDICT = { type: 'object', required: ['verdict', 'basis'], properties: {
  verdict: { enum: ['refuted', 'weakened', 'survives'] },
  basis: { enum: ['calculation', 'cited-evidence', 'internal-inconsistency', 'none'] } } }

// The slate needs every analysis, so this barrier is intentional.
phase('Lenses')
await parallel(lenses.map(l => () => agent(
  `Brief: ${dir}/brief.md. Dossier: ${dir}/dossier.md. Write ${dir}/analyses/${l}.md.`,
  { agentType: `lens-${l}`, label: l, phase: 'Lenses' })))

phase('Slate')
const slate = await agent(
  `Merge the candidate explanations in ${dir}/analyses/ into 4-8 competing, distinguishable ` +
  `hypotheses, always including a measurement-artifact one. Write ${dir}/hypotheses.md.`,
  { agentType: 'hypothesis-builder', schema: SLATE })

phase('Falsify')
const verdicts = (await parallel(slate.hypotheses.flatMap(h =>
  Array.from({ length: refuters }, (_, i) => () => agent(
    `Try to refute ${h.id}: "${h.claim}". Use ${dir}/dossier.md, Python and targeted searches. ` +
    `Write ${dir}/verdicts/${h.id}-${i}.md.`,
    { agentType: 'falsifier', schema: VERDICT, label: `${h.id}#${i}`, phase: 'Falsify' })
    .then(v => v && { id: h.id, ...v }))))).filter(Boolean)

// A hypothesis survives unless a majority of its refuters refuted it.
const votes = {}
for (const v of verdicts) (votes[v.id] = votes[v.id] || []).push(v.verdict)
const alive = Object.keys(votes).filter(id =>
  votes[id].filter(x => x === 'refuted').length * 2 < votes[id].length)

if (alive.length >= 2 && depth !== 'quick') {
  phase('Crux')
  await parallel(alive.map(id => () => agent(
    `Answer the verdicts against ${id} in ${dir}/verdicts/, then name the single observation ` +
    `that would decide between ${id} and ${alive.filter(x => x !== id).join(', ')}. ` +
    `Write ${dir}/cruxes/${id}.md.`,
    { agentType: 'crux-advocate', label: `crux:${id}`, phase: 'Crux' })))
}

phase('Judge')
await agent(`Adjudicate from ${dir}/dossier.md, ${dir}/hypotheses.md, ${dir}/verdicts/ and ` +
  `${dir}/cruxes/. Write ${dir}/report.md.`, { agentType: 'adjudicator' })

phase('Audit')
await agent(`Trace every factual claim in ${dir}/report.md to the dossier or a calculation; ` +
  `append a flagged-claims section.`, { agentType: 'report-auditor' })

return { report: `${dir}/report.md`, alive }
```

### 5.7 Depth tiers and cost

| Depth | What changes | Agents per run | Rough cost at API list prices |
|---|---|---|---|
| quick | 2 facets, no source check, 3 lenses, 1 refuter per hypothesis, no crux, Opus judge at `high` | ~10 | ~$5–15 |
| standard | as in §5.3 | ~15–20 | ~$15–40 |
| deep | 4 facets with checks, 6–7 lenses, 3 refuters per hypothesis, crux round, pairwise judging in both orders, Fable judge at `max` | ~35–45 | ~$50–120 |

The costs are my estimates, not measurements, and could easily be off by 2×. Run one standard pilot and read the per-agent token counts in `/workflows` before trusting them.

- **On a subscription**, runs draw down your usage window instead. Workflows pause at a usage limit and resume after the reset.
- **A deep analyze run can cross the 25-agent "Large workflow" warning.** If you run deep often, set the Dynamic workflow size to `large` in `/config`, which raises the warning threshold to 50.
- **Pre-approve tools** (`WebSearch`, `WebFetch`, `Bash(python3 *)`, writes under `runs/`) so a long run doesn't stall on permission prompts.
- **Expect an approval prompt per workflow run** in manual permission mode. For these two saved workflows, choose "Yes, and don't ask again".

### 5.8 Evaluation: test the premise instead of assuming it

1. **Cases.** Collect 10–20 conundrums with known resolutions, ideally from your own field and not written up online (for example, instrument problems your lab already solved).
   - Public classics are useful but contaminated: models know that OPERA's faster-than-light neutrinos were a loose fiber connector, the Pioneer anomaly was thermal recoil, and polywater was contamination.
   - If you use them, strip names, dates and places.
2. **Arms.**
   - (A) A single Opus 5.5 at `max`, given the same dossier.
   - (B) The pipeline with neutral method lenses.
   - (C) The same pipeline with philosopher personas.
   - (D) The pipeline without the falsification stage.
3. **Metrics.**
   - Is the known answer in the top 1 or top 3?
   - Brier score on the stated probabilities.
   - Share of report claims with verified provenance.
   - Tokens and wall-clock time.
4. **Decision rule.** Keep a component only if removing it hurts. Keep personas only if C beats B.

### 5.9 Build order

1. Write the agents, schemas and rubric. Run the stages by hand on one case to debug the prompts.
2. Build `conundrum-research`. First, try the built-in `/deep-research` plus a dossier-compiler step. It may be enough.
3. Build `conundrum-analyze`.
4. Write the `/conundrum` skill that wraps both, with the checkpoints.
5. Run the evals (§5.8) and prune whatever doesn't earn its cost.
6. Add a non-Claude critic. Of the optional extras, this is the one the evidence supports best (§4).
   - The "Astra 6" you mentioned is OpenAI's GPT-6 Astra, released in September 2026.
   - Claude Code can't run it as a subagent. A falsifier or a second judge can still call it through its API or CLI from `Bash`, or through an MCP server.
7. Optional: an interactive crux round using agent teams (experimental; ~7× tokens in plan mode).

### 5.10 Decisions for you

- **Which domains** you'll use this for. That changes the facets and the default lenses.
- **Which judge:** Fable 5.1 at `high`, or Opus 5.5 at `max`.
- **Where you run it.**
  - The local CLI has full web access.
  - This Claude Code on the web environment blocks doi.org, osti.gov and iopscience.iop.org. Research there falls back to search snippets unless you widen network access.

---

## Sources

**The paper and the reasoning-default confound**

- Harb et al., *The ballad of LLM agents: philosophical reasoning for chemistry*, Mach. Learn.: Sci. Technol. (2026): https://iopscience.iop.org/article/10.1088/2632-2153/ae792d. Open-access copy: https://www.osti.gov/pages/biblio/3377016-ballad-llm-agents-philosophical-reasoning-chemistry
- Preprint: https://chemrxiv.org/doi/10.26434/chemrxiv.15001731
- Same group's earlier paper: *Towards philosophical reasoning with agentic LLMs: Socratic method for scientific assistance*, https://iopscience.iop.org/article/10.1088/2632-2153/ae277f
- GPT-5.1 reasoning default (`none`) vs. GPT-5 (`medium`): https://developers.openai.com/api/docs/models/gpt-5.1 and https://x.com/kevinwhinnery/status/1989338879065751863

**Claude Code docs**

- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Workflows: https://code.claude.com/docs/en/workflows
- Agent teams: https://code.claude.com/docs/en/agent-teams
- Costs: https://code.claude.com/docs/en/costs

**Persona prompts**

- Zheng et al. 2024: https://aclanthology.org/2024.findings-emnlp.888/
- Wharton Prompting Science Report 4: https://arxiv.org/abs/2512.05858
- Araujo et al. 2025: https://aclanthology.org/2025.emnlp-main.1364/
- Kong et al. 2024: https://aclanthology.org/2024.naacl-long.228/

**Debate, voting and self-correction**

- Du et al. 2024: https://proceedings.mlr.press/v235/du24e.html
- Smit et al. 2024: https://proceedings.mlr.press/v235/smit24a.html
- Choi et al. 2025: https://arxiv.org/abs/2508.17536
- Zhang et al. 2025: https://arxiv.org/abs/2502.08788
- Tran & Kiela 2026: https://arxiv.org/abs/2604.02460
- Kaesberg et al. 2025: https://aclanthology.org/2025.findings-acl.606/
- Huang et al. 2024: https://arxiv.org/abs/2310.01798
- Kamoi et al. 2024: https://aclanthology.org/2024.tacl-1.78/
- BenchForm (Weng et al. 2025): https://arxiv.org/abs/2501.13381

**Faithfulness of stated reasoning**

- Turpin et al. 2023: https://arxiv.org/abs/2305.04388
- Anthropic 2025: https://www.anthropic.com/research/reasoning-models-dont-say-think

**Prior systems**

- AI co-scientist: https://www.nature.com/articles/s41586-026-10644-y
- Virtual Lab: https://www.nature.com/articles/s41586-025-09442-9
- Anthropic multi-agent research: https://www.anthropic.com/engineering/multi-agent-research-system

**Other**

- GPT-6 Astra: https://openai.com/index/gpt-6-astra/

**How I checked.** Paper details come from search-indexed text of the journal, OSTI and ChemRxiv pages. This environment's network policy blocks the full text, so claims marked ❓ need a check against the PDF.
