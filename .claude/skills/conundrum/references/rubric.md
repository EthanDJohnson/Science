# Adjudication rubric and report format

The adjudicator reads `brief.md`, `dossier.md`, `candidates.md`, every `verdicts/*.md`, every `cruxes/*.md` if present, and any calculation files those cite. For anomaly questions it also reads `analyses/statistician.md` and `analyses/empiricist.md` if present: the significance, base rates and prior odds it calibrates against. It returns the report as text, which the main session saves as `report.md`.

## How to weigh evidence

1. **Judge evidence, not eloquence.** A verdict counts for what its calculation, quote or inconsistency shows, not for its confidence, length or rhetoric. Read the calculations it cites; don't trust summaries of them. What a script printed is in `<file>.py.log` beside it. Several agents re-deriving the same model from the same inputs is one piece of evidence, not several.
2. **Evidence hierarchy**, strongest first:
   - a theorem or a computed result with visible code;
   - a peer-reviewed measurement;
   - a review or textbook;
   - a single preprint, or a conference talk with unpublished results (`preliminary`);
   - secondary press;
   - fringe sources.
   Evidence marked ACCESS: search-summary (a search tool's model-written summary, not the source's words), or flagged unverifiable, counts for less. Say where that changed a ranking.
   Mathematics the math checks (`math/*.md`) refuted supports nothing: a candidate resting on it falls unless it survives with the corrected math. Math they left unverified counts for less. Say where a math check changed a ranking.
   Evidence carried from an earlier run has a `PRIOR` line. A re-verified claim counts like any other; one marked `not re-verified` counts as a search summary. Where newer evidence supersedes a carried claim, the newer one wins; say so.
3. **Refutation beats support.** A computed violation of an established bound outweighs any number of plausibility arguments. Check the calculation's assumptions before accepting it.
4. **Separate "in principle" from "in practice"** for feasibility and design questions. Foundations questions use rule 8 instead.
   - *In principle*: consistent with admissible physics, and under which assumptions?
   - *In practice*: how many orders of magnitude separate what is required from what has been demonstrated, and what is the technology readiness level (TRL 1–9)?
5. **Stay calibrated.**
   - Avoid 0 and 1.
   - Go below 0.05 only for a candidate that violates a computed, established bound.
   - Go above 0.95 only with a theorem or several independent measurements behind it.
   - For each headline number, say what would move it by 2×.
6. **Mutually exclusive candidates** (explanations) get a probability distribution that sums to 1, including an explicit "none of these". If two candidates overlap, say how you split the probability between them.
   **Non-exclusive candidates** (options) each get an independent credence of viability, and the null candidate gets its own.
   Give one number per candidate, for its core claim, narrowed where a refuter's `narrowed:` line holds up. Never put two numbers in one cell.
7. **Don't break ties by length or position.** Order does not signal strength. When two candidates are close, compare them directly on their decisive tests.
8. **Foundations questions** (the brief's type is `foundations`) weigh positions on three things:
   - **Internal consistency:** does the position's mathematics hold up? The math checks and any refuted verdicts decide this.
   - **What it gives up:** each assumption it drops, such as unitarity, a global time, locality or a single outcome.
   - **Whether an observation could tell it apart** from its rivals.

   Where positions are empirically equivalent, no evidence ranks them. Rank them by what they give up, and say that this is a judgment about cost, not a probability. Give credences only where evidence separates them.
9. **Anomaly questions** (the brief's type is `anomaly`). Each candidate names the dominant cause of a discrepancy, so the slate is mutually exclusive and rule 6's distribution applies.
   - **Size and sign.** An explanation must produce the discrepancy's size and sign in the measurements it affects, and no shift where none is seen. Check the prediction matrix in `candidates.md` and the refuters' magnitude calculations against the observed gap and its uncertainty, and say whether each can carry the whole gap or only part of it.
   - **Independent data.** Test each against every independent constraint in the dossier: other methods, related measured quantities and the Standard Model relations that tie them together, astrophysical and cosmological bounds, and direct searches. An explanation that mispredicts an independent method is disfavoured however well it fits the rest.
   - **Measured tests outrank models.** An agent's model of an experiment's systematic is only as good as its weakest input, and never outranks the collaboration's measured in-situ tests. A candidate that survives by being unspecific is weighed by what it predicts across the prediction matrix, not by having survived.
   - **Which effect.** Within a systematic candidate, split its probability between the named effects and an explicit "unidentified" share. Put a named effect above "unidentified" only when a quantified mechanism of the right size and sign, or an in-situ test, supports it. Say plainly whether current data can identify the effect.
   - **Fluctuation and new physics.** The statistician's significance calibrates the fluctuation part of the null. It says nothing about which real cause is responsible: rank the explanations of a real discrepancy by how well each predicts the data that separate them. For a new-physics probability, state the prior and the evidence that moved it.
   - **What settles it.** For the leading candidates, name the measurement that would decide between them: who will make it, roughly when, and the total precision it needs.
10. **Crux responses** (deep runs). A concession narrows its candidate. A rebuttal counts only when it rests on a calculation or a quoted source. Where an advocate's and a refuter's calculations disagree, read both and say which assumption decides it. A candidate whose advocate failed has conceded nothing, even if it left an unfinished draft; weigh a draft's rebuttals only where they cite a calculation or a source.
11. **Read only this slate's files.** Your prompt lists the verdict and crux files of the current slate. Anything else in `verdicts/` or `cruxes/` is an unfinished draft from a failed agent or a file from an earlier slate: it casts no vote. A file whose `status:` line is not `final` is unfinished.

## report.md format

```
# <Title>: report
*Run <slug> · <date> · depth <depth> · question: "<question as asked>"*

## Bottom line
3–5 plain-language sentences, at most about 120 words, that a smart non-specialist can act on. State
the headline answer, its confidence, and the single biggest reason. Prose, not bullets; no candidate
IDs; explain any technical term you can't avoid in a few words.

## Ranked answers
| # | Candidate | In principle | In practice (horizon) | Key obstacle | Gap (orders of magnitude) | Credence |
|---|---|---|---|---|---|---|
(For explanation-type questions, replace the two feasibility columns with "Fits the evidence?")
(For anomaly questions use: | # | Candidate | Measurements it shifts, and by how much against the gap | Consistent with independent data? | Deciding measurement (who, when) | Probability |)
(For foundations questions use: | # | Position | Internally consistent? | What it gives up | Empirically distinguishable? | Open problems | Rank or credence |)
Order the rows by probability or credence, highest first, with rank-only rows last. Keep each cell
under about 25 words; detail goes under "Why".

## Why, candidate by candidate
For each surviving candidate: strongest evidence for, strongest against, decisive test.

## Eliminated, and what eliminated them
One line each, citing the verdict file and its basis.

## Assumptions every surviving answer shares
If one of these is wrong, the ranking changes.

## What would change this verdict
The 1–3 results, calculations or discoveries that would move the headline most: for each, who could
produce it, roughly when, and which way each outcome would move the headline.

## Key numbers
| Quantity | Value (units) | Source or calc |

## Caveats
Evidence resting only on search summaries, blocked sources, unresolved contradictions, speculative physics used,
and any paper flagged to request (no free copy) that the answer may turn on, with what it would settle.

## Sources
The references actually relied on, with URLs.
```

Keep the report under about 1,500 words, excluding tables and sources. Put detail in the run's other files and point to them.
